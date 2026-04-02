"""
zhuxy_arm_controller.py
机械臂自动抓放序列控制器 —— 最小功能单元

解决问题：原tcp_client.py中序列只发送第一条指令、无法自动推进的问题。

正确流程（状态机）：
  发送抓取位置
    → 收到 'fall'  → 吸盘ON  → 发送放置位置
    → 收到 'down'  → 吸盘OFF → 发送下一个抓取位置（或结束）

使用方法：
  直接运行此脚本，将使用zhuxy_config.py中的TEST_DATA进行测试
  运行前请确保机械臂和吸盘串口均已连接
"""

import socket
import serial
import threading
import time
import math

# 导入本项目的配置
from zhuxy_config import ARM_TCP, SUCTION_COM, ACTION_CONFIG, TEST_DATA


class ArmController:
    """机械臂+吸盘联合控制器"""

    def __init__(self):
        self.tcp_sock = None          # TCP socket
        self.ser = None               # 串口
        self.queue = []               # 动作队列，格式 [x,y,z,Rx,Ry,Rz_deg]
        self.current_index = 0        # 当前待执行的队列索引
        self.is_running = False       # 序列运行标志
        self._recv_thread = None      # 接收线程
        self._done_event = threading.Event()  # 序列完成信号
        self._lock = threading.Lock()         # 防止并发发送

    # ------------------------------------------------------------------ 连接管理

    def connect(self):
        """建立TCP和串口连接，返回True表示全部成功"""
        # --- TCP ---
        for attempt in range(1, ACTION_CONFIG['connect_retry'] + 1):
            try:
                self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_sock.connect((ARM_TCP['ip'], ARM_TCP['port']))
                print(f"✓ TCP已连接：{ARM_TCP['ip']}:{ARM_TCP['port']}")
                break
            except Exception as e:
                print(f"TCP连接失败（第{attempt}次）：{e}")
                self.tcp_sock = None
                if attempt == ACTION_CONFIG['connect_retry']:
                    return False
                time.sleep(1)

        # --- 串口 ---
        try:
            self.ser = serial.Serial(
                SUCTION_COM['port'],
                SUCTION_COM['baudrate'],
                timeout=SUCTION_COM['timeout']
            )
            print(f"✓ 串口已连接：{SUCTION_COM['port']}，波特率{SUCTION_COM['baudrate']}")
        except serial.SerialException as e:
            print(f"串口连接失败：{e}")
            print("警告：将在无吸盘模式下运行（仅测试机械臂运动）")

        return True

    def disconnect(self):
        """断开所有连接并停止线程"""
        self.is_running = False
        # 等待接收线程结束
        if self._recv_thread and self._recv_thread.is_alive():
            self._recv_thread.join(timeout=2.0)
        # 关闭TCP
        if self.tcp_sock:
            try:
                self.tcp_sock.close()
            except Exception:
                pass
            self.tcp_sock = None
            print("TCP连接已断开")
        # 关闭串口
        if self.ser and self.ser.is_open:
            self._suction_off()   # 确保离开前吸盘已释放
            self.ser.close()
            print("串口已关闭")

    # ------------------------------------------------------------------ 吸盘控制

    def _suction_on(self):
        """打开吸盘（串口发'1'）"""
        if self.ser and self.ser.is_open:
            self.ser.write(b'1')
            print("吸盘：ON（已吸合）")
        else:
            print("吸盘：ON（模拟，无串口）")

    def _suction_off(self):
        """关闭吸盘（串口发'0'）"""
        if self.ser and self.ser.is_open:
            self.ser.write(b'0')
            print("吸盘：OFF（已释放）")
        else:
            print("吸盘：OFF（模拟，无串口）")

    # ------------------------------------------------------------------ TCP发送

    def _send_position(self, pos):
        """
        向机械臂发送一条位置指令
        :param pos: [x, y, z, Rx, Ry, Rz_deg]，后三轴内部转为弧度发送
        """
        if not self.tcp_sock:
            print("错误：TCP未连接，无法发送指令")
            return False

        # 复制并将后三个角度值转换为弧度
        data = pos[:3] + [round(math.radians(v), 4) for v in pos[3:]]
        msg = "S," + ",".join(map(str, data))

        with self._lock:
            try:
                self.tcp_sock.send(msg.encode('utf-8'))
                print(f"→ 发送指令[{self.current_index}]：{msg}")
                return True
            except Exception as e:
                print(f"发送失败：{e}")
                return False

    # ------------------------------------------------------------------ 接收线程

    def _recv_loop(self):
        """
        接收线程主循环
        监听机械臂信号，驱动状态机推进序列
        信号约定：
          'fall'  → 机械臂已到达抓取位置（低位）→ 吸盘ON → 发送放置位置
          'down'  → 机械臂已到达放置位置（低位）→ 吸盘OFF → 发送下一抓取位置
        """
        print("接收线程已启动，等待机械臂信号...")
        buf = ""  # 接收缓冲区，应对粘包

        while self.is_running:
            try:
                self.tcp_sock.settimeout(1.0)
                chunk = self.tcp_sock.recv(1024)
                if not chunk:
                    print("连接被服务器关闭")
                    break

                buf += chunk.decode('utf-8', errors='replace')

                # 按换行符分割消息（如机械臂每条消息带\n），或直接处理整包
                messages = buf.split('\n')
                buf = messages[-1]  # 最后一段可能不完整，留到下次

                for raw_msg in messages[:-1]:
                    msg = raw_msg.strip()
                    if msg:
                        self._handle_message(msg)

                # 兼容无换行符的情况：直接处理缓冲区内容
                stripped = buf.strip()
                if stripped in ('fall', 'down'):
                    self._handle_message(stripped)
                    buf = ""

            except socket.timeout:
                continue  # 超时属正常，继续等待
            except Exception as e:
                if self.is_running:
                    print(f"接收线程异常：{e}")
                break

        print("接收线程已结束")

    def _handle_message(self, msg):
        """处理一条来自机械臂的消息"""
        print(f"← 收到信号：'{msg}'")

        if msg == 'fall':
            # 机械臂到达抓取位置，开启吸盘
            self._suction_on()
            time.sleep(ACTION_CONFIG['suction_on_delay'])

            # 推进到放置位置
            self.current_index += 1
            if self.current_index >= len(self.queue):
                print("警告：收到'fall'但队列已无放置位置，序列提前结束")
                self._finish()
                return
            print(f"发送放置位置（队列第{self.current_index + 1}条）")
            self._send_position(self.queue[self.current_index])

        elif msg == 'down':
            # 机械臂到达放置位置，关闭吸盘
            self._suction_off()
            time.sleep(ACTION_CONFIG['suction_off_delay'])

            # 推进到下一个抓取位置
            self.current_index += 1
            if self.current_index >= len(self.queue):
                # 所有方块处理完毕
                print(f"序列执行完成，共处理 {len(self.queue) // 2} 个方块")
                self._finish()
                return
            print(f"发送下一抓取位置（队列第{self.current_index + 1}条）")
            self._send_position(self.queue[self.current_index])

    def _finish(self):
        """标记序列完成"""
        self.is_running = False
        self._done_event.set()

    # ------------------------------------------------------------------ 启动接口

    def start(self, queue):
        """
        启动自动序列
        :param queue: 动作列表，格式 [[x,y,z,Rx,Ry,Rz], ...]，奇数索引=抓取，偶数索引=放置
        """
        if not queue:
            print("错误：队列为空，无法启动")
            return False
        if len(queue) % 2 != 0:
            print(f"警告：队列长度{len(queue)}为奇数，最后一条抓取指令将无对应放置")

        self.queue = queue
        self.current_index = 0
        self.is_running = True
        self._done_event.clear()

        # 启动接收线程
        self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._recv_thread.start()

        # 发送第一条抓取位置，驱动状态机开始运转
        print(f"=== 开始执行序列，共{len(queue)}条指令（{len(queue) // 2}个方块）===")
        self._send_position(self.queue[0])
        return True

    def wait_done(self, timeout=None):
        """
        阻塞等待序列完成
        :param timeout: 超时秒数，None表示永久等待
        :return: True=正常完成，False=超时
        """
        completed = self._done_event.wait(timeout=timeout)
        if not completed:
            print(f"超时：序列在{timeout}秒内未完成")
        return completed


# ------------------------------------------------------------------ 主程序入口

if __name__ == '__main__':
    print("=" * 50)
    print("机械臂自动抓放序列测试（使用TEST_DATA）")
    print("=" * 50)

    controller = ArmController()

    if not controller.connect():
        print("连接失败，程序退出")
        exit(1)

    try:
        # 使用配置文件中的测试数据
        queue = TEST_DATA
        print(f"加载测试数据：{len(queue)}条指令，对应{len(queue) // 2}个方块")

        if controller.start(queue):
            # 等待序列完成，超时时间 = 方块数量 × 每块预估时间
            estimated_timeout = len(queue) * ACTION_CONFIG['recv_timeout']
            print(f"等待序列完成（最长等待{estimated_timeout:.0f}秒）...")
            controller.wait_done(timeout=estimated_timeout)

    except KeyboardInterrupt:
        print("\n用户中断程序")

    finally:
        controller.disconnect()
        print("程序已退出")

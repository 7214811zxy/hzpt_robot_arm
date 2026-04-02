import socket
import time
import threading
import math
from src.modules.config import TCP_CONFIG
from src.modules.com import SerialCommunication

class TCPClient:
    def __init__(self, ip=TCP_CONFIG['ip'], port=TCP_CONFIG['port'], debug=TCP_CONFIG['debug']):
        self.debug = debug
        self.ip = ip
        self.port = port
        self.client_socket = None
        self.is_receiving = False
        self.receive_thread = None
        
        # 初始化S位置序列和序列控制变量
        self.s_positions_sequence = []  # 存储多组S位置数据
        self.current_sequence_index = 0  # 当前执行的序列索引
        self.is_sequence_running = False  # 序列是否正在运行
        self.waiting_for_next = False  # 是否正在等待发送下一组数据
        self.sequence_lock = threading.Lock()  # 用于线程同步
        self.data_received = threading.Event()  # 用于数据接收等待

        self.serial = SerialCommunication()     # 创建串口通信实例


    def set_queue(self, queue):
        self.s_positions_sequence = queue
        print(queue)
        print('重新设置队列')

    def connect(self):
        """连接到服务器"""
        if not self.client_socket:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.ip, self.port))
                print(f"成功连接到 {self.ip}:{self.port}")

                # 启动接收线程
                self.is_receiving = True
                self.receive_thread = threading.Thread(target=self.receive_messages)
                self.receive_thread.daemon = True
                self.receive_thread.start()
                return True
            except Exception as e:
                print(f"TCP错误：连接失败: {e}")
                self.client_socket = None
                return False
        return True

    def disconnect(self):
        """断开连接"""
        if self.client_socket:
            try:
                self.is_receiving = False
                self.stop_sequence()
                if self.receive_thread:
                    self.receive_thread.join(timeout=1.0)
                self.client_socket.close()
                self.client_socket = None
                print("已断开连接")
            except Exception as e:
                print(f"断开连接时出错: {e}")

    def process_received_data(self, message):
        """处理接收到的数据"""
        try:
            # 尝试解析接收到的数据
            message = message.strip()
            if not message:
                return
            
            try:
                # 尝试将消息转换为数组
                data = eval(message)
                
                # 验证数据格式
                if isinstance(data, list):
                    if len(data) == 6:  # 单个位置数据
                        self.add_sequence_data(data)
                    elif all(isinstance(item, list) and len(item) == 6 for item in data):  # 多组位置数据
                        for position in data:
                            self.add_sequence_data(position)
                    else:
                        print(f"无效的数据格式: {data}")
                else:
                    print(f"接收的数据不是列表格式: {data}")
                
            except (SyntaxError, ValueError) as e:
                print(f"数据解析失败: {e}")
                
        except Exception as e:
            print(f"数据处理错误: {e}")

    def receive_messages(self):
        self.serial.connect()
        self.serial.send_zero()
        """接收消息的线程函数"""
        while self.is_receiving and self.client_socket:
            try:
                self.client_socket.settimeout(1.0)
                data = self.client_socket.recv(1024)
                print("Try to get message")
                if data:
                    print("get message")
                    message = data.decode('utf-8', errors='replace')
                    print(f"接收: {message}")
                    
                    # 处理接收到的数据
                    # self.process_received_data_dev(message)
                    
                    # 设置数据接收事件
                    self.data_received.set()
                    
                    # 如果正在运行序列且等待下一组数据，检查是否收到"2"
                    # if self.is_sequence_running and self.waiting_for_next:
                    #     if message.strip() == "2" or "2" in message:
                    #         print("检测到信号'2'，准备发送下一组数据")
                    #         self._schedule_next_sequence_item()

                    if message == 'fall':
                        self.serial.send_one()
                        time.sleep(1)

                    if message == 'down':
                        self.serial.send_zero()
                        time.sleep(1)

            except socket.timeout:
                continue
            except Exception as e:
                if self.is_receiving:
                    print(f"接收消息时出错: {e}")
                    break
            except KeyboardInterrupt:
                print("串口警告：用户中断串口程序")


        self.serial.close()
        print("接收线程已结束")

    def send_message(self, message):
        """发送消息"""
        if not self.client_socket:
            print("未连接到服务器")
            return False
        try:
            self.client_socket.send(message.encode('utf-8'))
            print(f"发送: {message}")
            return True
        except Exception as e:
            print(f"发送消息失败: {e}")
            return False

    def start_sequence(self):
        """开始执行S位置序列"""
        if not self.client_socket:
            print("未连接到服务器")
            return False
        
        if not self.s_positions_sequence:
            print("等待接收位置数据...")
            # 等待数据接收
            self.data_received.wait()
            self.data_received.clear()
        
        if self.is_sequence_running:
            print("序列已经在运行中")
            return False
        
        self.is_sequence_running = True
        self.current_sequence_index = 0
        self.waiting_for_next = False
        
        print("开始执行位置序列")
        return self.send_current_sequence_item()

    def stop_sequence(self):
        """停止执行S位置序列"""
        if self.is_sequence_running:
            self.is_sequence_running = False
            self.waiting_for_next = False
            print("已停止序列执行")

    def _schedule_next_sequence_item(self):
        """调度下一个序列项"""
        self.current_sequence_index += 1
        if self.current_sequence_index >= len(self.s_positions_sequence):
            self.is_sequence_running = False
            self.waiting_for_next = False
            print("序列执行完成")
            return
        
        self.waiting_for_next = False
        print(f"发送序列项: {self.current_sequence_index + 1}")
        self.send_current_sequence_item()

    def send_current_sequence_item(self):
        """发送当前序列项"""
        if not self.is_sequence_running or self.current_sequence_index >= len(self.s_positions_sequence):
            if self.is_sequence_running:
                self.is_sequence_running = False
                print("序列执行完成")
            return False
        
        current_data = self.s_positions_sequence[self.current_sequence_index]
        numbers = current_data.copy()
        
        # 将后三个数值从角度转换为弧度
        for i in range(3, 6):
            numbers[i] = round(math.radians(numbers[i]), 3)

        
        # 创建符合服务器期望格式的字符串: "S,1,2,3,4,5,6"
        position_str = "S," + ",".join(map(str, numbers))
        
        if self.send_message(position_str):
            self.waiting_for_next = True
            return True
        else:
            self.is_sequence_running = False
            self.waiting_for_next = False
            return False

    def send_current_sequence_item_dev(self, data):
        """发送当前序列项"""
        # if not self.is_sequence_running or self.current_sequence_index >= len(self.s_positions_sequence):
        #     if self.is_sequence_running:
        #         self.is_sequence_running = False
        #         print("序列执行完成")
        #     return False

        numbers = data.copy()
        # # 将后三个数值从角度转换为弧度
        for i in range(3, 6):
            numbers[i] = round(math.radians(numbers[i]), 3)

        # 创建符合服务器期望格式的字符串: "S,1,2,3,4,5,6"
        position_str = "S," + ",".join(map(str, numbers))

        self.send_message(position_str)

    def add_sequence_data(self, data):
        """添加新的序列数据"""
        if isinstance(data, list) and len(data) == 6:
            try:
                # 确保所有元素都是数值类型
                numbers = [float(x) for x in data]
                self.s_positions_sequence.append(numbers)
                print(f"已添加新的序列数据: {numbers}")
                return True
            except (ValueError, TypeError):
                print(f"无效的数据格式: {data}")
                return False
        return False

# 使用示例
if __name__ == "__main__":
    client = TCPClient()

    if client.connect():
        try:
            print("等待接收数据...")

            queue = []
            client.set_queue(queue)

            # 保持程序运行
            while True:
                cmd = input("输入命令 (start/stop/quit): ")
                if cmd == "start":
                    client.start_sequence()
                elif cmd == "stop":
                    client.stop_sequence()
                elif cmd == "quit":
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        finally:
            client.disconnect() 
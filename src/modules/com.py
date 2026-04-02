import serial
import time
from src.modules.config import COM_CONFIG

class SerialCommunication:
    def __init__(self, port=COM_CONFIG['port'], baudrate=COM_CONFIG['baudrate'], timeout=COM_CONFIG['timeout']):
        """
        初始化串口通信
        :param port: 串口号，Windows通常是COMx，Linux/Mac通常是/dev/ttyxxx
        :param baudrate: 波特率
        :param timeout: 超时时间(秒)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        """建立串口连接"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"已连接到串口 {self.port}，波特率 {self.baudrate}")
            return True
        except serial.SerialException as e:
            print(f"串口错误: {e}")
            input("如需继续进行请回车：")
            return False

    def send_zero(self):
        """发送0"""
        if self.ser and self.ser.is_open:
            self.ser.write(b'0')
            print("发送: 0")
            return True
        return False

    def send_one(self):
        """发送1"""
        if self.ser and self.ser.is_open:
            self.ser.write(b'1')
            print("发送: 1")
            return True
        return False

    def close(self):
        """关闭串口连接"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("串口已关闭")

# 使用示例
if __name__ == "__main__":
    # 创建串口通信实例
    serial_comm = SerialCommunication()

    try:
        # 连接串口
        serial_comm.connect()

        # 循环发送0和1
        serial_comm.send_zero()
        time.sleep(1)
        serial_comm.send_one()
        time.sleep(1)


    except KeyboardInterrupt:
        print("串口警告：用户中断串口程序")

    finally:
        # 确保串口被关闭
        serial_comm.close()
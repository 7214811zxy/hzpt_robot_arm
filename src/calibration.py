from modules.tcp_client import TCPClient


if __name__ == '__main__':
    queue = [[-25.343, 453.594, 133.487, -180, 0, -90]]

    # 这里需要socket连接发送数据
    client = TCPClient()

    if client.connect():
        try:
            while True:
                set_queue = input('输入调整值:').split()
                print(set_queue)
                if len(set_queue) > 3:
                    print("数据无效（三位）")
                    break

                check = input(f"请检查增加量为{set_queue}，Y/N")

                if check in ['Y', 'y']:

                    for i in range(0, 3):
                        queue[0][i] += float(set_queue[i])

                    print(queue)

                    print("等待接收数据...")

                    client.set_queue(queue)

                    client.start_sequence()


        except KeyboardInterrupt:
            print("\n程序被用户中断")
        finally:
            client.disconnect()

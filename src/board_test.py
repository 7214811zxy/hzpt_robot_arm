from modules.tcp_client import TCPClient
from modules.board import Board
from config import QUEUE_CONFIG, BOARD_CONFIG

if __name__ == '__main__':
    # 初始化棋盘
    board = Board()
    # 这里需要socket连接发送数据
    client = TCPClient()

    if client.connect():
        try:
            while True:
                # 测试获取单个格子的中心点
                cell_name = input("Enter cell name: ")

                if cell_name == "AA":
                    # 棋盘原点
                    mech_center = (BOARD_CONFIG['coordinate_calibration']['origin_mechanical'][0], 
                                  BOARD_CONFIG['coordinate_calibration']['origin_mechanical'][1])
                    print(f"棋盘原点的机械坐标: {mech_center}")
                
                elif cell_name == "BB":
                    # 对角点 (根据棋盘宽度和高度计算)
                    mech_center = (BOARD_CONFIG['coordinate_calibration']['diagonal_point_mechanical'][0],
                                   BOARD_CONFIG['coordinate_calibration']['diagonal_point_mechanical'][1])
                    print(f"棋盘右下角点的机械坐标: {mech_center}")
                
                elif cell_name == "CC":
                    # 左上角点 (x轴为0，y轴为height)
                    mech_center = (BOARD_CONFIG['coordinate_calibration']['x_point_mechanical'][0],
                                   BOARD_CONFIG['coordinate_calibration']['x_point_mechanical'][1])
                    print(f"棋盘左上角点的机械坐标: {mech_center}")
                
                elif cell_name == "DD":
                    # 右上角点 (x轴为width，y轴为height)
                    mech_center = (BOARD_CONFIG['coordinate_calibration']['y_point_mechanical'][0],
                                   BOARD_CONFIG['coordinate_calibration']['y_point_mechanical'][1])
                    print(f"棋盘右上角点的机械坐标: {mech_center}")
                
                elif len(cell_name) == 2 or len(cell_name) == 3:
                    board_center, mech_center = board.get_cell_center(cell_name)

                    if mech_center:
                        print(f"格子 {cell_name} 的机械坐标系中心点: {mech_center}")
                    else:
                        print(f"格子 {cell_name} 的棋盘坐标系中心点: {board_center}")

                else:
                    cell_list = cell_name.split()

                    mech_center, _, _ = board.get_shape_center(cell_list)

                queue = [[round(mech_center[0], 3), round(mech_center[1], 3), QUEUE_CONFIG['board_Z'], QUEUE_CONFIG['Rx'], QUEUE_CONFIG['Ry'], QUEUE_CONFIG['Rz']]]
                print(queue)

                print("等待接收数据...")

                client.set_queue(queue)

                client.start_sequence()

        except KeyboardInterrupt:
            print("\n程序被用户中断")
        finally:
            client.disconnect()

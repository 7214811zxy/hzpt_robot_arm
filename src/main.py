import time
from modules.vision_processor import TetrisProcessor
from modules.take_photo import take_photo
from modules.place_tetris import place_Q1, tetris_optimal_placement
from modules.board import Board
from modules.join_queue import join_queue
from modules.tcp_client import TCPClient
from modules.config import PLACE_CONFIG

TEST_DATA = [[-427.479, 115.122, 100, -180, 0, -90], [-227.731, 464.273, 90, -180, 0, -58],
             [-385.093, 325.585, 100, -180, 0, -58], [-170.772, 407.34, 90, -180, 0, -17],
             [-318.173, 306.699, 100, -180, 0, -17], [-213.549, 478.54, 90, -180, 0, -100],
             [-446.446, 523.574, 100, -180, 0, -100], [-156.59, 421.608, 90, -180, 0, -118],
             [-702.782, 300.222, 100, -180, 0, -118], [-120.962, 371.775, 90, -180, 0, -50],
             [-528.966, 121.567, 100, -180, 0, -50], [-206.515, 514.174, 90, -180, 0, -8],
             [-636.218, 273.317, 100, -180, 0, -8], [-178.036, 485.708, 90, -180, 0, 70],
             [-632.32, 365.768, 100, -180, 0, 70], [-149.556, 457.241, 90, -180, 0, 82],
             [-300.37, 375.094, 100, -180, 0, 82], [-121.077, 428.775, 90, -180, 0, 114],
             [-469.723, 80.153, 100, -180, 0, 114], [-96.158, 410.98, 90, -180, 0, 266],
             [-583.629, 403.915, 100, -180, 0, 266], [-60.673, 418.173, 90, -180, 0, 361],
             [-341.321, 342.136, 100, -180, 0, 361], [-174.563, 524.92, 90, -180, 0, 256],
             [-591.394, 195.751, 100, -180, 0, 256], [-138.964, 489.338, 90, -180, 0, 196],
             [-470.399, 154.495, 100, -180, 0, 196], [-82.062, 453.772, 90, -180, 0, 185],
             [-360.52, 184.457, 100, -180, 0, 185], [-117.719, 524.947, 90, -180, 0, 303],
             [-454.869, 472.303, 100, -180, 0, 303], [-153.318, 553.438, 90, -180, 0, 390],
             [-243.677, 316.555, 100, -180, 0, 390], [-82.119, 482.273, 90, -180, 0, 228],
             [-379.373, 135.499, 100, -180, 0, 228], [-39.444, 468.062, 90, -180, 0, 306],
             [-524.43, 370.299, 100, -180, 0, 306], [-82.178, 517.886, 90, -180, 0, 476],
             [-433.688, 296.874, 100, -180, 0, 476], [-110.7, 567.727, 90, -180, 0, 575],
             [-449.105, 405.01, 100, -180, 0, 575], [-68.039, 553.528, 90, -180, 0, 446],
             [-361.278, 411.686, 100, -180, 0, 446], [-32.411, 503.695, 90, -180, 0, 514],
             [-406.324, 241.375, 100, -180, 0, 514], [-0.444, 507.296, 90, -180, 0, 581],
             [-506.391, 427.626, 100, -180, 0, 581], [-71.671, 592.712, 90, -180, 0, 628],
             [-334.132, 243.889, 100, -180, 0, 628], [-114.333, 606.911, 90, -180, 0, 601],
             [-528.813, 484.74, 100, -180, 0, 601], [-28.981, 564.263, 90, -180, 0, 654],
             [-392.891, 450.544, 100, -180, 0, 654], [-85.969, 635.445, 90, -180, 0, 581],
             [-596.717, 314.975, 100, -180, 0, 581], [27.949, 521.581, 90, -180, 0, 495],
             [-477.96, 254.849, 100, -180, 0, 495], [-0.588, 578.547, 90, -180, 0, 568],
             [-276.433, 259.96, 100, -180, 0, 568], [-29.096, 621.263, 90, -180, 0, 607]]

if __name__ == '__main__':
    '''
    ===step1===
    摄像机拍照并保存图片
    '''
    # # 调用拍照函数
    take_photo()

    '''
    ===step2===
    处理图片，并计算所有图形数量、角度及坐标
    stats：存储所有图形数据（类型、矫正角度、坐标）的字典
    number_list：存储所有图形数量的数组
    '''
    # 创建处理器实例并处理图像
    processor = TetrisProcessor()
    stats, number_list, results = processor.process_image()

    '''===step3===
    创建棋盘类，计算摆放逻辑，演算如何摆放，并求出摆放的图形的中心点坐标、姿态以及摆放顺序
    '''
    board = Board()

    # 保存所有方块计算后的中心点坐标
    center_list = []

    # 保存方块的放置顺序
    type_list = []

    # 保存方块的旋转角度
    angle_list = []

    '''===以下是例程===
    # 获取该方块的格子
    highlight_cells = ['B11', 'A10', 'B10', 'C10']

    # 获取该方块中心点
    center, _ = board.get_shape_center(highlight_cells)

    if board.debug:
        # 重新可视化，显示高亮的图形
        board.visualize_board(highlight_cells)
    ===以上是例程==='''

    if number_list != None:
        if number_list == [5, 5, 5, 5, 5, 5, 5]:
            print("第一题")
            place_step = place_Q1()
            for i in range(len(place_step)):
                # 获取该方块的格子
                highlight_cells = place_step[i][2]
                # 获取该方块中心点
                center, _, _ = board.get_shape_center(highlight_cells)
                center_list.append(center)
                type_list.append(place_step[i][0])
                angle_list.append(place_step[i][1])
                if board.debug:
                    # 重新可视化，显示高亮的图形
                    board.visualize_board(highlight_cells)

        else:
            print("第二题")
            place_step = tetris_optimal_placement(number_list, PLACE_CONFIG['order'])
            # 打印结果
            for step in place_step:
                print(step)
            for i in range(len(place_step)):
                # 获取该方块的格子
                highlight_cells = place_step[i][2]
                # 获取该方块中心点
                center, _, _ = board.get_shape_center(highlight_cells)
                center_list.append(center)
                type_list.append(place_step[i][0])
                angle_list.append(place_step[i][1])
                if board.debug:
                    # 重新可视化，显示高亮的图形
                    board.visualize_board(highlight_cells)

        # stats是存储所有图形数据的字典
        print(stats)

        # number_list是存储目前所有图形数量(I、L_left、L_right、O、T、Z_left、Z_right)
        print(number_list)

        # center_list保存所有方块计算后的中心点坐标
        print(center_list)

        # type_list保存方块的放置顺序
        print(type_list)

        # angle_list保存方块的旋转角度
        print(angle_list)

        '''===step4===
        根据摆放顺序发出指令
        '''

        # 放置机械臂行动坐标的队列
        queue = join_queue(stats, number_list, center_list, type_list, angle_list)

        print(queue)
        print(len(queue))

        # 这里需要socket连接发送数据
        client = TCPClient()

        if client.connect():
            try:
                print("等待接收数据...")

                client.set_queue(queue)

                if client.debug:
                    # 保持程序运行
                    client.send_message("link test")
                    # client.send_current_sequence_item()
                    TEST_DATA_INDEX = 0
                    while True:
                        if TEST_DATA_INDEX == len(TEST_DATA) -1:
                            break
                        input("next...")
                        client.send_current_sequence_item_dev(TEST_DATA[TEST_DATA_INDEX])
                        TEST_DATA_INDEX += 1
                else:
                    client.start_sequence()

            except KeyboardInterrupt:
                print("\n程序被用户中断")
            finally:
                client.disconnect()

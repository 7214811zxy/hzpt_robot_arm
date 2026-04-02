from src.modules.config import QUEUE_CONFIG

def join_queue(stats, number_list, center_list, type_list, angle_list):
    # 放置机械臂行动坐标的队列
    queue = []
    order_list = []
    if QUEUE_CONFIG['order'] == 0:
        for i in range(len(number_list)):
            order_list.append(0)
    elif QUEUE_CONFIG['order'] == 1:
        for i in range(len(number_list)):
            order_list.append(number_list[i]-1)

    for i in range(len(center_list)):
        if QUEUE_CONFIG['debug']:
            print(f'\n====现在是第{i + 1}个方块信息====')
        if type_list[i] == 'I':
            tetris_type = type_list[i]
            # print(tetris_type)

            # 这是要去抓取的目标方块的坐标
            start_coord = stats['I']['blocks'][order_list[0]]['coords']
            # print(start_coord[0],start_coord[1])

            # 这是要去抓取的目标方块的需要旋转的角度（顺时针为负，逆时针为正）
            to_angle = stats['I']['blocks'][order_list[0]]['angle'] - angle_list[i]
            if to_angle > 90 and to_angle <= 270:
                to_angle = to_angle - 180
            elif to_angle < -90 and to_angle >= -270:
                to_angle = to_angle + 180
            elif to_angle > 270:
                to_angle = to_angle - 360
            elif to_angle < -270:
                to_angle = to_angle + 360
            # print(to_angle)

            # 这是放置的坐标
            to_coord = center_list[i]
            # print(to_coord[0],to_coord[1])

            if QUEUE_CONFIG['debug']:
                print(
                    f'本次抓取方块{type_list[i]}-{order_list[0] + 1}，坐标：（{start_coord[0]}，{start_coord[1]}），旋转{to_angle}度后放置到坐标（{to_coord[0]},{to_coord[1]}）')
            if QUEUE_CONFIG['order'] == 0:
                order_list[0] = order_list[0] + 1
            elif QUEUE_CONFIG['order'] == 1:
                order_list[0] = order_list[0] - 1

        elif type_list[i] == 'L_left':
            tetris_type = type_list[i]
            # print(tetris_type)

            # 这是要去抓取的目标方块的坐标
            start_coord = stats['L_left']['blocks'][order_list[1]]['coords']
            # print(start_coord[0],start_coord[1])

            # 这是要去抓取的目标方块的需要旋转的角度（顺时针为负，逆时针为正）
            to_angle = stats['L_left']['blocks'][order_list[1]]['angle'] - angle_list[i]
            if to_angle > 180:
                to_angle = to_angle - 360
            if to_angle < -180:
                to_angle = to_angle + 360
            # print(to_angle)

            # 这是放置的坐标
            if angle_list[i] == 0:
                to_coord = (center_list[i][0] - QUEUE_CONFIG['L_shape_offset'], center_list[i][1] - QUEUE_CONFIG['L_shape_offset'])

            elif angle_list[i] == 90:
                to_coord = (center_list[i][0] - QUEUE_CONFIG['L_shape_offset'], center_list[i][1] + QUEUE_CONFIG['L_shape_offset'])

            elif angle_list[i] == 180:
                to_coord = (center_list[i][0] + QUEUE_CONFIG['L_shape_offset'], center_list[i][1] + QUEUE_CONFIG['L_shape_offset'])

            elif angle_list[i] == 270:
                to_coord = (center_list[i][0] + QUEUE_CONFIG['L_shape_offset'], center_list[i][1] - QUEUE_CONFIG['L_shape_offset'])

            # to_coord = center_list[i]
            # print(to_coord[0],to_coord[1])

            if QUEUE_CONFIG['debug']:
                print(
                    f'本次抓取方块{type_list[i]}-{order_list[1] + 1}，坐标：（{start_coord[0]}，{start_coord[1]}），旋转{to_angle}度后放置到坐标（{to_coord[0]},{to_coord[1]}）')
            if QUEUE_CONFIG['order'] == 0:
                order_list[1] = order_list[1] + 1
            elif QUEUE_CONFIG['order'] == 1:
                order_list[1] = order_list[1] - 1

        elif type_list[i] == 'L_right':
            tetris_type = type_list[i]
            # print(tetris_type)

            # 这是要去抓取的目标方块的坐标
            start_coord = stats['L_right']['blocks'][order_list[2]]['coords']
            # print(start_coord[0],start_coord[1])

            # 这是要去抓取的目标方块的需要旋转的角度（顺时针为负，逆时针为正）
            to_angle = stats['L_right']['blocks'][order_list[2]]['angle'] - angle_list[i]
            if to_angle > 180:
                to_angle = to_angle - 360
            if to_angle < -180:
                to_angle = to_angle + 360
            # print(to_angle)

            # 这是放置的坐标
            if angle_list[i] == 0:
                to_coord = (center_list[i][0] - QUEUE_CONFIG['L_shape_offset'], center_list[i][1] - QUEUE_CONFIG['L_shape_offset'])

            elif angle_list[i] == 90:
                to_coord = (center_list[i][0] - QUEUE_CONFIG['L_shape_offset'], center_list[i][1] + QUEUE_CONFIG['L_shape_offset'])

            elif angle_list[i] == 180:
                to_coord = (center_list[i][0] + QUEUE_CONFIG['L_shape_offset'], center_list[i][1] + QUEUE_CONFIG['L_shape_offset'])

            elif angle_list[i] == 270:
                to_coord = (center_list[i][0] + QUEUE_CONFIG['L_shape_offset'], center_list[i][1] - QUEUE_CONFIG['L_shape_offset'])

            # to_coord = center_list[i]
            # print(to_coord[0],to_coord[1])

            if QUEUE_CONFIG['debug']:
                print(
                    f'本次抓取方块{type_list[i]}-{order_list[2] + 1}，坐标：（{start_coord[0]}，{start_coord[1]}），旋转{to_angle}度后放置到坐标（{to_coord[0]},{to_coord[1]}）')
            if QUEUE_CONFIG['order'] == 0:
                order_list[2] = order_list[2] + 1
            elif QUEUE_CONFIG['order'] == 1:
                order_list[2] = order_list[2] - 1

        elif type_list[i] == 'O':
            tetris_type = type_list[i]
            # print(tetris_type)

            # 这是要去抓取的目标方块的坐标
            start_coord = stats['O']['blocks'][order_list[3]]['coords']
            # print(start_coord[0],start_coord[1])

            # 这是要去抓取的目标方块的需要旋转的角度（顺时针为负，逆时针为正）
            to_angle = stats['O']['blocks'][order_list[3]]['angle'] - angle_list[i]
            while (to_angle > 90 or to_angle < -90):
                if to_angle > 90:
                    to_angle = to_angle - 90
                if to_angle < -90:
                    to_angle = to_angle + 90
            # print(to_angle)

            # 这是放置的坐标
            to_coord = center_list[i]
            # print(to_coord[0],to_coord[1])

            if QUEUE_CONFIG['debug']:
                print(
                    f'本次抓取方块{type_list[i]}-{order_list[3] + 1}，坐标：（{start_coord[0]}，{start_coord[1]}），旋转{to_angle}度后放置到坐标（{to_coord[0]},{to_coord[1]}）')
            if QUEUE_CONFIG['order'] == 0:
                order_list[3] = order_list[3] + 1
            elif QUEUE_CONFIG['order'] == 1:
                order_list[3] = order_list[3] - 1

        elif type_list[i] == 'T':
            tetris_type = type_list[i]
            # print(tetris_type)

            # 这是要去抓取的目标方块的坐标
            start_coord = stats['T']['blocks'][order_list[4]]['coords']
            # print(start_coord[0],start_coord[1])

            # 这是要去抓取的目标方块的需要旋转的角度（顺时针为负，逆时针为正）
            to_angle = stats['T']['blocks'][order_list[4]]['angle'] - angle_list[i]
            if to_angle > 180:
                to_angle = to_angle - 360
            if to_angle < -180:
                to_angle = to_angle + 360
            # print(to_angle)

            # 这是放置的坐标
            to_coord = center_list[i]
            # print(to_coord[0],to_coord[1])

            if QUEUE_CONFIG['debug']:
                print(
                    f'本次抓取方块{type_list[i]}-{order_list[4] + 1}，坐标：（{start_coord[0]}，{start_coord[1]}），旋转{to_angle}度后放置到坐标（{to_coord[0]},{to_coord[1]}）')
            if QUEUE_CONFIG['order'] == 0:
                order_list[4] = order_list[4] + 1
            elif QUEUE_CONFIG['order'] == 1:
                order_list[4] = order_list[4] - 1

        elif type_list[i] == 'Z_left':
            tetris_type = type_list[i]
            # print(tetris_type)

            # 这是要去抓取的目标方块的坐标
            start_coord = stats['Z_left']['blocks'][order_list[5]]['coords']
            # print(start_coord[0],start_coord[1])

            # 这是要去抓取的目标方块的需要旋转的角度（顺时针为负，逆时针为正）
            to_angle = stats['Z_left']['blocks'][order_list[5]]['angle'] - angle_list[i]
            if to_angle > 90 and to_angle <= 270:
                to_angle = to_angle - 180
            elif to_angle < -90 and to_angle >= -270:
                to_angle = to_angle + 180
            elif to_angle > 270:
                to_angle = to_angle - 360
            elif to_angle < -270:
                to_angle = to_angle + 360
            # print(to_angle)

            # 这是放置的坐标
            to_coord = center_list[i]
            # print(to_coord[0],to_coord[1])

            if QUEUE_CONFIG['debug']:
                print(
                    f'本次抓取方块{type_list[i]}-{order_list[5] + 1}，坐标：（{start_coord[0]}，{start_coord[1]}），旋转{to_angle}度后放置到坐标（{to_coord[0]},{to_coord[1]}）')
            if QUEUE_CONFIG['order'] == 0:
                order_list[5] = order_list[5] + 1
            elif QUEUE_CONFIG['order'] == 1:
                order_list[5] = order_list[5] - 1

        elif type_list[i] == 'Z_right':
            tetris_type = type_list[i]
            # print(tetris_type)

            # 这是要去抓取的目标方块的坐标
            start_coord = stats['Z_right']['blocks'][order_list[6]]['coords']
            # print(start_coord[0],start_coord[1])

            # 这是要去抓取的目标方块的需要旋转的角度（顺时针为负，逆时针为正）
            to_angle = stats['Z_right']['blocks'][order_list[6]]['angle'] - angle_list[i]
            if to_angle > 90 and to_angle <= 270:
                to_angle = to_angle - 180
            elif to_angle < -90 and to_angle >= -270:
                to_angle = to_angle + 180
            elif to_angle > 270:
                to_angle = to_angle - 360
            elif to_angle < -270:
                to_angle = to_angle + 360
            # print(to_angle)

            # 这是放置的坐标
            to_coord = (round(center_list[i][0], 3), round(center_list[i][1], 3))
            # print(to_coord[0],to_coord[1])

            if QUEUE_CONFIG['debug']:
                print(
                    f'本次抓取方块{type_list[i]}-{order_list[6] + 1}，坐标：（{start_coord[0]}，{start_coord[1]}），旋转{to_angle}度后放置到坐标（{to_coord[0]},{to_coord[1]}）')
            if QUEUE_CONFIG['order'] == 0:
                order_list[6] = order_list[6] + 1
            elif QUEUE_CONFIG['order'] == 1:
                order_list[6] = order_list[6] - 1


        if queue == []:
            queue.append([start_coord[0], start_coord[1], QUEUE_CONFIG['vision_Z'], QUEUE_CONFIG['Rx'], QUEUE_CONFIG['Ry'], QUEUE_CONFIG['Rz']])
            to_Rz = QUEUE_CONFIG['Rz'] + to_angle

        else:
            queue.append([start_coord[0], start_coord[1], QUEUE_CONFIG['vision_Z'], QUEUE_CONFIG['Rx'], QUEUE_CONFIG['Ry'], to_Rz])
            to_Rz = to_Rz + to_angle


        queue.append([round(to_coord[0], 3), round(to_coord[1], 3), QUEUE_CONFIG['board_Z'], QUEUE_CONFIG['Rx'], QUEUE_CONFIG['Ry'], to_Rz])

    return queue
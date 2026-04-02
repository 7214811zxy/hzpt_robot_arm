import random
def place_Q1():
    '''
        存储格式
                [类型,    (I、L_left、L_right、O、T、Z_left、Z_right)
                姿态,     (标准状态顺时针0、90、180、270)
                []       (方块所在格子数)
                ]
    '''
    a = random.randint(1, 2)
    if a == 1:
        print('方案一')
        place_step = [['L_right', 180, ['A1', 'A0', 'B0', 'C0']],
                      ['T', 180, ['D0', 'E0', 'E1', 'F0']],
                      ['Z_right', 90, ['G0', 'G1', 'F1', 'F2']],
                      ['L_left', 180, ['H0', 'I0', 'J0', 'J1']],
                      ['T', 180, ['B1', 'C1', 'C2', 'D1']],
                      ['L_right', 90, ['H1', 'I1', 'I2', 'I3']],
                      ['L_left', 270, ['A2', 'B2', 'A3', 'A4']],
                      ['O', 0, ['B3', 'B4', 'C3', 'C4']],
                      ['L_left', 270, ['D2', 'E2', 'D3', 'D4']],
                      ['L_right', 90, ['E3', 'F3', 'F4', 'F5']],
                      ['O', 0, ['G2', 'G3', 'H2', 'H3']],
                      ['I', 90, ['J2', 'J3', 'J4', 'J5']],
                      ['Z_right', 90, ['E4', 'E5', 'D5', 'D6']],
                      ['L_right', 180, ['G4', 'G5', 'H4', 'I4']],
                      ['L_left', 180, ['A5', 'B5', 'C5', 'C6']],
                      ['Z_left', 0, ['H5', 'I5', 'H6', 'G6']],
                      ['Z_right', 0, ['A6', 'B6', 'B7', 'C7']],
                      ['Z_left', 0, ['E6', 'F6', 'E7', 'D7']],
                      ['O', 0, ['I6', 'I7', 'J6', 'J7']],
                      ['T', 180, ['F7', 'G7', 'G8', 'H7']],
                      ['I', 90, ['A7', 'A8', 'A9', 'A10']],
                      ['I', 0, ['B8', 'C8', 'D8', 'E8']],
                      ['Z_left', 90, ['F8', 'F9', 'G9', 'G10']],
                      ['O', 0, ['H8', 'H9', 'I8', 'I9']],
                      ['I', 90, ['J8', 'J9', 'J10', 'J11']],
                      ['T', 180, ['C9', 'D9', 'E9', 'D10']],
                      ['Z_left', 90, ['B9', 'B10', 'C10', 'C11']],
                      ['Z_right', 0, ['E10', 'F10', 'F11', 'G11']],
                      ['L_left', 270, ['H10', 'H11', 'H12', 'I10']],
                      ['O', 0, ['A11', 'A12', 'B11', 'B12']],
                      ['Z_left', 0, ['D11', 'D12', 'C12', 'E11']],
                      ['T', 270, ['I11', 'I12', 'I13', 'J12']],
                      ['L_right', 180, ['E12', 'F12', 'G12', 'E13']],
                      ['I', 0, ['A13', 'B13', 'C13', 'D13']]
                  ]
    elif a == 2:
        print('方案二')
        place_step = [['I', 0, ['A0', 'B0', 'C0', 'D0']],
                      ['Z_right', 90, ['E0', 'E1', 'D1', 'D2']],
                      ['L_right', 180, ['F0', 'F1', 'G0', 'H0']],
                      ['Z_left', 0, ['H1', 'I0', 'I1', 'J0']],
                      ['O', 0, ['A1', 'A2', 'B1', 'B2']],
                      ['L_left', 90, ['C1', 'C2', 'C3', 'B3']],
                      ['O', 0, ['E2', 'E3', 'F2', 'F3']],
                      ['I', 90, ['G1', 'G2', 'G3', 'G4']],
                      ['L_right', 0, ['H2', 'I2', 'J1', 'J2']],
                      ['T', 270, ['A3', 'A4', 'A5', 'B4']],
                      ['Z_right', 90, ['C4', 'C5', 'D3', 'D4']],
                      ['Z_left', 0, ['D5', 'E5', 'E4', 'F4']],
                      ['L_left', 180, ['H3', 'I3', 'J3', 'J4']],
                      ['Z_right', 0, ['H4', 'I4', 'I5', 'J5']],
                      ['Z_left', 90, ['B5', 'B6', 'C6', 'C7']],
                      ['Z_left', 90, ['A6', 'A7', 'B7', 'B8']],
                      ['L_right', 90, ['F5', 'G5', 'G6', 'G7']],
                      ['L_left', 180, ['D6', 'E6', 'F6', 'F7']],
                      ['T', 270, ['H5', 'H6', 'H7', 'I6']],
                      ['I', 90, ['J6', 'J7', 'J8', 'J9']],
                      ['O', 0, ['D7', 'D8', 'E7', 'E8']],
                      ['Z_right', 90, ['H8', 'H9', 'I7', 'I8']],
                      ['I', 90, ['A8', 'A9', 'A10', 'A11']],
                      ['Z_right', 90, ['B9', 'B10', 'C8', 'C9']],
                      ['O', 0, ['D9', 'D10', 'E9', 'E10']],
                      ['L_right', 90, ['F8', 'G8', 'G9', 'G10']],
                      ['L_right', 270, ['F9', 'F10', 'F11', 'G11']],
                      ['T', 90, ['H10', 'I9', 'I10', 'I11']],
                      ['T', 0, ['B11', 'C10', 'C11', 'D11']],
                      ['I', 90, ['J10', 'J11', 'J12', 'J13']],
                      ['T', 0, ['G12', 'H11', 'H12', 'I12']],
                      ['Z_left', 90, ['E11', 'E12', 'F12', 'F13']],
                      ['L_left', 180, ['B12', 'C12', 'D12', 'D13']],
                      ['L_left', 0, ['A12', 'A13', 'B13', 'C13']]
                  ]

    return place_step


def tetris_optimal_placement(block_counts, placement_order, default_angles=None):
    """
    俄罗斯方块最优放置函数

    参数:
        block_counts: 数组，表示每种方块的个数，顺序为 ['I', 'L_left', 'L_right', 'O', 'T', 'Z_left', 'Z_right']
        placement_order: 列表，表示放置顺序，例如 ['I', 'L_left', 'L_right', ...]
        default_angles: 字典，表示每种方块的默认角度（逆时针），例如 {'I': 0, 'L_left': 90, ...}

    返回:
        place_step: 列表，包含最优放置方案
    """
    import copy

    # 将数组转换为字典
    block_types = ['I', 'L_left', 'L_right', 'O', 'T', 'Z_left', 'Z_right']
    block_counts_dict = {block_type: count for block_type, count in zip(block_types, block_counts)}

    # 默认角度设置
    if default_angles is None:
        default_angles = {
            'I': 0,
            'L_left': 0,
            'L_right': 0,
            'O': 0,
            'T': 270, 
            'Z_left': 270,
            'Z_right': 90
        }

    # 定义方块形状（相对坐标，以左下角A0为原点，y轴向上）
    block_shapes = {
        'I': {
            0: [(0, 0), (0, 1), (0, 2), (0, 3)],  # 水平排列 ■■■■
            90: [(0, 0), (1, 0), (2, 0), (3, 0)],  # 垂直排列
            180: [(0, 0), (0, 1), (0, 2), (0, 3)],  # 水平排列
            270: [(0, 0), (1, 0), (2, 0), (3, 0)]  # 垂直排列
        },
        'L_left': {
            0: [(0, 0), (1, 0), (1, 1), (1, 2)],  # ■■■ / ■□□
            90: [(0, 1), (1, 1), (2, 0), (2, 1)],  # ■□ / ■□ / ■■
            180: [(0, 0), (1, 2), (0, 1), (0, 2)],  # □□■ / ■■■
            270: [(0, 0), (0, 1), (1, 0), (2, 0)]  # ■■ / □■ / □■
        },
        'L_right': {
            0: [(1, 0), (1, 1), (1, 2), (0, 2)],  # ■■■ / □□■
            90: [(0, 0), (0, 1), (1, 1), (2, 1)],  # ■■ / □■ / □■
            180: [(0, 0), (0, 1), (0, 2), (1, 0)],  # ■□□ / ■■■
            270: [(0, 0), (1, 0), (2, 0), (2, 1)]  # ■□ / ■□ / ■■
        },
        'O': {
            0: [(0, 0), (0, 1), (1, 0), (1, 1)],  # ■■ / ■■
            90: [(0, 0), (0, 1), (1, 0), (1, 1)],
            180: [(0, 0), (0, 1), (1, 0), (1, 1)],
            270: [(0, 0), (0, 1), (1, 0), (1, 1)]
        },
        'T': {
            0: [(0, 1), (1, 0), (1, 1), (2, 1)],  # ■■■ / □■□
            90: [(0, 0), (0, 1), (0, 2), (1, 1)],  # ■□ / ■■ / ■□
            180: [(0, 0), (1, 0), (1, 1), (2, 0)],  # □■□ / ■■■
            270: [(0, 1), (1, 0), (1, 1), (1, 2)]  # □■ / ■■ / □■
        },
        'Z_left': {
            0: [(2, 1), (1, 0), (1, 1), (0, 0)],  # ■■□ / □■■
            90: [(0, 1), (0, 2), (1, 0), (1, 1)],  # ■□ / ■■ / □■
            180: [(2, 1), (1, 0), (1, 1), (0, 0)],  # 与0度相同
            270: [(0, 1), (0, 2), (1, 0), (1, 1)]  # 与90度相同
        },
        'Z_right': {
            0: [(2, 0), (1, 0), (0, 1), (1, 1)],  # □■■ / ■■□
            90: [(0, 0), (0, 1), (1, 1), (1, 2)],  # □■ / ■■ / ■□
            180: [(2, 0), (1, 0), (0, 1), (1, 1)],  # 与0度相同
            270: [(0, 0), (0, 1), (1, 1), (1, 2)]  # 与90度相同
        }
    }

    # 列的映射
    col_map = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
        'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9
    }
    reverse_col_map = {v: k for k, v in col_map.items()}

    # 定义游戏板
    board = [[False for _ in range(10)] for _ in range(14)]  # 14行10列

    # 检查位置是否可用（适应新坐标系统：A0为原点，y轴向上）
    def is_valid_position(board, block_type, angle, row, col):
        shape = block_shapes[block_type][angle]

        for dr, dc in shape:
            r, c = row + dr, col + dc
            # 转换到实际的数组索引（board数组仍然是从上到下）
            board_row = 13 - r
            if not (0 <= r < 14 and 0 <= c < 10) or not (0 <= board_row < 14) or board[board_row][c]:
                return False

        return True

    # 检查方块是否满足俄罗斯方块规则（重力支撑）
    def is_valid_tetris_placement(board, block_type, angle, row, col):
        """检查方块放置是否符合俄罗斯方块规则（必须有支撑）"""
        if not is_valid_position(board, block_type, angle, row, col):
            return False

        shape = block_shapes[block_type][angle]

        # 检查是否有重力支撑
        has_support = False

        for dr, dc in shape:
            r, c = row + dr, col + dc

            # 如果任何一个方块格子在底部（row=0），则有支撑
            if r == 0:
                has_support = True
                break

            # 检查下方是否有支撑（已有方块）
            board_row_below = 13 - (r - 1)  # 下方一行
            if 0 <= board_row_below < 14 and board[board_row_below][c]:
                has_support = True
                break

        return has_support

    # 将方块放置到游戏板上（适应新坐标系统）
    def place_block(board, block_type, angle, row, col):
        shape = block_shapes[block_type][angle]
        new_board = copy.deepcopy(board)

        for dr, dc in shape:
            r, c = row + dr, col + dc
            # 转换到实际的数组索引
            board_row = 13 - r
            if 0 <= r < 14 and 0 <= c < 10 and 0 <= board_row < 14:
                new_board[board_row][c] = True

        return new_board

    # 获取所有可能的放置位置（适应新坐标系统）
    def get_all_possible_placements(block_type, angle, target_row, target_col):
        """
        获取将方块的任意一部分放在目标格子的所有可能放置方案

        参数:
            block_type: 方块类型
            angle: 方块角度
            target_row: 目标行（从底部A0开始，0-13）
            target_col: 目标列（0-9）

        返回:
            可能的放置位置列表 [(实际放置行, 实际放置列), ...]
        """
        shape = block_shapes[block_type][angle]
        possible_placements = []

        # 对于方块的每个组成部分，尝试将该部分放在目标格子
        for part_idx, (dr, dc) in enumerate(shape):
            # 计算方块左下角应该在的位置
            actual_row = target_row - dr
            actual_col = target_col - dc

            # 检查这个放置是否有效且唯一
            placement = (actual_row, actual_col)
            if placement not in possible_placements:
                possible_placements.append(placement)

        return possible_placements

    # 获取方块放置后的位置坐标（适应新坐标系统）
    def get_positions(block_type, angle, row, col):
        shape = block_shapes[block_type][angle]
        positions = []

        for dr, dc in shape:
            r, c = row + dr, col + dc
            # 确保坐标在有效范围内
            if 0 <= r < 14 and 0 <= c < 10:
                positions.append(f"{reverse_col_map[c]}{r}")

        # 对于I形方块，需要根据角度调整位置顺序
        if block_type == 'I':
            if angle in [90, 270]:  # 水平排列
                # 确保位置按列顺序排列
                positions.sort(key=lambda x: (int(x[1:]), x[0]))
            elif angle in [0, 180]:  # 垂直排列
                # 确保位置按行顺序排列
                positions.sort(key=lambda x: (x[0], int(x[1:])))

        return positions  # 排序以确保一致性

    # 计算放置后的得分（适应新坐标系统：底部行权重更高）
    def calculate_score(board):
        # 在新坐标系统中，底部行（board数组的后面部分）权重更高
        score = 0
        filled_rows = 0

        for r in range(14):
            row_filled = sum(1 for c in range(10) if board[r][c])
            # r=0对应最顶部，r=13对应最底部，所以最底部权重最高
            score += row_filled * (r + 1)

            # 额外奖励：检查是否有填满的行
            if row_filled == 10:  # 行完全填满
                filled_rows += 1
                # 给填满行一个非常高的奖励，特别是底部的行
                score += 800 * (r + 1)  # 底部填满行奖励更多

        # 整体填满行数奖励
        if filled_rows > 0:
            score += filled_rows * filled_rows * 500  # 填满多行有额外的平方奖励

        return score

    # 回填功能：检查并填补游戏板上的空隙
    def backfill_gaps(board, current_block_type, remaining_blocks, place_step):
        """
        回填功能：尝试用当前类型方块填补游戏板上的空隙
        优先填补底部行的空隙，提高整体得分
        """
        if remaining_blocks.get(current_block_type, 0) <= 0:
            return board, remaining_blocks, place_step

        # 从底部开始检查每一行
        for target_row in range(14):
            board_row = 13 - target_row
            # 检查这一行是否有空格
            empty_cols = [col for col in range(10) if not board[board_row][col]]
            if not empty_cols:
                continue  # 这一行已满，跳过

            # 尝试在空格处放置当前类型方块
            best_placement = None
            best_score = -1

            for angle in [0, 90, 180, 270]:
                for target_col in empty_cols:
                    possible_placements = get_all_possible_placements(current_block_type, angle, target_row, target_col)

                    for actual_row, actual_col in possible_placements:
                        if is_valid_tetris_placement(board, current_block_type, angle, actual_row, actual_col):
                            new_board = place_block(board, current_block_type, angle, actual_row, actual_col)
                            score = calculate_score(new_board)

                            # 给回填位置额外奖励
                            row_bonus = (14 - target_row) * 15  # 底部回填优先
                            score += row_bonus

                            # 检查是否能填满一行
                            filled_row = True
                            for c in range(10):
                                board_r = 13 - target_row
                                if not new_board[board_r][c]:
                                    filled_row = False
                                    break

                            if filled_row:
                                score += 500  # 如果能填满一行，给予巨大奖励

                            if score > best_score:
                                best_score = score
                                best_placement = (angle, actual_row, actual_col)

            # 如果找到好的回填位置
            if best_placement is not None:
                angle, row, col = best_placement
                board = place_block(board, current_block_type, angle, row, col)
                positions = get_positions(current_block_type, angle, row, col)

                # 调整角度输出格式
                if current_block_type == 'I':
                    angle = 90 if angle in [90, 270] else 0
                else:
                    angle = (angle - default_angles[current_block_type]) % 360

                if current_block_type in ['Z_left', 'Z_right']:
                    angle = angle % 180

                # 添加到放置步骤
                place_step.append([current_block_type, angle, positions])

                # 减少剩余方块数量
                remaining_blocks[current_block_type] -= 1

                print(f"  回填 - {current_block_type} - 位置:{positions} 角度:{angle}° (行:{target_row})")

                # 如果方块用完了，退出
                if remaining_blocks.get(current_block_type, 0) <= 0:
                    break

        return board, remaining_blocks, place_step

    # 回溯优化：检查前五步是否有更优解，严格按照放置顺序
    def backtrack_optimization(board, block_type, remaining_blocks, place_step, placement_order):
        """
        回溯优化：尝试回溯检查前五步放置是否有更优解，严格按照放置顺序
        如果找到更好的放置组合，则应用新的放置方案，保证放置顺序的一致性

        参数:
            board: 当前游戏板
            block_type: 当前方块类型
            remaining_blocks: 剩余方块数量
            place_step: 当前放置步骤
            placement_order: 放置顺序

        返回:
            优化后的游戏板、剩余方块和放置步骤
        """
        # 只有当已经放置了至少3步才进行回溯
        if len(place_step) < 3:
            return board, remaining_blocks, place_step

        # 决定回溯步数，最多回溯5步，但不超过已放置的步数
        steps_to_backtrack = min(5, len(place_step))

        # 获取最后几步放置的信息
        last_steps = place_step[-steps_to_backtrack:]

        # 创建没有最后几步放置的备用棋盘
        backup_board = [[False for _ in range(10)] for _ in range(14)]
        # 重新放置除最后几步以外的所有方块
        for i in range(len(place_step) - steps_to_backtrack):
            step_type, step_angle, step_positions = place_step[i]
            # 从位置中提取行和列
            for pos in step_positions:
                col = col_map[pos[0]]
                row = int(pos[1:])
                # 设置棋盘状态
                board_row = 13 - row
                if 0 <= board_row < 14 and 0 <= col < 10:
                    backup_board[board_row][col] = True

        # 备份剩余方块数量（包括回溯的方块）
        backup_remaining_blocks = copy.deepcopy(remaining_blocks)

        # 统计回溯步骤中每种方块的数量
        backtrack_block_counts = {}
        for step in last_steps:
            step_type = step[0]
            backtrack_block_counts[step_type] = backtrack_block_counts.get(step_type, 0) + 1
            # 增加回溯的方块数量
            if step_type in backup_remaining_blocks:
                backup_remaining_blocks[step_type] += 1

        # 打印回溯信息
        print(f"🔄 回溯优化 - 尝试回溯{steps_to_backtrack}步，涉及方块：{backtrack_block_counts}")

        # 计算当前得分
        current_score = calculate_score(board)

        # 获取当前的放置序列（按顺序）
        current_sequence = [step[0] for step in place_step[-steps_to_backtrack:]]

        # 创建临时方块顺序列表，确保按照原始的放置顺序进行重新放置
        # 只包含在回溯步骤中出现的方块类型
        temp_order = []
        for bt in placement_order:
            if bt in backtrack_block_counts and backtrack_block_counts[bt] > 0:
                temp_order.append((bt, backtrack_block_counts[bt]))

        # 存储最优放置结果
        best_score = current_score
        best_new_board = None
        best_new_steps = []

        # 用于标记是否找到更好的放置
        found_better = False

        # 尝试重新放置最后几步
        print(f"  📊 当前放置序列: {current_sequence}")
        print(f"  🔍 重新尝试按顺序放置: {[f'{t[0]}:{t[1]}' for t in temp_order]}")

        # 临时变量，存储重新放置的结果
        temp_board = copy.deepcopy(backup_board)
        temp_remaining = copy.deepcopy(backup_remaining_blocks)
        temp_steps = place_step[:-steps_to_backtrack]

        # 严格按照放置顺序进行重新放置
        for block_type, count in temp_order:
            # 放置指定数量的当前类型方块
            for _ in range(count):
                if temp_remaining.get(block_type, 0) <= 0:
                    break

                # 尝试单个放置
                single_score, single_placement, single_fills_row = find_best_single_placement(temp_board, block_type)

                # 应用预测功能
                single_score, single_placement, predicted_fills_row = predict_future_placement(
                    temp_board, block_type, single_score, single_placement, single_fills_row
                )


                # 单个方块放置
                if single_placement is None:
                    print(f"    ⚠️ 无法放置 {block_type} 方块")
                    break

                angle, row, col = single_placement
                temp_board = place_block(temp_board, block_type, angle, row, col)
                positions = get_positions(block_type, angle, row, col)

                # 调整角度输出格式
                if block_type == 'I':
                    display_angle = 90 if angle in [90, 270] else 0
                else:
                    display_angle = (angle - default_angles[block_type]) % 360

                if block_type in ['Z_left', 'Z_right']:
                    display_angle = display_angle % 180

                # 添加到放置步骤
                temp_steps.append([block_type, display_angle, positions])

                # 减少剩余方块数量
                temp_remaining[block_type] -= 1
                print(f"    ✓ 放置{block_type}，位置:{positions}")

        # 计算优化后的得分
        optimized_score = calculate_score(temp_board)
        score_improvement = optimized_score - current_score

        print(f"  📈 回溯优化结果：当前分数 {current_score}，优化后分数 {optimized_score}，提升 {score_improvement}")

        # 如果优化后的分数显著高于当前分数，应用优化
        if optimized_score > current_score + (30 * steps_to_backtrack):
            found_better = True
            best_score = optimized_score
            best_new_board = temp_board
            best_new_steps = temp_steps

        # 如果找到更好的放置组合，应用它
        if found_better:
            # 获取新的放置序列
            new_sequence = [step[0] for step in best_new_steps[-steps_to_backtrack:]]
            print(f"✅ 回溯优化成功 - 替换放置序列：{current_sequence} → {new_sequence}")
            print(f"   分数提升: {best_score - current_score}")

            # 更新棋盘和放置步骤
            board = best_new_board
            place_step = best_new_steps

            # 更新剩余方块数量
            remaining_blocks = temp_remaining
        else:
            print(f"❌ 回溯优化失败 - 未找到更好的放置序列")

        return board, remaining_blocks, place_step

    # 辅助函数：寻找单个方块的最佳放置位置
    def find_best_single_placement(board, block_type):
        """寻找单个方块的最佳放置位置，优先填满底部行，避免某列过高"""
        best_score = -1
        best_placement = None
        best_fills_row = False  # 新增：标记是否能填满整行
        found_valid_placement = False  # 标记是否找到有效放置位置

        # 计算当前各列的高度
        column_heights = []
        for col in range(10):
            # 从底部向上查找第一个空格
            height = 0
            for row in range(14):
                board_row = 13 - row
                if board[board_row][col]:
                    height = row + 1
            column_heights.append(height)

        # 计算平均列高
        avg_height = sum(column_heights) / 10

        # 找出当前最高的列及其高度
        max_height = max(column_heights)
        max_height_col = column_heights.index(max_height)

        # 标记过高的列（比平均高度高2以上）
        high_columns = [i for i, h in enumerate(column_heights) if h > avg_height + 2]

        # 保存所有评估过的位置，避免重复评估
        evaluated_positions = set()

        # 先进行第一轮扫描，找到一个有效的放置位置
        for row in range(14):  # 从底部开始
            for col in range(10):  # 从A列到J列
                if found_valid_placement:
                    break  # 找到第一个位置后跳出
                
                for angle in [0, 90, 180, 270]:
                    if found_valid_placement:
                        break  # 找到第一个位置后跳出
                    
                    possible_placements = get_all_possible_placements(block_type, angle, row, col)
                    
                    for actual_row, actual_col in possible_placements:
                        # 避免重复评估
                        position_key = (actual_row, actual_col, angle)
                        if position_key in evaluated_positions:
                            continue
                        evaluated_positions.add(position_key)
                        
                        # 必须满足俄罗斯方块规则（有重力支撑）
                        if is_valid_tetris_placement(board, block_type, angle, actual_row, actual_col):
                            found_valid_placement = True
                            # 评估该位置的得分
                            current_score, fills_row = evaluate_placement(board, block_type, angle, actual_row, actual_col, avg_height, high_columns, column_heights)
                            
                            # 更新最佳放置
                            if fills_row and not best_fills_row:
                                best_score = current_score
                                best_placement = (angle, actual_row, actual_col)
                                best_fills_row = True
                            elif fills_row and best_fills_row and current_score > best_score:
                                best_score = current_score
                                best_placement = (angle, actual_row, actual_col)
                            elif not best_fills_row and current_score > best_score:
                                best_score = current_score
                                best_placement = (angle, actual_row, actual_col)
                            break  # 找到第一个位置后跳出

        # 如果找到了有效位置，继续扩展搜索范围
        if found_valid_placement:
            # 定义扩展搜索范围（至少3行）
            max_search_row = min(14, best_placement[1] + 4) if best_placement else 14
            max_search_col = 10
            
            print(f"  🔍 扩展搜索：从基本位置向右和向上搜索更多位置")
            
            # 扩展搜索范围
            for row in range(14):
                for col in range(10):
                    # 只搜索尚未评估过的位置
                    for angle in [0, 90, 180, 270]:
                        possible_placements = get_all_possible_placements(block_type, angle, row, col)
                        
                        for actual_row, actual_col in possible_placements:
                            # 避免重复评估
                            position_key = (actual_row, actual_col, angle)
                            if position_key in evaluated_positions:
                                continue
                            evaluated_positions.add(position_key)
                            
                            # 必须满足俄罗斯方块规则（有重力支撑）
                            if is_valid_tetris_placement(board, block_type, angle, actual_row, actual_col):
                                # 评估该位置的得分
                                current_score, fills_row = evaluate_placement(board, block_type, angle, actual_row, actual_col, avg_height, high_columns, column_heights)
                                
                                # 更新最佳放置
                                if fills_row and not best_fills_row:
                                    best_score = current_score
                                    best_placement = (angle, actual_row, actual_col)
                                    best_fills_row = True
                                    print(f"  ✨ 扩展搜索：发现可填满行的位置！位置:({actual_row},{actual_col}) 角度:{angle} 得分:{current_score}")
                                elif fills_row and best_fills_row and current_score > best_score:
                                    best_score = current_score
                                    best_placement = (angle, actual_row, actual_col)
                                    print(f"  ✨ 扩展搜索：发现更好的填满行位置！位置:({actual_row},{actual_col}) 角度:{angle} 得分:{current_score}")
                                elif not best_fills_row and current_score > best_score:
                                    best_score = current_score
                                    best_placement = (angle, actual_row, actual_col)
                                    print(f"  🔍 扩展搜索：发现更好的位置！位置:({actual_row},{actual_col}) 角度:{angle} 得分:{current_score}")

        # 如果找到了最佳放置位置，输出更详细的信息
        if best_placement is not None:
            angle, row, col = best_placement
            temp_board = place_block(board, block_type, angle, row, col)

            # 检查是否填满了行
            filled_rows = 0
            for check_row in range(14):
                board_row_idx = 13 - check_row
                if all(temp_board[board_row_idx][col] for col in range(10)):
                    filled_rows += 1
            
            # 添加填满行的提示
            fill_row_message = f"✅ 填满{filled_rows}行!" if filled_rows > 0 else ""

            # 计算放置后的各列高度
            after_heights = []
            for c in range(10):
                height = 0
                for r in range(14):
                    board_row = 13 - r
                    if temp_board[board_row][c]:
                        height = r + 1
                after_heights.append(height)

            # 输出放置前后的高度变化
            height_changes = [after_heights[i] - column_heights[i] for i in range(10)]
            # 仅当有明显变化时输出详情
            max_change = max(height_changes) if height_changes else 0
            if max_change > 1 or filled_rows > 0:
                print(f"  单个{block_type}最佳放置 - 位置:({row},{col}) 角度:{angle} 得分:{best_score} {fill_row_message}")
                print(f"  列高变化: {height_changes}")

        return best_score, best_placement, best_fills_row  # 返回是否填满行的信息
        
    # 辅助函数：评估放置位置的得分
    def evaluate_placement(board, block_type, angle, actual_row, actual_col, avg_height, high_columns, column_heights):
        """评估指定位置放置方块的得分"""
        new_board = place_block(board, block_type, angle, actual_row, actual_col)

        # 检查是否能填满行
        filled_rows = 0
        for check_row in range(14):
            board_row_idx = 13 - check_row
            if all(new_board[board_row_idx][col] for col in range(10)):
                filled_rows += 1

        # 计算基础分数
        score = calculate_score(new_board)

        # 给底部位置额外奖励（大幅增加底部奖励）
        bottom_bonus = (14 - actual_row) * 5  # 增加到5，更强调底部优先
        score += bottom_bonus

        # 计算放置后的各列高度
        new_column_heights = []
        for c in range(10):
            new_height = 0
            for r in range(14):
                board_row = 13 - r
                if new_board[board_row][c]:
                    new_height = r + 1
            new_column_heights.append(new_height)

        # 计算新的最高列和高度方差
        new_max_height = max(new_column_heights)
        height_variance = sum((h - avg_height) ** 2 for h in new_column_heights) / 10

        # 计算高度增加最多的列
        max_increase = 0
        for c in range(10):
            increase = new_column_heights[c] - column_heights[c]
            max_increase = max(max_increase, increase)

        # 强烈惩罚会导致某列高度增加过多的放置
        height_penalty = 0

        # 如果放置后最高列高度超过7，给予惩罚
        if new_max_height >= 8:
            height_penalty += (new_max_height - 7) * 50

        # 如果高度增加超过3，给予更大惩罚
        if max_increase > 3:
            height_penalty += (max_increase - 3) * 60

        # 如果高度方差增大，也给予惩罚
        if height_variance > 4:
            height_penalty += height_variance * 20

        # 检查是否会在已经过高的列上继续堆积
        affected_high_columns = 0
        shape = block_shapes[block_type][angle]
        for dr, dc in shape:
            r, c = actual_row + dr, actual_col + dc
            if 0 <= c < 10 and c in high_columns:
                affected_high_columns += 1

        # 惩罚在已经过高的列上继续堆积
        if affected_high_columns > 0:
            height_penalty += affected_high_columns * 40

        # 应用高度惩罚
        if height_penalty > 0:
            score -= height_penalty

        # 奖励能够填平较低列的放置
        low_columns_filled = 0
        for c in range(10):
            if column_heights[c] < avg_height - 1 and new_column_heights[c] > column_heights[c]:
                low_columns_filled += 1

        score += low_columns_filled * 40  # 增加奖励填平低列

        # 惩罚会产生空洞的放置
        holes_created = 0
        for c in range(10):
            for r in range(14):
                board_row = 13 - r
                if not new_board[board_row][c] and any(
                        new_board[br][c] for br in range(board_row - 1, -1, -1)):
                    holes_created += 1

        score -= holes_created * 40  # 强烈惩罚产生空洞

        # 给顺序放置额外奖励
        # A到J列顺序奖励
        col_order_bonus = 10 - actual_col  # A列(0)得10分，J列(9)得1分
        score += col_order_bonus

        # I形方块优先水平放置
        if block_type == 'I' and angle in [0, 180]:  # 水平放置
            score += 20
            
        # O形方块特殊处理：优先放置在底部两个格子都有支撑的位置
        if block_type == 'O':
            # 检查底部两个格子的支撑情况
            supports_count = 0
            bottom_positions = []
            
            # O形方块的底部两个格子（相对坐标）
            if angle in [0, 90, 180, 270]:  # O形方块四个角度都一样
                bottom_positions = [(0, 0), (1, 0)]  # 左下和右下
            
            # 检查每个底部位置是否有支撑
            for dr, dc in bottom_positions:
                r, c = actual_row + dr, actual_col + dc
                # 检查是否在底部或下方有方块
                if r == 0:  # 在底部
                    supports_count += 1
                else:
                    board_row_below = 13 - (r - 1)  # 下方一行
                    if 0 <= board_row_below < 14 and 0 <= c < 10 and board[board_row_below][c]:
                        supports_count += 1
            
            # 奖励底部支撑情况
            if supports_count == 2:  # 两个底部格子都有支撑
                score += 120  # 大幅奖励
            elif supports_count == 1:  # 只有一个底部格子有支撑
                score += 60   # 中等奖励

        # T形方块增加90度和270度角度的优先级
        if block_type == 'T' and angle in [90, 270]:  # T字朝左或朝右
            score += 40  # 给予更高的奖励，提高这些角度的优先级

        # 额外奖励：如果能填满行
        if filled_rows > 0:
            # 单个方块填满行比组合更有价值
            score += filled_rows * 800  # 增加奖励，更强调填满行

        # 返回得分和是否填满行
        return score, filled_rows > 0

    # 预留给未来可能添加的辅助函数

    # 预测未来放置：先检查当前行所有列位置，再检查上方三行是否有更优的放置位置
    def predict_future_placement(board, block_type, current_score, current_placement, fills_row):
        """
        预测未来放置：先检查当前行所有列位置，再检查上方三行是否有更优的放置位置
        通过模拟在当前行及上方三行内放置方块，评估是否有更好的放置方案

        参数:
            board: 当前游戏板
            block_type: 当前方块类型
            current_score: 当前最优放置的分数
            current_placement: 当前最优放置的位置 (angle, row, col)
            fills_row: 当前放置方案是否能填满行

        返回:
            最优放置的分数和位置以及是否填满行 (score, (angle, row, col), fills_row)
        """
        if current_placement is None:
            return current_score, current_placement, fills_row

        current_angle, current_row, current_col = current_placement
        best_score = current_score
        best_placement = current_placement
        best_fills_row = fills_row

        # 计算当前各列的高度
        column_heights = []
        for col in range(10):
            # 从底部向上查找第一个空格
            height = 0
            for row in range(14):
                board_row = 13 - row
                if board[board_row][col]:
                    height = row + 1
            column_heights.append(height)

        # 计算平均列高和标记过高的列
        avg_height = sum(column_heights) / 10
        high_columns = [i for i, h in enumerate(column_heights) if h > avg_height + 2]

        # 首先检查当前行的所有列
        target_row = current_row
        # 尝试在当前行的每个位置放置方块
        for col in range(10):
            # 跳过当前列（已经评估过）
            if col == current_col:
                continue

            for angle in [0, 90, 180, 270]:
                possible_placements = get_all_possible_placements(block_type, angle, target_row, col)

                for actual_row, actual_col in possible_placements:
                    # 必须满足俄罗斯方块规则（有重力支撑）
                    if is_valid_tetris_placement(board, block_type, angle, actual_row, actual_col):
                        # 模拟放置方块
                        new_board = place_block(board, block_type, angle, actual_row, actual_col)

                        # 检查是否能填满行
                        filled_rows = 0
                        for check_row in range(14):
                            board_row_idx = 13 - check_row
                            if all(new_board[board_row_idx][c] for c in range(10)):
                                filled_rows += 1

                        # 计算预测得分
                        prediction_score = calculate_score(new_board)

                        # 上方行放置给予额外奖励
                        # 当前行不需要额外奖励，因为不是上方行
                        height_bonus = 0
                        prediction_score += height_bonus

                        # 填满行额外奖励
                        if filled_rows > 0:
                            prediction_score += filled_rows * 400  # 预测到填满行，给予更高奖励

                        # T形方块增加90度和270度角度的优先级
                        if block_type == 'T' and angle in [90, 270]:
                            prediction_score += 40  # 与其他部分保持一致

                        # 计算放置后的各列高度
                        new_column_heights = []
                        for c in range(10):
                            new_height = 0
                            for r in range(14):
                                board_row = 13 - r
                                if new_board[board_row][c]:
                                    new_height = r + 1
                            new_column_heights.append(new_height)

                        # 计算新的最高列
                        new_max_height = max(new_column_heights)

                        # 检查是否会在已经过高的列上继续堆积
                        affected_high_columns = 0
                        shape = block_shapes[block_type][angle]
                        for dr, dc in shape:
                            r, c = actual_row + dr, actual_col + dc
                            if 0 <= c < 10 and c in high_columns:
                                affected_high_columns += 1

                        # 如果会影响过高的列，降低评分
                        if affected_high_columns > 0 or new_max_height >= 8:
                            prediction_score -= 100

                        # 如果能填满行，而当前最佳方案不能填满行，优先选择这个方案
                        if filled_rows > 0 and not best_fills_row:
                            best_score = prediction_score
                            best_placement = (angle, actual_row, actual_col)
                            best_fills_row = True
                            print(f"  🔮 预测：在当前行找到可填满行的方案！行数:{filled_rows}")
                        # 如果都能填满行，选择得分更高的
                        elif filled_rows > 0 and best_fills_row:
                            if prediction_score > best_score:
                                best_score = prediction_score
                                best_placement = (angle, actual_row, actual_col)
                                print(f"  🔮 预测：在当前行找到更好的填满行方案，分数提升:{prediction_score - best_score:.0f}")
                        # 如果当前不能填满行，但之前也没有找到填满行的方案
                        elif not best_fills_row and prediction_score > best_score + 50:  # 同一行需要小一些的提升即可采用
                            best_score = prediction_score
                            best_placement = (angle, actual_row, actual_col)
                            print(f"  🔮 预测：在当前行找到更优放置 - 分数提升:{prediction_score - current_score:.0f}")

        # 定义上方行预测范围
        prediction_rows = min(3, 13 - current_row)  # 避免超出边界
        if prediction_rows <= 0:
            return best_score, best_placement, best_fills_row

        # 然后检查上方三行的放置情况
        for offset in range(1, prediction_rows + 1):
            target_row = current_row + offset

            # 尝试在上方行的每个位置放置方块
            for col in range(10):
                for angle in [0, 90, 180, 270]:
                    possible_placements = get_all_possible_placements(block_type, angle, target_row, col)

                    for actual_row, actual_col in possible_placements:
                        # 必须满足俄罗斯方块规则（有重力支撑）
                        if is_valid_tetris_placement(board, block_type, angle, actual_row, actual_col):
                            # 模拟放置方块
                            new_board = place_block(board, block_type, angle, actual_row, actual_col)

                            # 检查是否能填满行
                            filled_rows = 0
                            for check_row in range(14):
                                board_row_idx = 13 - check_row
                                if all(new_board[board_row_idx][c] for c in range(10)):
                                    filled_rows += 1

                            # 计算预测得分，根据预测深度调整奖励
                            prediction_score = calculate_score(new_board)

                            # 上方行放置给予额外奖励
                            # 越靠上的行，奖励越大（鼓励利用更多空间）
                            height_bonus = offset * 40
                            prediction_score += height_bonus

                            # 填满行额外奖励
                            if filled_rows > 0:
                                prediction_score += filled_rows * 400  # 预测到填满行，给予更高奖励

                            # 计算放置后的各列高度
                            new_column_heights = []
                            for c in range(10):
                                new_height = 0
                                for r in range(14):
                                    board_row = 13 - r
                                    if new_board[board_row][c]:
                                        new_height = r + 1
                                new_column_heights.append(new_height)

                            # 计算新的最高列
                            new_max_height = max(new_column_heights)

                            # 检查是否会在已经过高的列上继续堆积
                            affected_high_columns = 0
                            shape = block_shapes[block_type][angle]
                            for dr, dc in shape:
                                r, c = actual_row + dr, actual_col + dc
                                if 0 <= c < 10 and c in high_columns:
                                    affected_high_columns += 1

                            # 如果会影响过高的列，降低评分
                            if affected_high_columns > 0 or new_max_height >= 8:
                                prediction_score -= 150

                            # 如果能填满行，而当前最佳方案不能填满行，优先选择这个方案
                            if filled_rows > 0 and not best_fills_row:
                                best_score = prediction_score
                                best_placement = (angle, actual_row, actual_col)
                                best_fills_row = True
                                print(f"  🔮 预测：在上方{offset}行找到可填满行的方案！行数:{filled_rows}")
                            # 如果都能填满行，选择得分更高的
                            elif filled_rows > 0 and best_fills_row:
                                if prediction_score > best_score:
                                    best_score = prediction_score
                                    best_placement = (angle, actual_row, actual_col)
                                    print(f"  🔮 预测：找到更好的填满行方案，分数提升:{prediction_score - best_score:.0f}")
                            # 如果当前不能填满行，但之前也没有找到填满行的方案
                            elif not best_fills_row and prediction_score > best_score + 100:  # 上方行需要显著提高才采用
                                best_score = prediction_score
                                best_placement = (angle, actual_row, actual_col)
                                print(f"  🔮 预测：在上方{offset}行发现更优放置 - 分数提升:{prediction_score - current_score:.0f}")

        return best_score, best_placement, best_fills_row

    # 预留函数空间

    # 贪心算法寻找最优放置（严格按照placement_order顺序，遵循俄罗斯方块规则）
    place_step = []
    remaining_blocks = copy.deepcopy(block_counts_dict)

    # 计算总方块数
    total_blocks = sum(remaining_blocks.values())

    print(f"开始放置，按照顺序：{placement_order}")
    print(f"方块数量：{[f'{bt}:{block_counts_dict[bt]}' for bt in placement_order]}")
    print("=" * 60)

    # 严格按照placement_order顺序放置：先摆完所有同类型的方块
    for block_type in placement_order:
        if remaining_blocks.get(block_type, 0) <= 0:
            continue

        # 开始摆放当前类型的方块
        type_count = remaining_blocks[block_type]
        print(f"\n🔶 开始放置 {block_type} 方块，共 {type_count} 个")

        # I形方块特殊处理：当I是第一个摆放的方块时，优先从A0开始水平摆放
        if block_type == 'I' and len(place_step) == 0:
            print("  I形方块是第一个摆放的方块，应用特殊放置策略")

            # 确定需要放置的I形方块数量
            i_count = remaining_blocks['I']

            # 特殊策略：从底部开始水平摆放，先在第0行放两个，然后再往上
            rows_needed = (i_count + 1) // 2  # 向上取整，计算需要的行数

            print(f"  尝试水平放置I形方块，总共{i_count}个，预计需要{rows_needed}行")

            # 依次放置I形方块
            for row in range(rows_needed):
                # 第一个I形方块，水平放置（角度0）
                first_col = 0  # A列
                angle = 0  # 水平

                # 检查是否可以放置
                if is_valid_tetris_placement(board, 'I', angle, row, first_col):
                    # 放置第一个I形方块
                    board = place_block(board, 'I', angle, row, first_col)
                    positions = get_positions('I', angle, row, first_col)
                    place_step.append(['I', 0, positions])  # 角度0度

                    # 减少剩余方块数量
                    remaining_blocks['I'] -= 1
                    total_blocks -= 1
                    placed_count = 1

                    print(f"  第{len(place_step)}步 ✓ - I ({placed_count}/{type_count}) - 位置:{positions} 角度:0°")

                    # 如果还有I形方块，且当前行还能放第二个
                    if remaining_blocks['I'] > 0:
                        # 放置第二个I形方块，优先连在第一个I形方块后面（EFGH列）
                        second_col = 4  # E列，刚好与第一个不重叠，且可能填满一行
                        if is_valid_tetris_placement(board, 'I', angle, row, second_col):
                            board = place_block(board, 'I', angle, row, second_col)
                            positions = get_positions('I', angle, row, second_col)
                            place_step.append(['I', 0, positions])  # 角度0度

                            # 减少剩余方块数量
                            remaining_blocks['I'] -= 1
                            total_blocks -= 1
                            placed_count += 1

                            print(f"  第{len(place_step)}步 ✓ - I ({placed_count}/{type_count}) - 位置:{positions} 角度:0° (连续放置)")

                            # 检查是否成功填满了一行
                            is_row_filled = True
                            board_row_idx = 13 - row
                            for c in range(8):  # 检查前8列是否都已填满
                                if not board[board_row_idx][c]:
                                    is_row_filled = False
                                    break

                            if is_row_filled:
                                print(f"  ✅ 第{row}行成功填满前8列！")
                            
                            # 检查当前行是否还能放第三个I形方块（IJKL列）
                            if remaining_blocks['I'] > 0:
                                third_col = 8  # I列，连接前两个I形方块，可能填满行
                                if is_valid_tetris_placement(board, 'I', angle, row, third_col):
                                    board = place_block(board, 'I', angle, row, third_col)
                                    positions = get_positions('I', angle, row, third_col)
                                    place_step.append(['I', 0, positions])  # 角度0度

                                    # 减少剩余方块数量
                                    remaining_blocks['I'] -= 1
                                    total_blocks -= 1
                                    placed_count += 1

                                    print(f"  第{len(place_step)}步 ✓ - I ({placed_count}/{type_count}) - 位置:{positions} 角度:0° (连续放置)")
                                    print(f"  ✅ 第{row}行已完全填满！")
                        else:
                            # 如果E列不能放，尝试其他列
                            for test_col in [6, 2, 8]:
                                if is_valid_tetris_placement(board, 'I', angle, row, test_col):
                                    second_col = test_col
                                    board = place_block(board, 'I', angle, row, second_col)
                                    positions = get_positions('I', angle, row, second_col)
                                    place_step.append(['I', 0, positions])  # 角度0度

                                    # 减少剩余方块数量
                                    remaining_blocks['I'] -= 1
                                    total_blocks -= 1
                                    placed_count += 1

                                    print(f"  第{len(place_step)}步 ✓ - I ({placed_count}/{type_count}) - 位置:{positions} 角度:0° (备选位置)")
                                    break
                else:
                    print(f"  ⚠️ 无法在行{row}放置I形方块，改用常规策略")
                    break

            # 如果还有剩余的I形方块，使用常规策略放置
            if remaining_blocks['I'] > 0:
                print(f"  还有{remaining_blocks['I']}个I形方块需要放置，切换到常规策略")
            else:
                # 如果I形方块全部放置完成，继续下一种方块
                continue

        # 为I形方块添加额外的水平放置偏好
        elif block_type == 'I' and remaining_blocks['I'] >= 2:
            print(f"  I形方块数量较多({remaining_blocks['I']}个)，增强水平放置偏好")

            # 遍历底部行，尝试水平放置I形方块
            horizontal_placed = 0
            for row in range(min(6, 14)):  # 优先考虑底部6行
                # 检查当前行已有的I形方块位置
                existing_i_positions = []
                for col in range(10):
                    if col <= 6 and is_valid_tetris_placement(board, 'I', 0, row, col) == False:
                        # 检查是否是因为有I形方块导致无法放置
                        # 简单检查：尝试看看col到col+3是否都被占用
                        all_occupied = True
                        for c in range(col, min(col + 4, 10)):
                            board_row = 13 - row
                            if not board[board_row][c]:
                                all_occupied = False
                                break
                        if all_occupied:
                            existing_i_positions.append(col)
                
                    # 找出可能的连接位置
                    possible_cols = []
                    # 如果有已放置的I形方块，尝试在其旁边放置
                    if existing_i_positions:
                        for pos in existing_i_positions:
                            # 检查左侧
                            if pos >= 4 and is_valid_tetris_placement(board, 'I', 0, row, pos - 4):
                                possible_cols.append(pos - 4)
                            # 检查右侧
                            if pos + 4 <= 6 and is_valid_tetris_placement(board, 'I', 0, row, pos + 4):
                                possible_cols.append(pos + 4)
                    else:
                        # 没有已放置的I形方块，尝试从左到右放置
                        possible_cols = [0, 4, 6, 2]
                    
                    # 按优先级尝试放置
                    for col in possible_cols:
                        angle = 0  # 水平放置
                        if is_valid_tetris_placement(board, 'I', angle, row, col) and remaining_blocks['I'] > 0:
                            # 放置I形方块
                            board = place_block(board, 'I', angle, row, col)
                            positions = get_positions('I', angle, row, col)
                            place_step.append(['I', 0, positions])  # 角度0度

                            # 减少剩余方块数量
                            remaining_blocks['I'] -= 1
                            total_blocks -= 1
                            placed_count += 1
                            horizontal_placed += 1

                            print(f"  第{len(place_step)}步 ✓ - I ({placed_count}/{type_count}) - 位置:{positions} 角度:0° (水平优先)")

                            # 检查当前行是否已经填满
                            current_row_filled = True
                            board_row_idx = 13 - row
                            for c in range(10):
                                if not board[board_row_idx][c]:
                                    current_row_filled = False
                                    break
                            
                            if current_row_filled:
                                print(f"  ✅ 第{row}行已完全填满！")
                            
                            # 每放置2个水平I形方块后检查回溯优化
                            if horizontal_placed % 2 == 0 and horizontal_placed >= 2:
                                board, remaining_blocks, place_step = backtrack_optimization(
                                    board, block_type, remaining_blocks, place_step, placement_order
                                )

                            # 限制连续水平放置的数量，防止过度堆积
                            if horizontal_placed >= 4 or remaining_blocks['I'] <= 0:
                                break

                    if horizontal_placed >= 4 or remaining_blocks['I'] <= 0:
                        break

                if horizontal_placed > 0:
                    print(f"  已水平放置{horizontal_placed}个I形方块")

                # 如果I形方块全部放置完成，继续下一种方块
                if remaining_blocks['I'] <= 0:
                    continue

        # 摆完当前类型的所有方块
        placed_count = 0
        while remaining_blocks.get(block_type, 0) > 0:

            # 单个方块放置逻辑
            best_score, best_placement, fills_row = find_best_single_placement(board, block_type)

            # 应用预测功能：检查上方三行是否有更好的放置位置
            predicted_score, predicted_placement, predicted_fills_row = predict_future_placement(board, block_type, best_score,
                                                                            best_placement, fills_row)

            # 如果预测找到更好的放置位置，使用预测结果（除非当前方案能填满行而预测方案不能）
            if predicted_fills_row or (not fills_row and predicted_score > best_score):
                best_score = predicted_score
                best_placement = predicted_placement
                fills_row = predicted_fills_row

            # 如果找不到合法位置，跳过当前方块
            if best_placement is None:
                print(f"⚠️ 无法放置 {block_type} 方块，跳过")
                break

            # 直接使用贪心方案
            angle, row, col = best_placement
            board = place_block(board, block_type, angle, row, col)
            positions = get_positions(block_type, angle, row, col)

            # 对于I形方块，调整角度输出（在新坐标系统中）
            if block_type == 'I':
                angle = 90 if angle in [90, 270] else 0
            else:
                angle = (angle - default_angles[block_type]) % 360

            if block_type == 'Z_left' or block_type == 'Z_right':
                angle = angle % 180

            # 添加到放置步骤
            place_step.append([block_type, angle, positions])

            # 减少剩余方块数量
            remaining_blocks[block_type] -= 1
            total_blocks -= 1
            placed_count += 1

            # 显示放置信息（按类型分组）
            fill_message = "✅ 填满行!" if fills_row else ""
            print(
                f"  第{len(place_step)}步 ✓ - {block_type} ({placed_count}/{type_count}) - 位置:{positions} 角度:{angle}° {fill_message}")

        # 当前类型方块放置完成后，尝试回填
        if placed_count > 0:
            print(f"✅ {block_type} 方块放置完成，共放置 {placed_count} 个")

            # 尝试用剩余的当前类型方块回填空隙
            if remaining_blocks.get(block_type, 0) > 0:
                original_remaining = remaining_blocks.get(block_type, 0)
                board, remaining_blocks, place_step = backfill_gaps(
                    board, block_type, remaining_blocks, place_step
                )
                filled_count = original_remaining - remaining_blocks.get(block_type, 0)
                if filled_count > 0:
                    print(f"📋 回填完成：额外放置了 {filled_count} 个 {block_type} 方块")

    # 严格按照placement_order顺序放置完成
    print(f"\n{'=' * 60}")
    print(f"🎉 俄罗斯方块放置完成！")
    print(f"📋 严格按照顺序：{placement_order}")
    print(f"📊 总共放置了 {len(place_step)} 个方块")
    print(f"📦 最终剩余方块：{remaining_blocks}")
    print(f"⚖️ 所有方块均遵循俄罗斯方块重力规则（有支撑）")
    print(f"🔄 按类型分组放置：先放完所有同类型方块再放下一类型")
    print(f"🔍 使用回溯优化：检查前两步放置是否有更优解")
    print(f"📌 使用回填策略：智能填补游戏板空隙")
    print(f"{'=' * 60}")

    return place_step


# 示例使用
if __name__ == "__main__":
    # 示例输入
    block_counts = [5, 5, 5, 5, 4, 5, 5]

    placement_order = ['I', 'L_left', 'L_right', 'O', 'T', 'Z_left', 'Z_right']

    # 调用函数
    result = tetris_optimal_placement(block_counts, placement_order)

    # 打印结果
    for step in result:
        print(step)

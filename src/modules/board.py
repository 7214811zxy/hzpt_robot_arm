# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from src.modules.config import BOARD_CONFIG
import os
from src.modules.matrix_utils import calculate_calibration_matrix_test

class Board:
    def __init__(self, config=None):
        """
        初始化棋盘类
        :param width: 棋盘总宽度
        :param height: 棋盘总高度
        :param grid_width: 横向格子数
        :param grid_height: 纵向格子数
        :param offset_x: X轴偏移量
        :param offset_y: Y轴偏移量
        :param debug: 是否开启调试模式
        """
        self.config = config if config is not None else BOARD_CONFIG
        self.width = BOARD_CONFIG['width']
        self.height = BOARD_CONFIG['height']
        self.grid_width = BOARD_CONFIG['grid_width']
        self.grid_height = BOARD_CONFIG['grid_height']
        self.offset_x = BOARD_CONFIG['offset_x']
        self.offset_y = BOARD_CONFIG['offset_y']
        self.debug = BOARD_CONFIG['debug']

        self.test_num = 0
        
        # 计算每个格子的宽度和高度
        self.cell_width = BOARD_CONFIG['width'] / BOARD_CONFIG['grid_width']
        self.cell_height = BOARD_CONFIG['height'] / BOARD_CONFIG['grid_height']
        
        # 创建坐标映射字典
        self.coordinate_map = {}
        for row in range(BOARD_CONFIG['grid_height']):
            for col in range(BOARD_CONFIG['grid_width']):
                # 从A0开始命名
                cell_name = f"{chr(65 + col)}{row}"
                # 存储格子的四个角点坐标（从左下角开始顺时针）
                x = BOARD_CONFIG['offset_x'] + col * self.cell_width
                y = BOARD_CONFIG['offset_y'] + row * self.cell_height
                self.coordinate_map[cell_name] = [
                    (x, y),  # 左下角
                    (x + self.cell_width, y),  # 右下角
                    (x + self.cell_width, y + self.cell_height),  # 右上角
                    (x, y + self.cell_height)  # 左上角
                ]
        
        # 初始化坐标系矫正
        self.calibration_enabled = BOARD_CONFIG.get('coordinate_calibration', {}).get('enabled', False)
        if self.calibration_enabled:
            # self.calibration_matrix = self._calculate_calibration_matrix()
            self.calibration_matrix = calculate_calibration_matrix_test(
                target_size_x=self.width,
                target_size_y=self.height,
                origin_mechanical_point=self.config['coordinate_calibration']['origin_mechanical'],
                x_point_mechanical_point=self.config['coordinate_calibration']['x_point_mechanical'],
                y_point_mechanical_point=self.config['coordinate_calibration']['y_point_mechanical'],
                diagonal_point_mechanical_point=self.config['coordinate_calibration']['diagonal_point_mechanical'],
                debug=self.debug
            )
            if self.debug:
                print(f"坐标矫正矩阵:\n{self.calibration_matrix}")
        
        if self.debug:
            self.visualize_board()

    
    def board_to_mechanical(self, board_point):
        """
        将棋盘坐标系中的点转换到机械坐标系中
        :param board_point: 棋盘坐标系中的点 (x, y)
        :return: 机械坐标系中的点 (x, y)
        """
        if not self.calibration_enabled:
            return board_point
        
        # 转换为齐次坐标
        homogeneous_point = np.array([board_point[0], board_point[1], 1])
        
        # 应用矫正矩阵
        mechanical_point = np.dot(self.calibration_matrix, homogeneous_point)
        
        return (mechanical_point[0], mechanical_point[1])
    
    def mechanical_to_board(self, mechanical_point):
        """
        将机械坐标系中的点转换到棋盘坐标系中
        :param mechanical_point: 机械坐标系中的点 (x, y)
        :return: 棋盘坐标系中的点 (x, y)
        """
        if not self.calibration_enabled:
            return mechanical_point
        
        # 转换为齐次坐标
        homogeneous_point = np.array([mechanical_point[0], mechanical_point[1], 1])
        
        # 应用矫正矩阵的逆矩阵
        inv_matrix = np.linalg.inv(self.calibration_matrix)
        board_point = np.dot(inv_matrix, homogeneous_point)
        
        return (board_point[0], board_point[1])

    def get_shape_center(self, cell_names, out = True):
        """
        获取四个相邻格子组成的图形的中心点坐标
        :param cell_names: 四个相邻格子的名称列表，如 ['A0', 'A1', 'B0', 'B1']
        :return: (中心点坐标, 图形边界线列表)
        """
        if len(cell_names) != 4:
            raise ValueError("必须提供4个格子名称")

        # 获取所有格子的角点
        all_points = []
        for cell_name in cell_names:
            if cell_name not in self.coordinate_map:
                raise ValueError(f"无效的格子名称: {cell_name}")
            all_points.extend(self.coordinate_map[cell_name])

        # 计算中心点
        points = np.array(all_points)
        center_x = round(np.mean(points[:, 0]), 3)
        center_y = round(np.mean(points[:, 1]), 3)

        # 获取所有格子的坐标
        cells = [self.coordinate_map[name] for name in cell_names]

        # 找到所有边界线
        boundary_lines = []
        for cell in cells:
            # 检查每条边是否在另一个格子的内部
            for i in range(4):
                start = cell[i]
                end = cell[(i + 1) % 4]
                is_boundary = True
                for other_cell in cells:
                    if cell != other_cell:
                        x1, y1 = other_cell[0]  # 左下角
                        x2, y2 = other_cell[2]  # 右上角
                        # 检查边的中点是否在另一个格子内部
                        mid_x = (start[0] + end[0]) / 2
                        mid_y = (start[1] + end[1]) / 2
                        if x1 < mid_x < x2 and y1 < mid_y < y2:
                            is_boundary = False
                            break
                if is_boundary:
                    boundary_lines.append((start, end))
        
        # 原始棋盘坐标
        board_center = (center_x, center_y)
        
        # 如果启用了坐标系矫正，转换到机械坐标系
        if self.calibration_enabled:
            mechanical_center = self.board_to_mechanical(board_center)
            if self.debug and out:
                print(f"图形中心点棋盘坐标: ({center_x}, {center_y})")
                print(f"图形中心点机械坐标: ({mechanical_center[0]:.3f}, {mechanical_center[1]:.3f})")
            
            return mechanical_center, boundary_lines, board_center
        elif self.debug and out:
            print(f"图形中心点坐标: ({center_x}, {center_y})")

        return board_center, boundary_lines, board_center

    def get_cell_center(self, cell_name):
        """
        获取单个格子的中心点坐标
        :param cell_name: 格子的名称，如 'A0'
        :return: (中心点棋盘坐标, 中心点机械坐标)
        """
        if cell_name not in self.coordinate_map:
            raise ValueError(f"无效的格子名称: {cell_name}")
        
        # 获取格子的四个角点
        cell_corners = self.coordinate_map[cell_name]
        
        # 计算中心点
        points = np.array(cell_corners)
        center_x = round(np.mean(points[:, 0]), 3)
        center_y = round(np.mean(points[:, 1]), 3)
        
        # 原始棋盘坐标
        board_center = (center_x, center_y)
        
        # 如果启用了坐标系矫正，转换到机械坐标系
        mechanical_center = None
        if self.calibration_enabled:
            mechanical_center = self.board_to_mechanical(board_center)
            if self.debug:
                print(f"格子 {cell_name} 中心点棋盘坐标: ({center_x}, {center_y})")
                print(f"格子 {cell_name} 中心点机械坐标: ({mechanical_center[0]:.3f}, {mechanical_center[1]:.3f})")
        elif self.debug:
            print(f"格子 {cell_name} 中心点坐标: ({center_x}, {center_y})")
        
        # 如果是调试模式，生成可视化图像
        if self.debug:
            self.visualize_point(cell_name, board_center)
        
        return board_center, mechanical_center
            
    def visualize_point(self, cell_name, point):
        """
        可视化单个点
        :param cell_name: 格子名称
        :param point: 点的坐标
        """
        # 设置matplotlib支持中文显示
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 创建主图和子图
        if self.calibration_enabled and self.config['coordinate_calibration'].get('visualize_calibration', False):
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 14))
            fig.suptitle(f'格子 {cell_name} 中心点可视化', fontsize=16)
            axes = [ax1, ax2]
            titles = ['原始棋盘坐标系', '矫正后机械坐标系']
        else:
            fig, ax = plt.subplots(figsize=(10, 14))
            axes = [ax]
            titles = ['棋盘坐标系']

        for idx, ax in enumerate(axes):
            is_mechanical = idx == 1
            
            # 绘制所有格子
            for row in range(self.grid_height):
                for col in range(self.grid_width):
                    cell_id = f"{chr(65 + col)}{row}"
                    points = self.coordinate_map[cell_id]
                    
                    # 确定格子颜色
                    facecolor = 'lightblue' if cell_id == cell_name else 'none'
                    
                    if is_mechanical:
                        # 转换坐标到机械坐标系
                        mech_points = [self.board_to_mechanical(p) for p in points]
                        x, y = mech_points[0]
                        width = mech_points[1][0] - x
                        height = mech_points[3][1] - y
                        rect = Rectangle((x, y), width, height,
                                        linewidth=1, edgecolor='black', facecolor=facecolor)
                        
                        # 添加格子名称
                        center_x = x + width / 2
                        center_y = y + height / 2
                    else:
                        rect = Rectangle(points[0], self.cell_width, self.cell_height,
                                        linewidth=1, edgecolor='black', facecolor=facecolor)
                        
                        # 添加格子名称
                        center_x = points[0][0] + self.cell_width / 2
                        center_y = points[0][1] + self.cell_height / 2
                    
                    ax.add_patch(rect)
                    ax.text(center_x, center_y, cell_id, ha='center', va='center')

            # 绘制中心点
            if is_mechanical:
                # 在机械坐标系中显示
                mech_point = self.board_to_mechanical(point)
                ax.scatter(mech_point[0], mech_point[1], color='red', s=200, zorder=5)
                ax.text(mech_point[0], mech_point[1] + 5, f'中心点\n({mech_point[0]:.3f}, {mech_point[1]:.3f})',
                        ha='center', va='bottom', fontsize=12, fontweight='bold')
                
                # 在中心点周围添加醒目的标记
                ax.plot([mech_point[0]-5, mech_point[0]+5], [mech_point[1], mech_point[1]], 
                        color='red', linewidth=2, zorder=4)
                ax.plot([mech_point[0], mech_point[0]], [mech_point[1]-5, mech_point[1]+5], 
                        color='red', linewidth=2, zorder=4)
            else:
                # 在原始坐标系中显示
                ax.scatter(point[0], point[1], color='red', s=200, zorder=5)
                ax.text(point[0], point[1] + 5, f'中心点\n({point[0]:.3f}, {point[1]:.3f})',
                        ha='center', va='bottom', fontsize=12, fontweight='bold')
                
                # 在中心点周围添加醒目的标记
                ax.plot([point[0]-5, point[0]+5], [point[1], point[1]], 
                        color='red', linewidth=2, zorder=4)
                ax.plot([point[0], point[0]], [point[1]-5, point[1]+5], 
                        color='red', linewidth=2, zorder=4)

            # 设置坐标轴和标题
            if is_mechanical:
                calib_config = self.config['coordinate_calibration']
                origin = calib_config['origin_mechanical']
                x_min, y_min = origin[0] - 10, origin[1] - 10
                x_max = origin[0] + self.width + 10
                y_max = origin[1] + self.height + 10
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)
            else:
                ax.set_xlim(self.offset_x - 10, self.offset_x + self.width + 10)
                ax.set_ylim(self.offset_y - 10, self.offset_y + self.height + 10)
            
            ax.set_aspect('equal')
            ax.grid(True)
            ax.set_xlabel('X坐标', fontsize=12)
            ax.set_ylabel('Y坐标', fontsize=12)
            ax.set_title(titles[idx], fontsize=14, fontweight='bold')

        # 确保输出目录存在
        if not os.path.exists('board_test'):
            os.makedirs('board_test')
        plt.savefig(f'board_test/point_{cell_name}.png', dpi=300, bbox_inches='tight')
        plt.close(fig)

    def visualize_board(self, highlight_cells=None):
        """可视化棋盘"""
        # 设置matplotlib支持中文显示
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 创建主图和子图
        if self.calibration_enabled and self.config['coordinate_calibration'].get('visualize_calibration', False):
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 14))
            fig.suptitle('棋盘可视化', fontsize=16)
            axes = [ax1, ax2]
            titles = ['原始棋盘坐标系', '矫正后机械坐标系']
        else:
            fig, ax = plt.subplots(figsize=(10, 14))
            axes = [ax]
            titles = ['棋盘坐标系']

        for idx, ax in enumerate(axes):
            is_mechanical = idx == 1
            
            # 绘制格子
            for row in range(self.grid_height):
                for col in range(self.grid_width):
                    cell_name = f"{chr(65 + col)}{row}"
                    points = self.coordinate_map[cell_name]
                    
                    if is_mechanical:
                        # 转换坐标到机械坐标系
                        mech_points = [self.board_to_mechanical(p) for p in points]
                        x, y = mech_points[0]
                        width = mech_points[1][0] - x
                        height = mech_points[3][1] - y
                        rect = Rectangle((x, y), width, height,
                                        linewidth=1, edgecolor='black', facecolor='none')
                        
                        # 添加格子名称
                        center_x = x + width / 2
                        center_y = y + height / 2
                    else:
                        rect = Rectangle(points[0], self.cell_width, self.cell_height,
                                        linewidth=1, edgecolor='black', facecolor='none')
                        
                        # 添加格子名称
                        center_x = points[0][0] + self.cell_width / 2
                        center_y = points[0][1] + self.cell_height / 2
                    
                    ax.add_patch(rect)
                    ax.text(center_x, center_y, cell_name, ha='center', va='center')

            # 如果指定了要高亮的格子，绘制图形和中心点
            if highlight_cells:
                try:
                    # 获取原始棋盘坐标系中的中心点和边界线
                    _, board_boundary_lines, board_center = self.get_shape_center(highlight_cells, out=False)
                    
                    if is_mechanical:
                        # 在机械坐标系中显示
                        mech_center = self.board_to_mechanical(board_center)
                        
                        # 转换边界线到机械坐标系
                        mech_boundary_lines = []
                        for start, end in board_boundary_lines:
                            mech_start = self.board_to_mechanical(start)
                            mech_end = self.board_to_mechanical(end)
                            mech_boundary_lines.append((mech_start, mech_end))
                            
                        # 绘制图形边框
                        for start, end in mech_boundary_lines:
                            ax.plot([start[0], end[0]], [start[1], end[1]],
                                    color='green', linewidth=4)
                        # 绘制中心点
                        ax.scatter(mech_center[0], mech_center[1], color='red', s=200, zorder=5)
                        ax.text(mech_center[0], mech_center[1] + 5, f'中心点\n({mech_center[0]:.3f}, {mech_center[1]:.3f})',
                                ha='center', va='bottom', fontsize=12, fontweight='bold')
                        
                        # 在中心点周围添加醒目的标记
                        ax.plot([mech_center[0]-5, mech_center[0]+5], [mech_center[1], mech_center[1]], 
                                color='red', linewidth=2, zorder=4)
                        ax.plot([mech_center[0], mech_center[0]], [mech_center[1]-5, mech_center[1]+5], 
                                color='red', linewidth=2, zorder=4)
                    else:
                        # 在原始坐标系中显示
                        # 绘制图形边框
                        for start, end in board_boundary_lines:
                            ax.plot([start[0], end[0]], [start[1], end[1]],
                                    color='green', linewidth=4)
                        # 绘制中心点
                        ax.scatter(board_center[0], board_center[1], color='red', s=200, zorder=5)
                        ax.text(board_center[0], board_center[1] + 5, f'中心点\n({board_center[0]:.3f}, {board_center[1]:.3f})',
                                ha='center', va='bottom', fontsize=12, fontweight='bold')
                        
                        # 在中心点周围添加醒目的标记
                        ax.plot([board_center[0]-5, board_center[0]+5], [board_center[1], board_center[1]], 
                                color='red', linewidth=2, zorder=4)
                        ax.plot([board_center[0], board_center[0]], [board_center[1]-5, board_center[1]+5], 
                                color='red', linewidth=2, zorder=4)
                except ValueError as e:
                    print(f"错误: {e}")

            # 设置坐标轴和标题
            if is_mechanical:
                calib_config = self.config['coordinate_calibration']
                origin = calib_config['origin_mechanical']
                x_min, y_min = origin[0] - 10, origin[1] - 10
                x_max = origin[0] + self.width + 10
                y_max = origin[1] + self.height + 10
                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)
            else:
                ax.set_xlim(self.offset_x - 10, self.offset_x + self.width + 10)
                ax.set_ylim(self.offset_y - 10, self.offset_y + self.height + 10)
            
            ax.set_aspect('equal')
            ax.grid(True)
            ax.set_xlabel('X坐标', fontsize=12)
            ax.set_ylabel('Y坐标', fontsize=12)
            ax.set_title(titles[idx], fontsize=14, fontweight='bold')

        # 确保输出目录存在
        if not os.path.exists('board_test'):
            os.makedirs('board_test')
        plt.savefig(f'board_test/board{self.test_num}.png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        self.test_num += 1

# 使用示例
if __name__ == "__main__":
    # 创建一个棋盘实例，设置X轴偏移量为100
    board = Board()
    
    # 获取四个相邻格子组成的图形的中心点坐标
    try:
        highlight_cells = ['A1', 'A0', 'B0', 'C0']
        center, _ = board.get_shape_center(highlight_cells)
        print(f"图形中心点坐标: {center}")

        if board.debug:
            # 重新可视化，显示高亮的图形
            board.visualize_board(highlight_cells)
    except ValueError as e:
        print(e) 
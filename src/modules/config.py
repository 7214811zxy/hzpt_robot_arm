"""
配置文件
包含所有模块的配置参数
"""

picture_save_path = './test_img/test111.jpg'          # 程序图像保存路径，也是视觉处理图片输入路径
L_shape_offset_number = -5                # L形块中心点往最长边偏移的量（坐标值）


# 拍照模块配置
TAKE_PHOTO_CONFIG = {
    'debug': True,
    'run': True,                         # 是否开启摄像头拍照

    'save_path': picture_save_path,      # 输出目录路径
    'camera_number':1,                  # 摄像头编号

    'time': 2,                           # 摄像机调整时间（秒）
    'exposure': -13                      # 摄像机手动曝光值（慎改，值取决于摄像头型号）
}

# 视觉识别模块配置
VISION_CONFIG = {
    # 调试模式开关
    'debug': True,
    
    # 输入输出路径配置
    'input_path': picture_save_path,      # 输入图像路径
    'output_path': './test_result',       # 输出目录路径

    # 图像处理和坐标系参数
    'target_size': (410, 410),            # 目标图像尺寸，必须是整数
    'scale_factor': 0.7,                  # 图像缩放因子
    
    # 坐标基准点配置
    'origin_offset': {
        'x': 0,                         # 图像原点对应的x轴基准值
        'y': 0,                          # 图像原点对应的y轴基准值
    },

    # L形块偏移设置
    'l_shape_offset': {
        'enabled': True,                  # 是否启用L形块偏移
        'offset': L_shape_offset_number,      # L形块中心点往最长边偏移的量（坐标值）
        'visualize': True,               # 是否在图像中可视化偏移后的点
    },

    # 坐标原点位置配置
    'coordinate_origin': {
        'position': 'bottom_left',           # 坐标原点位置：'top_left', 'top_right', 'bottom_left', 'bottom_right'
        'default_direction': True,        # 是否需要自动设置正方形
        'x_direction': 'right',           # x轴正方向：'right', 'left'（当default_direction为False时使用）
        'y_direction': 'down',            # y轴正方向：'down', 'up'（当default_direction为False时使用）
    },
    
    # 坐标系缩放配置
    'coordinate_scale': {
        'enabled': True,                  # 是否启用坐标系缩放
        'use_target_size': True,          # 是否使用target_size作为缩放目标
        'scale_to_width': 410,            # 缩放到的宽度（当use_target_size为False时使用）
        'scale_to_height': 410,           # 缩放到的高度（当use_target_size为False时使用）
    },
    
    # 轮廓处理参数
    'min_area': 6000,                    # 最小轮廓面积
    'max_area': 12000,                   # 最大轮廓面积
    'min_complexity': 100,                # 最小复杂度
    'max_aspect_ratio': 7,                # 最大宽高比
    
    # 形状识别参数
    'i_shape_ratio': 3.0,                 # I形块宽高比阈值
    'o_shape_ratio': 1.2,                 # O形块宽高比阈值
    'o_shape_area_ratio': 0.9,            # O形块面积比阈值
    'l_shape_min_ratio': 1.4,             # L形块最小宽高比
    'l_shape_max_ratio': 1.6,             # L形块最大宽高比
    'l_shape_min_area_ratio': 0.65,       # L形块最小面积比
    'l_shape_max_area_ratio': 0.75,       # L形块最大面积比
    
    # 形态学操作参数
    'morphology': {
        'median_blur_size': 5,            # 中值滤波核大小（必须为奇数，很神奇）
        'close_kernel_size': (3, 3),      # 闭运算核大小
        'open_kernel_size': (2, 2),       # 开运算核大小
        'close2_kernel_size': (3, 3),     # 第二次闭运算核大小
    },

    # 坐标系矫正配置
    'coordinate_calibration': {
        'enabled': True,                  # 是否启用坐标系矫正
        'origin_mechanical': (-758.298, 297.306),  # 棋盘原点在机械坐标系中的位置 (x, y)
        'x_point_mechanical': (-468.533, 7.756),  # 棋盘x轴上一点在机械坐标系中的位置 (x, y)
        'y_point_mechanical': (-468.741, 585.977),  # 棋盘y轴上一点在机械坐标系中的位置 (x, y)
        'diagonal_point_mechanical': (-177.516, 297.069),  # 棋盘对角顶点在机械坐标系中的位置 (x, y)
        'visualize_calibration': True        # 是否可视化矫正后的坐标系
    }
}

# 棋盘配置模块
BOARD_CONFIG = {
    'debug': False,

    'width': 200,                   # 棋盘总宽度
    'height': 280,                  # 棋盘总高度
    'grid_width': 10,                # 横向格子数
    'grid_height': 14,               # 纵向格子数
    'offset_x': 0,                   # X轴偏移量
    'offset_y': 0,                   # Y轴偏移量
    
    # 坐标系矫正配置
    'coordinate_calibration': {
        'enabled': True,            # 是否启用坐标系矫正
        'origin_mechanical': (-263.301, 485.605),  # 棋盘原点在机械坐标系中的位置 (x, y)
        'x_point_mechanical': (-120.850, 343.122),   # 棋盘x轴上一点在机械坐标系中的位置 (x, y)
        'y_point_mechanical': (-64.740, 685.203),      # 棋盘y轴上一点在机械坐标系中的位置 (x, y)
        'diagonal_point_mechanical': (77.593, 542.661),  # 棋盘对角顶点在机械坐标系中的位置 (x, y)
        'visualize_calibration': True        # 是否可视化矫正后的坐标系
    }
}

PLACE_CONFIG = {

    'order': ['I', 'O', 'L_left', 'L_right', 'T', 'Z_left', 'Z_right']      # 下棋顺序
}

# 队列模块配置
QUEUE_CONFIG = {
    'debug': True,

    'vision_Z': 100,                    # 视觉盘z轴固定值
    'board_Z': 90,                      # 放置盘z轴固定值
    'Rx': -180,                         # Rx固定值
    'Ry': 0,                            # Ry固定值
    'Rz': -90,                          # Rz固定值

    'L_shape_offset': (L_shape_offset_number / 1.41),               # L形块中心点往最长边偏移的量（坐标值）

    'order': 0                              # 抓取顺序，0 1 分别代表顺着y轴 从下往上抓取 或 从上往下抓取

}

# 通讯模块配置
TCP_CONFIG = {
    'debug': True,

    'ip': '192.168.10.200',             # 设置ip
    'port': 2017,                       # 设置端口

}

COM_CONFIG = {
    'port': 'COM4',         # 串口号，Windows通常是COMx，Linux/Mac通常是/dev/ttyxxx
    'baudrate': 9600,       # 波特率
    'timeout': 1            # 超时时间(秒)

}
import numpy as np
'''
计算坐标系矫正矩阵
# origin_mechanical: 机械坐标系原点, 格式为 (x, y)
# x_point_mechanical: 机械坐标系X轴点, 格式为 (x, y)
# y_point_mechanical: 机械坐标系Y轴点, 格式为 (x, y)
# diagonal_point_mechanical: 机械坐标系对角点, 格式为 (x, y)
'''
def calculate_calibration_matrix_test(
    target_size_x, 
    target_size_y, 
    origin_mechanical_point,
    x_point_mechanical_point,
    y_point_mechanical_point,
    diagonal_point_mechanical_point,
    debug=False):

    # 棋盘坐标系中的点（使用缩小后的坐标）
    # 注意：这里的坐标系原点在左上角，x轴向右为正，y轴向下为正
    board_origin = np.array([0, 0, 1])  # 原点（左上角）
    board_x_point = np.array([target_size_x, 0, 1])  # x轴上的点（右上角）
    board_y_point = np.array([0, target_size_y, 1])  # y轴上的点（左下角）
    board_diagonal = np.array([target_size_x, target_size_y, 1])  # 对角点（右下角）

    # 获取机械坐标系中的点
    mech_origin = np.array([origin_mechanical_point[0],
                            origin_mechanical_point[1], 1])
    mech_x_point = np.array([x_point_mechanical_point[0],
                             x_point_mechanical_point[1], 1])
    mech_y_point = np.array([y_point_mechanical_point[0],
                             y_point_mechanical_point[1], 1])
    mech_diagonal = np.array([diagonal_point_mechanical_point[0],
                              diagonal_point_mechanical_point[1], 1])

    # 构建源点和目标点矩阵
    src_points = np.array([board_origin[:2], board_x_point[:2], board_y_point[:2], board_diagonal[:2]])
    dst_points = np.array([mech_origin[:2], mech_x_point[:2], mech_y_point[:2], mech_diagonal[:2]])

    # 使用最小二乘法计算最佳拟合变换矩阵
    # 构建A矩阵
    A = []
    for i in range(len(src_points)):
        x, y = src_points[i]
        u, v = dst_points[i]
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(A)

    # 构建b向量
    b = []
    for i in range(len(src_points)):
        u, v = dst_points[i]
        b.append(u)
        b.append(v)
    b = np.array(b)

    # 求解线性方程组
    h = np.linalg.lstsq(A, b, rcond=None)[0]

    # 构建变换矩阵
    matrix = np.array([
        [h[0], h[1], h[2]],
        [h[3], h[4], h[5]],
        [h[6], h[7], 1]
    ])

    if debug:
        print(f"坐标矫正矩阵:\n{matrix}")

        # 计算变换误差
        transformed_points = []
        for point in src_points:
            homogeneous = np.array([point[0], point[1], 1])
            transformed = np.dot(matrix, homogeneous)
            transformed_points.append(transformed[:2] / transformed[2])

        error = np.mean(np.sqrt(np.sum((transformed_points - dst_points) ** 2, axis=1)))
        print(f"平均变换误差: {error:.3f} 像素")

        # 打印坐标点信息
        print("\n图像坐标系点:")
        print(f"原点(左上角): {board_origin[:2]}")
        print(f"X轴点(右上角): {board_x_point[:2]}")
        print(f"Y轴点(左下角): {board_y_point[:2]}")
        print(f"对角点(右下角): {board_diagonal[:2]}")

        print("\n机械坐标系点:")
        print(f"原点: {mech_origin[:2]}")
        print(f"X轴点: {mech_x_point[:2]}")
        print(f"Y轴点: {mech_y_point[:2]}")
        print(f"对角点: {mech_diagonal[:2]}")

        # 测试一些关键点的转换
        test_points = [
            (0, 0, "原点(左上角)"),
            (target_size_x, 0, "右上角"),
            (0, target_size_y, "左下角"),
            (target_size_x, target_size_y, "右下角"),
            (target_size_x / 2, target_size_y / 2, "中心点")
        ]

        print("\n关键点转换测试:")
        for x, y, name in test_points:
            point = np.array([x, y, 1])
            transformed = np.dot(matrix, point)
            transformed = transformed[:2] / transformed[2]
            print(f"{name}: 图像坐标({x}, {y}) -> 机械坐标({transformed[0]:.3f}, {transformed[1]:.3f})")

    return matrix

if __name__ == "__main__":
    calculate_calibration_matrix_test(
        target_size_x=100,
        target_size_y=100,
        origin_mechanical_point=(0, 0),
        x_point_mechanical_point=(100, 0),
        y_point_mechanical_point=(0, 100),
        diagonal_point_mechanical_point=(100, 100),
        debug=True
    )

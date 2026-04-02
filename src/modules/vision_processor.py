import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import os
from src.modules.config import VISION_CONFIG
from src.modules.matrix_utils import calculate_calibration_matrix_test

class TetrisProcessor:
    def __init__(self, config=None):
        """
        初始化TetrisProcessor类
        :param config: 配置字典，如果为None则使用默认配置
        """
        self.config = config if config is not None else VISION_CONFIG
        self.debug = self.config['debug']
        self.scale_factor = self.config['scale_factor']
        self.target_size = self.config['target_size']
        
        # 初始化坐标系矫正
        self.calibration_enabled = self.config.get('coordinate_calibration', {}).get('enabled', False)
        if self.calibration_enabled:
            # self.calibration_matrix = self._calculate_calibration_matrix()
            self.calibration_matrix = calculate_calibration_matrix_test(
                target_size_x=self.target_size[0],
                target_size_y=self.target_size[1],
                origin_mechanical_point=self.config['coordinate_calibration']['origin_mechanical'],
                x_point_mechanical_point=self.config['coordinate_calibration']['x_point_mechanical'],
                y_point_mechanical_point=self.config['coordinate_calibration']['y_point_mechanical'],
                diagonal_point_mechanical_point=self.config['coordinate_calibration']['diagonal_point_mechanical'],
                debug=self.debug
            )   
            if self.debug:
                print(f"坐标矫正矩阵:\n{self.calibration_matrix}")
                
    # def _calculate_calibration_matrix(self):
    #     """
    #     计算坐标系矫正矩阵
    #     使用棋盘坐标系中的原点和两个轴上的点与它们在机械坐标系中的对应关系
    #     计算一个转换矩阵，用于将棋盘坐标系转换到机械坐标系
    #     原点在左上角，X轴向右为正，Y轴向下为正
    #     """
    #     calib_config = self.config['coordinate_calibration']
    #
    #     # 棋盘坐标系中的点（使用缩小后的坐标）
    #     # 注意：这里的坐标系原点在左上角，x轴向右为正，y轴向下为正
    #     board_origin = np.array([0, 0, 1])  # 原点（左上角）
    #     board_x_point = np.array([self.target_size[0], 0, 1])  # x轴上的点（右上角）
    #     board_y_point = np.array([0, self.target_size[1], 1])  # y轴上的点（左下角）
    #     board_diagonal = np.array([self.target_size[0], self.target_size[1], 1])  # 对角点（右下角）
    #
    #     # 获取机械坐标系中的点
    #     mech_origin = np.array([calib_config['origin_mechanical'][0],
    #                            calib_config['origin_mechanical'][1], 1])
    #     mech_x_point = np.array([calib_config['x_point_mechanical'][0],
    #                             calib_config['x_point_mechanical'][1], 1])
    #     mech_y_point = np.array([calib_config['y_point_mechanical'][0],
    #                             calib_config['y_point_mechanical'][1], 1])
    #     mech_diagonal = np.array([calib_config['diagonal_point_mechanical'][0],
    #                              calib_config['diagonal_point_mechanical'][1], 1])
    #
    #     # 构建源点和目标点矩阵
    #     src_points = np.array([board_origin[:2], board_x_point[:2], board_y_point[:2], board_diagonal[:2]])
    #     dst_points = np.array([mech_origin[:2], mech_x_point[:2], mech_y_point[:2], mech_diagonal[:2]])
    #
    #     # 使用最小二乘法计算最佳拟合变换矩阵
    #     # 构建A矩阵
    #     A = []
    #     for i in range(len(src_points)):
    #         x, y = src_points[i]
    #         u, v = dst_points[i]
    #         A.append([x, y, 1, 0, 0, 0, -u*x, -u*y])
    #         A.append([0, 0, 0, x, y, 1, -v*x, -v*y])
    #     A = np.array(A)
    #
    #     # 构建b向量
    #     b = []
    #     for i in range(len(src_points)):
    #         u, v = dst_points[i]
    #         b.append(u)
    #         b.append(v)
    #     b = np.array(b)
    #
    #     # 求解线性方程组
    #     h = np.linalg.lstsq(A, b, rcond=None)[0]
    #
    #     # 构建变换矩阵
    #     matrix = np.array([
    #         [h[0], h[1], h[2]],
    #         [h[3], h[4], h[5]],
    #         [h[6], h[7], 1]
    #     ])
    #
    #     if self.debug:
    #         print(f"坐标矫正矩阵:\n{matrix}")
    #
    #         # 计算变换误差
    #         transformed_points = []
    #         for point in src_points:
    #             homogeneous = np.array([point[0], point[1], 1])
    #             transformed = np.dot(matrix, homogeneous)
    #             transformed_points.append(transformed[:2] / transformed[2])
    #
    #         error = np.mean(np.sqrt(np.sum((transformed_points - dst_points) ** 2, axis=1)))
    #         print(f"平均变换误差: {error:.3f} 像素")
    #
    #         # 打印坐标点信息
    #         print("\n图像坐标系点:")
    #         print(f"原点(左上角): {board_origin[:2]}")
    #         print(f"X轴点(右上角): {board_x_point[:2]}")
    #         print(f"Y轴点(左下角): {board_y_point[:2]}")
    #         print(f"对角点(右下角): {board_diagonal[:2]}")
    #
    #         print("\n机械坐标系点:")
    #         print(f"原点: {mech_origin[:2]}")
    #         print(f"X轴点: {mech_x_point[:2]}")
    #         print(f"Y轴点: {mech_y_point[:2]}")
    #         print(f"对角点: {mech_diagonal[:2]}")
    #
    #         # 测试一些关键点的转换
    #         test_points = [
    #             (0, 0, "原点(左上角)"),
    #             (self.target_size[0], 0, "右上角"),
    #             (0, self.target_size[1], "左下角"),
    #             (self.target_size[0], self.target_size[1], "右下角"),
    #             (self.target_size[0]/2, self.target_size[1]/2, "中心点")
    #         ]
    #
    #         print("\n关键点转换测试:")
    #         for x, y, name in test_points:
    #             point = np.array([x, y, 1])
    #             transformed = np.dot(matrix, point)
    #             transformed = transformed[:2] / transformed[2]
    #             print(f"{name}: 图像坐标({x}, {y}) -> 机械坐标({transformed[0]:.3f}, {transformed[1]:.3f})")
    #
    #     return matrix
    
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
        
    def _debug_print(self, message):
        """
        调试模式下的打印函数
        :param message: 要打印的消息
        """
        if self.debug:
            print(message)
            
    def _debug_save_image(self, image, filename, output_dir):
        """
        调试模式下保存图像
        :param image: 要保存的图像
        :param filename: 文件名
        :param output_dir: 输出目录
        """
        if self.debug:
            cv2.imwrite(os.path.join(output_dir, filename), image)
            
    def _rectify_contour(self, contour):
        """
        将轮廓的转折角度修正为直角或270度角，同时保持形状特征
        :param contour: 输入轮廓
        :return: 修正后的轮廓
        """
        # 先进行轮廓近似，得到主要转折点
        epsilon = 0.005 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # 如果点数太少，不做处理直接返回
        if len(approx) < 4:
            return contour
            
        # 获取轮廓的最小外接矩形，用来确定主要方向
        rect = cv2.minAreaRect(contour)
        center, (width, height), angle = rect
        
        # 确保width是较长的边
        if width < height:
            width, height = height, width
            angle += 90
            
        # 将角度调整到-45到45度之间
        while angle <= -45:
            angle += 90
        while angle > 45:
            angle -= 90
            
        # 创建旋转矩阵
        M = cv2.getRotationMatrix2D((0, 0), angle, 1.0)
        
        # 旋转点集以使主要边与坐标轴对齐
        rotated_points = cv2.transform(approx, M).reshape(-1, 2)
        
        # 计算旋转后的轮廓边界
        min_x = np.min(rotated_points[:, 0])
        max_x = np.max(rotated_points[:, 0])
        min_y = np.min(rotated_points[:, 1])
        max_y = np.max(rotated_points[:, 1])
        
        # 对点进行聚类，找出应该对齐的点
        x_coords = rotated_points[:, 0]
        y_coords = rotated_points[:, 1]
        
        # 用DBSCAN聚类找出x坐标相近的点
        x_clustering = DBSCAN(eps=3, min_samples=1).fit(x_coords.reshape(-1, 1))
        x_clusters = {}
        for i, label in enumerate(x_clustering.labels_):
            if label not in x_clusters:
                x_clusters[label] = []
            x_clusters[label].append(i)
            
        # 用DBSCAN聚类找出y坐标相近的点
        y_clustering = DBSCAN(eps=3, min_samples=1).fit(y_coords.reshape(-1, 1))
        y_clusters = {}
        for i, label in enumerate(y_clustering.labels_):
            if label not in y_clusters:
                y_clusters[label] = []
            y_clusters[label].append(i)
            
        # 对聚类后的点进行调整，使同一聚类的点具有相同的x或y坐标
        rectified_points = rotated_points.copy()
        
        # 调整x坐标 - 先将点靠近四个主要边
        for cluster_indices in x_clusters.values():
            if len(cluster_indices) > 1:
                avg_x = np.mean(x_coords[cluster_indices])
                # 判断是否靠近左右边界
                if abs(avg_x - min_x) < 10:  # 靠近左边界
                    for idx in cluster_indices:
                        rectified_points[idx, 0] = min_x
                elif abs(avg_x - max_x) < 10:  # 靠近右边界
                    for idx in cluster_indices:
                        rectified_points[idx, 0] = max_x
                else:  # 中间区域的点保持平均值
                    for idx in cluster_indices:
                        rectified_points[idx, 0] = avg_x
                        
        # 调整y坐标 - 先将点靠近四个主要边
        for cluster_indices in y_clusters.values():
            if len(cluster_indices) > 1:
                avg_y = np.mean(y_coords[cluster_indices])
                # 判断是否靠近上下边界
                if abs(avg_y - min_y) < 10:  # 靠近上边界
                    for idx in cluster_indices:
                        rectified_points[idx, 1] = min_y
                elif abs(avg_y - max_y) < 10:  # 靠近下边界
                    for idx in cluster_indices:
                        rectified_points[idx, 1] = max_y
                else:  # 中间区域的点保持平均值
                    for idx in cluster_indices:
                        rectified_points[idx, 1] = avg_y
                        
        # 根据轮廓的几何形状属性调整点
        # 强制所有边都严格垂直或水平
        for i in range(len(rectified_points)):
            next_idx = (i + 1) % len(rectified_points)
            
            current = rectified_points[i]
            next_point = rectified_points[next_idx]
            
            # 计算边的方向向量
            edge_vec = next_point - current
            
            # 如果边长度很短，跳过
            if np.linalg.norm(edge_vec) < 3:
                continue
                
            # 判断边是更接近水平还是垂直
            if abs(edge_vec[0]) > abs(edge_vec[1]):  # 更接近水平
                # 强制水平
                next_point[1] = current[1]
            else:  # 更接近垂直
                # 强制垂直
                next_point[0] = current[0]
                
        # 处理每个角点，调整角度使其更接近90度或270度
        for i in range(len(rectified_points)):
            prev_idx = (i - 1) % len(rectified_points)
            next_idx = (i + 1) % len(rectified_points)
            
            prev = rectified_points[prev_idx]
            current = rectified_points[i]
            next_point = rectified_points[next_idx]
            
            # 计算前后两个向量
            vec_prev = current - prev
            vec_next = next_point - current
            
            # 如果向量太短，跳过
            if np.linalg.norm(vec_prev) < 3 or np.linalg.norm(vec_next) < 3:
                continue
                
            # 标准化向量
            vec_prev_norm = vec_prev / np.linalg.norm(vec_prev)
            vec_next_norm = vec_next / np.linalg.norm(vec_next)
            
            # 计算向量的点积和叉积
            dot_product = np.dot(vec_prev_norm, vec_next_norm)
            cross_product = np.cross(vec_prev_norm, vec_next_norm)
            
            # 计算角度
            angle_rad = np.arccos(np.clip(dot_product, -1.0, 1.0))
            angle_deg = np.degrees(angle_rad)
            
            # 根据角度和叉积调整点
            if 70 < angle_deg < 110:  # 接近90度
                # 根据前后向量的方向调整当前点
                if abs(vec_prev_norm[0]) > abs(vec_prev_norm[1]):  # 前向量更水平
                    # 后向量应该垂直，调整next点
                    next_point[0] = current[0]
                else:  # 前向量更垂直
                    # 后向量应该水平，调整next点
                    next_point[1] = current[1]
            elif cross_product < 0 and 250 < angle_deg < 290:  # 接近270度，是凹角
                # 这种情况通常出现在L形、Z形等块的转折处
                if abs(vec_prev_norm[0]) > abs(vec_prev_norm[1]):  # 前向量更水平
                    # 后向量应该垂直，调整next点
                    next_point[0] = current[0]
                else:  # 前向量更垂直
                    # 后向量应该水平，调整next点
                    next_point[1] = current[1]
                    
        # 最后对全部点的位置做一个小幅度调整，使相邻的点更精确地形成直角
        for _ in range(2):  # 迭代优化2次
            for i in range(len(rectified_points)):
                prev_idx = (i - 1) % len(rectified_points)
                next_idx = (i + 1) % len(rectified_points)
                
                prev = rectified_points[prev_idx]
                current = rectified_points[i]
                next_point = rectified_points[next_idx]
                
                # 判断前边和后边的方向
                dx_prev = abs(current[0] - prev[0])
                dy_prev = abs(current[1] - prev[1])
                
                dx_next = abs(next_point[0] - current[0])
                dy_next = abs(next_point[1] - current[1])
                
                # 根据前后边的方向调整点
                if dx_prev > dy_prev and dx_next < dy_next:  # 前边水平，后边垂直
                    next_point[0] = current[0]  # 垂直对齐
                elif dx_prev < dy_prev and dx_next > dy_next:  # 前边垂直，后边水平
                    next_point[1] = current[1]  # 水平对齐
                    
        # 重新整形为OpenCV轮廓格式
        rectified_points = rectified_points.reshape(-1, 1, 2)
        
        # 创建逆旋转矩阵，将修正后的点变换回原始方向
        M_inv = cv2.getRotationMatrix2D((0, 0), -angle, 1.0)
        
        # 应用逆变换
        rectified_contour = cv2.transform(rectified_points, M_inv)
        
        return rectified_contour 

    def _preprocess(self, image_path, output_dir='.'):
        """
        预处理图像并提取轮廓
        :param image_path: 输入图像路径
        :param output_dir: 输出目录
        :return: 过滤后的轮廓列表
        """
        image = cv2.imread(image_path)
        if image is None:
            self._debug_print(f"错误：无法读取图像 {image_path}")
            return []
            
        self._debug_print("原始图像大小:" + str(image.shape))
        
        # 调整图像大小以标准化处理
        image = cv2.resize(image, None, fx=self.scale_factor, fy=self.scale_factor)
        self._debug_print("缩放后图像大小:" + str(image.shape))
        
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 高斯模糊去噪
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 使用Otsu阈值处理，自动找到最佳阈值
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # 获取形态学操作参数
        morphology_config = self.config.get('morphology', {})
        median_blur_size = morphology_config.get('median_blur_size', 5)
        close_kernel_size = morphology_config.get('close_kernel_size', (3, 3))
        open_kernel_size = morphology_config.get('open_kernel_size', (2, 2))
        close2_kernel_size = morphology_config.get('close2_kernel_size', (3, 3))
        
        # 1. 首先进行中值滤波，去除小的噪点
        median = cv2.medianBlur(binary, median_blur_size)
        
        # 2. 使用较大的核进行闭运算，填充内部空隙
        kernel_close = np.ones(close_kernel_size, np.uint8)
        closed = cv2.morphologyEx(median, cv2.MORPH_CLOSE, kernel_close)
        
        # 3. 使用较小的核进行开运算，去除小的突起
        kernel_open = np.ones(open_kernel_size, np.uint8)
        opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_open)
        
        # 4. 再次进行闭运算，确保边缘平滑
        kernel_close2 = np.ones(close2_kernel_size, np.uint8)
        final = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close2)
        
        # 保存中间处理结果用于调试
        if self.debug:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            self._debug_save_image(binary, f"{base_name}_debug_binary.jpg", output_dir)
            self._debug_save_image(median, f"{base_name}_debug_median.jpg", output_dir)
            self._debug_save_image(closed, f"{base_name}_debug_closed.jpg", output_dir)
            self._debug_save_image(opened, f"{base_name}_debug_opened.jpg", output_dir)
            self._debug_save_image(final, f"{base_name}_debug_final.jpg", output_dir)
        
        # 查找所有轮廓，包括内部轮廓
        contours, hierarchy = cv2.findContours(final, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        self._debug_print("找到的轮廓数量:" + str(len(contours)))
        
        # 过滤轮廓
        filtered_contours = []
        min_area = self.config['min_area']
        max_area = self.config['max_area']
        
        # 绘制所有轮廓用于调试
        if self.debug:
            all_contours_img = image.copy()
            cv2.drawContours(all_contours_img, contours, -1, (0, 255, 0), 2)
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            self._debug_save_image(all_contours_img, f"{base_name}_debug_all_contours.jpg", output_dir)
        
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            
            # 计算轮廓的复杂度（周长的平方/面积）
            complexity = perimeter * perimeter / area if area > 0 else float('inf')
            
            # 计算最小外接矩形
            rect = cv2.minAreaRect(cnt)
            _, (width, height), _ = rect
            aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else float('inf')
            
            self._debug_print(f"轮廓 {i}: 面积={area:.2f}, 复杂度={complexity:.2f}, 宽高比={aspect_ratio:.2f}")
            
            # 过滤条件：面积在合理范围内，复杂度不太高，宽高比合理
            if (min_area < area < max_area and 
                complexity < self.config['min_complexity'] and
                aspect_ratio < self.config['max_aspect_ratio']):
                # 对轮廓进行平滑处理
                epsilon = 0.02 * perimeter
                smoothed_cnt = cv2.approxPolyDP(cnt, epsilon, True)
                
                # 进行角度校正
                rectified_cnt = self._rectify_contour(smoothed_cnt)
                
                filtered_contours.append(rectified_cnt)
                self._debug_print(f"轮廓 {i}: 被接受")
            else:
                self._debug_print(f"轮廓 {i}: 被过滤掉")
        
        self._debug_print("过滤后的轮廓数量:" + str(len(filtered_contours)))
        
        # 绘制过滤后的轮廓用于调试
        if self.debug:
            debug_img = image.copy()
            cv2.drawContours(debug_img, filtered_contours, -1, (0, 255, 0), 2)
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            self._debug_save_image(debug_img, f"{base_name}_debug_contours.jpg", output_dir)
        
        return filtered_contours

    def _determine_shape_type(self, contour):
        """
        直接从轮廓确定方块类型
        :param contour: 输入轮廓
        :return: 方块类型
        """
        # 计算最小外接矩形
        rect = cv2.minAreaRect(contour)
        center, (width, height), angle = rect
        
        # 确保width是较长的边
        if width < height:
            width, height = height, width
        
        aspect_ratio = width / height if height > 0 else 0
        
        # 计算轮廓面积与最小外接矩形面积的比例
        area = cv2.contourArea(contour)
        rect_area = width * height
        area_ratio = area / rect_area if rect_area > 0 else 0
        
        # 计算轮廓复杂度（周长的平方/面积）
        perimeter = cv2.arcLength(contour, True)
        complexity = perimeter * perimeter / area if area > 0 else 0
        
        # 用于绘制调试信息
        self._debug_print(f"宽高比: {aspect_ratio:.2f}, 面积比: {area_ratio:.2f}, 复杂度: {complexity:.2f}")
        
        # 计算凸包和凸缺陷
        hull = cv2.convexHull(contour, returnPoints=False)
        try:
            defects = cv2.convexityDefects(contour, hull)
            defect_count = len(defects) if defects is not None else 0
            
            # 分析凸缺陷的深度和角度
            significant_defects = []
            for i in range(defect_count):
                s, e, f, d = defects[i, 0]
                if d / 256.0 > 5:  # 只计算显著的凸缺陷
                    # 获取凸缺陷的三个点
                    start = tuple(contour[s][0])
                    end = tuple(contour[e][0])
                    far = tuple(contour[f][0])
                    
                    # 计算凹陷角度
                    v1 = np.array(start) - np.array(far)
                    v2 = np.array(end) - np.array(far)
                    angle = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
                    
                    significant_defects.append({
                        'depth': d / 256.0,
                        'angle': angle,
                        'points': (start, end, far)
                    })
            
            self._debug_print(f"显著凸缺陷数量: {len(significant_defects)}")
            
            # 分析凹陷的对称性
            if len(significant_defects) >= 2:
                # 计算凹陷角度的差异
                angles = [d['angle'] for d in significant_defects]
                angle_diff = abs(angles[0] - angles[1])
                
                # 计算凹陷点的对称性
                points1 = significant_defects[0]['points']
                points2 = significant_defects[1]['points']
                
                # 计算中心点
                center_x = sum(p[0] for p in points1 + points2) / 6
                center_y = sum(p[1] for p in points1 + points2) / 6
                
                # 计算对称性得分
                symmetry_score = 0
                for p1, p2 in zip(points1, points2):
                    # 计算点到中心的距离
                    d1 = np.sqrt((p1[0] - center_x)**2 + (p1[1] - center_y)**2)
                    d2 = np.sqrt((p2[0] - center_x)**2 + (p2[1] - center_y)**2)
                    # 计算距离的差异
                    symmetry_score += abs(d1 - d2)
                
                self._debug_print(f"凹陷角度差异: {angle_diff:.2f}度")
                self._debug_print(f"对称性得分: {symmetry_score:.2f}")
                
                # 根据对称性判断是Z形还是T形
                if angle_diff < 20 and symmetry_score < 20:  # Z形块应该更对称
                    return 'Z'
                else:
                    return 'T'
                    
        except Exception as e:
            self._debug_print(f"分析凸缺陷时出错: {str(e)}")
            defect_count = 0
        
        # 四个主要特征
        # 1. 宽高比 (aspect_ratio)
        # 2. 面积比 (area_ratio)
        # 3. 显著凸缺陷数量 (defect_count)
        # 4. 形状复杂度 (complexity)
        
        # 识别I形块
        if aspect_ratio > self.config['i_shape_ratio']:
            return 'I'
        
        # 识别O形块
        if aspect_ratio < self.config['o_shape_ratio'] and area_ratio > self.config['o_shape_area_ratio']:
            return 'O'
        
        # 识别L形块
        # L形块的特点是有一个显著凸缺陷，宽高比接近1.5
        if (self.config['l_shape_min_ratio'] < aspect_ratio < self.config['l_shape_max_ratio'] and 
            self.config['l_shape_min_area_ratio'] < area_ratio < self.config['l_shape_max_area_ratio'] and 
            len(significant_defects) == 1):
            return 'L'
        
        # 基于凸缺陷的简单识别规则
        if len(significant_defects) == 0:
            if aspect_ratio > self.config['i_shape_ratio']:
                return 'I'
            else:
                return 'O'
        elif len(significant_defects) == 1:
            return 'L'
        else:  # len(significant_defects) >= 2
            if aspect_ratio > 1.7:
                return 'Z'
            else:
                return 'T' 

    def _calculate_rotation_angle(self, contour, shape_type):
        """
        计算旋转角度，使最长边与x轴平行，且尽可能靠近x轴
        对于L形块，确保较大凸起部分在最长边上方
        :param contour: 输入轮廓
        :param shape_type: 方块类型
        :return: 旋转角度, 最长边, 最长边的法向量
        """
        # 获取轮廓的所有点
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        points = approx.reshape(-1, 2)
        
        # 找出最长边
        max_length = 0
        longest_edge = None
        longest_edge_points = None
        
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            length = np.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))
            if length > max_length:
                max_length = length
                longest_edge = (p1, p2)
                longest_edge_points = (i, (i + 1) % len(points))
        
        if longest_edge is None:
            self._debug_print("警告：未找到最长边")
            return 0, None, None
        
        # 计算最长边的方向向量
        edge_vector = np.array(longest_edge[1]) - np.array(longest_edge[0])
        edge_length = np.linalg.norm(edge_vector)
        edge_direction = edge_vector / edge_length
        
        # 计算与x轴正方向的夹角（弧度）
        angle_rad = np.arctan2(edge_direction[1], edge_direction[0])
        angle_deg = np.degrees(angle_rad)
        
        # 获取轮廓中心点
        M = cv2.moments(contour)
        if M["m00"] != 0:
            center_x = M["m10"] / M["m00"]
            center_y = M["m01"] / M["m00"]
        else:
            self._debug_print("警告：无法计算中心点")
            return 0, None, None
            
        # 计算最长边的中点
        mid_point = (np.array(longest_edge[0]) + np.array(longest_edge[1])) / 2
        
        # 计算最长边中点到中心点的向量
        center_to_mid = mid_point - np.array([center_x, center_y])
        
        # 将角度调整到0-360度之间
        angle_deg = angle_deg % 360
        
        # 计算最长边的法向量（垂直于最长边的单位向量）
        normal_vector = np.array([-edge_direction[1], edge_direction[0]])
        
        # 对L形块进行特殊处理
        if shape_type == 'L':
            # 计算所有点到最长边的距离
            distances = []
            for point in points:
                # 计算点到直线的距离
                v = point - longest_edge[0]
                dist = abs(np.cross(edge_direction, v))
                distances.append((dist, point))
            
            # 找出距离最长边最远的点（即L形块的凸起部分顶点）
            max_dist_point = max(distances, key=lambda x: x[0])[1]
            
            # 计算该点相对于最长边中点的位置
            relative_pos = max_dist_point - mid_point
            
            # 计算该点在最长边方向上的投影
            projection = np.dot(relative_pos, edge_direction)
            
            # 根据投影和垂直距离确定旋转方向
            cross_product = np.cross(edge_direction, relative_pos)
            
            # 调整角度，使凸起部分在最长边上方
            if cross_product < 0:  # 凸起部分在最长边下方
                angle_deg = (angle_deg + 180) % 360
                # 由于旋转了180度，法向量方向也需要反转
                normal_vector = -normal_vector
        else:
            # 对其他形状的处理保持不变
            # 1. 首先将角度调整到-90到90度之间
            while angle_deg <= -90:
                angle_deg += 180
            while angle_deg > 90:
                angle_deg -= 180
            
            # 2. 如果最长边的中点y坐标大于中心点的y坐标，需要额外旋转180度
            if center_to_mid[1] > 0:
                angle_deg += 180
                # 由于旋转了180度，法向量方向也需要反转
                normal_vector = -normal_vector
            
            # 3. 确保角度在0-360度之间
            angle_deg = angle_deg % 360
        
        self._debug_print(f"最长边长度: {max_length:.2f}")
        self._debug_print(f"最长边方向向量: {edge_direction}")
        self._debug_print(f"最长边法向量: {normal_vector}")
        self._debug_print(f"计算得到的旋转角度: {angle_deg:.2f}度")
        self._debug_print(f"中心点: ({center_x:.3f}, {center_y:.3f})")
        self._debug_print(f"最长边中点: ({mid_point[0]:.2f}, {mid_point[1]:.2f})")
        
        return angle_deg, longest_edge, normal_vector

    def _transform_coordinates(self, cx, cy, width, height, origin_position, default_direction, coordinate_origin):
        """
        根据配置的坐标原点位置和坐标轴方向转换坐标
        :param cx: 原始x坐标
        :param cy: 原始y坐标
        :param width: 图像宽度
        :param height: 图像高度
        :param origin_position: 坐标原点位置 ('top_left', 'top_right', 'bottom_left', 'bottom_right')
        :param default_direction: 是否需要自动设置正方形
        :param coordinate_origin: 坐标原点配置字典
        :return: 转换后的坐标 (transformed_cx, transformed_cy)
        """
        transformed_cx = cx
        transformed_cy = cy

        if default_direction:
            if origin_position == 'top_left':
                x_direction = 'right'
                y_direction = 'down'

            if origin_position == 'top_right':
                x_direction = 'left'
                y_direction = 'down'

            if origin_position == 'bottom_left':
                x_direction = 'right'
                y_direction = 'up'

            if origin_position == 'bottom_right':
                x_direction = 'left'
                y_direction = 'up'
        else:
            x_direction = coordinate_origin['x_direction']
            y_direction = coordinate_origin['y_direction']

        # 根据原点位置映射坐标
        if origin_position == 'top_left':
            # 不需要变换
            pass
        elif origin_position == 'top_right':
            # 原点在右上角，x坐标需要反转
            transformed_cx = width - cx
        elif origin_position == 'bottom_left':
            # 原点在左下角，y坐标需要反转
            transformed_cy = height - cy
        elif origin_position == 'bottom_right':
            # 原点在右下角，x和y坐标都需要反转
            transformed_cx = width - cx
            transformed_cy = height - cy
        
        # 根据坐标轴方向映射坐标
        if x_direction == 'left':
            # x轴正方向朝左，需要反转x坐标
            if origin_position in ['top_left', 'bottom_left']:
                transformed_cx = width - transformed_cx
            else:  # top_right, bottom_right
                transformed_cx = transformed_cx
        
        if y_direction == 'up':
            # y轴正方向朝上，需要反转y坐标
            if origin_position in ['top_left', 'top_right']:
                transformed_cy = height - transformed_cy
            else:  # bottom_left, bottom_right
                transformed_cy = transformed_cy
        
        self._debug_print(f"原始坐标: ({cx}, {cy}) -> 转换后坐标: ({transformed_cx:.3f}, {transformed_cy:.3f})")
        self._debug_print(f"坐标原点: {origin_position}, X轴方向: {x_direction}, Y轴方向: {y_direction}")
        
        return transformed_cx, transformed_cy

    def _find_and_rectify_brightest_area(self, image_path, output_dir='.'):
        """
        查找图像中最亮的区域并将其校正为矩形
        :param image_path: 输入图像路径
        :param output_dir: 输出目录
        :return: 处理结果字典
        """
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            self._debug_print(f"错误：无法读取图像 {image_path}")
            return None
            
        # 调整图像大小
        image = cv2.resize(image, None, fx=self.scale_factor, fy=self.scale_factor)
        self._debug_print("缩放后图像大小:" + str(image.shape))
        
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 使用自适应阈值处理找到亮区域
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 151, -20)
        
        # 形态学操作，去除噪点并连接区域
        kernel = np.ones((5,5), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # 查找轮廓
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            self._debug_print("未找到任何轮廓")
            return None
        
        # 找到最大的轮廓（假设这是游戏区域）
        max_area = 0
        max_contour = None
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            self._debug_print(f"发现轮廓，面积: {area}")
            if area > max_area:
                max_area = area
                max_contour = cnt
        
        if max_contour is None:
            self._debug_print("未找到足够大的轮廓")
            return None
        
        self._debug_print(f"最大轮廓面积: {max_area}")
        
        # 对轮廓进行多边形逼近，找到四个顶点
        epsilon = 0.02 * cv2.arcLength(max_contour, True)
        approx = cv2.approxPolyDP(max_contour, epsilon, True)
        
        self._debug_print(f"初始逼近顶点数: {len(approx)}")
        
        # 确保有4个顶点
        if len(approx) != 4:
            self._debug_print(f"警告：轮廓不是四边形（顶点数：{len(approx)}）")
            # 如果顶点数不是4，尝试调整epsilon值
            epsilon = 0.1 * cv2.arcLength(max_contour, True)
            approx = cv2.approxPolyDP(max_contour, epsilon, True)
            self._debug_print(f"调整后顶点数: {len(approx)}")
            if len(approx) != 4:
                self._debug_print(f"无法找到四个顶点，当前顶点数：{len(approx)}")
                return None
        
        # 获取四个顶点并按照左上、右上、右下、左下的顺序排序
        vertices = approx.reshape(-1, 2)
        
        # 计算重心
        center_x = np.mean(vertices[:, 0])
        center_y = np.mean(vertices[:, 1])
        
        # 按照象限排序顶点
        sorted_vertices = []
        for quad in [(True, True), (False, True), (False, False), (True, False)]:  # 左上、右上、右下、左下
            quad_vertices = []
            for vertex in vertices:
                if (vertex[0] < center_x) == quad[0] and (vertex[1] < center_y) == quad[1]:
                    quad_vertices.append(vertex)
            if quad_vertices:
                sorted_vertices.append(quad_vertices[0])
        
        if len(sorted_vertices) != 4:
            self._debug_print("无法正确排序顶点")
            return None
        
        vertices = np.array(sorted_vertices)
        
        # 创建目标点（使用指定的目标尺寸）
        dst_points = np.array([
            [0, 0],                          # 左上
            [self.target_size[0] - 1, 0],         # 右上
            [self.target_size[0] - 1, self.target_size[1] - 1], # 右下
            [0, self.target_size[1] - 1]          # 左下
        ], dtype=np.float32)
        
        # 计算透视变换矩阵
        M = cv2.getPerspectiveTransform(vertices.astype(np.float32), dst_points)
        
        # 返回处理结果
        return {
            'vertices': vertices,
            'perspective_matrix': M,
            'target_size': self.target_size,
            'scale_factor': self.scale_factor
        }

    def process_image(self, image_path = VISION_CONFIG['input_path'], output_dir = VISION_CONFIG['output_path'], target_size=VISION_CONFIG['target_size']):
        """
        处理图像的主方法
        :param image_path: 输入图像路径
        :param output_dir: 输出目录
        :param target_size: 目标尺寸
        :return: 统计字典和结果数组
        """
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        self._debug_print(f"开始处理图像: {image_path}")
        
        # 获取坐标基准点
        origin_x = self.config['origin_offset']['x']
        origin_y = self.config['origin_offset']['y']
        self._debug_print(f"使用坐标基准点: ({origin_x}, {origin_y})")
        
        # 获取L形块偏移设置
        l_shape_offset_config = self.config.get('l_shape_offset', {'enabled': False, 'offset': 0, 'visualize': False})
        l_shape_offset_enabled = l_shape_offset_config.get('enabled', False)
        l_shape_offset = l_shape_offset_config.get('offset', 0)
        l_shape_visualize = l_shape_offset_config.get('visualize', False)
        self._debug_print(f"L形块偏移: {'启用' if l_shape_offset_enabled else '禁用'}, 偏移量: {l_shape_offset}")
        
        # 获取坐标系缩放配置
        coordinate_scale = self.config['coordinate_scale']
        use_coord_scale = coordinate_scale['enabled']
        
        # 获取坐标原点位置配置
        coord_origin = self.config['coordinate_origin']
        origin_position = coord_origin['position']
        default_direction = coord_origin['default_direction']
        if default_direction:
            if origin_position == 'top_left':
                x_direction = 'right'
                y_direction = 'down'

            if origin_position == 'top_right':
                x_direction = 'left'
                y_direction = 'down'

            if origin_position == 'bottom_left':
                x_direction = 'right'
                y_direction = 'up'

            if origin_position == 'bottom_right':
                x_direction = 'left'
                y_direction = 'up'
        else:
            x_direction = coord_origin['x_direction']
            y_direction = coord_origin['y_direction']

        
        self._debug_print(f"坐标原点位置: {origin_position}")
        self._debug_print(f"X轴正方向: {x_direction}")
        self._debug_print(f"Y轴正方向: {y_direction}")
        
        # 如果设置使用target_size作为缩放目标，则使用target_size的值
        if use_coord_scale and coordinate_scale['use_target_size']:
            scale_width = target_size[0]
            scale_height = target_size[1]
            self._debug_print(f"坐标系缩放: 启用, 使用target_size: {scale_width}x{scale_height}")
        else:
            scale_width = coordinate_scale['scale_to_width']
            scale_height = coordinate_scale['scale_to_height']
            self._debug_print(f"坐标系缩放: {'启用' if use_coord_scale else '禁用'}, 目标尺寸: {scale_width}x{scale_height}")
        
        # 首先获取并处理最亮区域
        brightest_area_result = self._find_and_rectify_brightest_area(image_path, output_dir)
        if not brightest_area_result:
            self._debug_print("无法处理最亮区域，终止处理")
            return None, None, None
        
        # 读取图像并预处理
        image = cv2.imread(image_path)
        if image is None:
            self._debug_print(f"错误：无法读取图像 {image_path}")
            return None, None, None
        
        # 使用相同的缩放因子
        scale_factor = brightest_area_result['scale_factor']
        image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
        
        # 获取图像实际尺寸
        img_height, img_width = image.shape[:2]
        self._debug_print(f"图像实际尺寸: {img_width}x{img_height}")
        
        # 处理原始图像中的方块
        contours = self._preprocess(image_path, output_dir)
        
        if not contours:
            self._debug_print(f"未找到有效轮廓，处理终止")
            return None, None, None
        
        # 创建统计字典和结果数组
        stats = {
            'I': {'count': 0, 'blocks': []},
            'L_left': {'count': 0, 'blocks': []},
            'L_right': {'count': 0, 'blocks': []},
            'O': {'count': 0, 'blocks': []},
            'T': {'count': 0, 'blocks': []},
            'Z_left': {'count': 0, 'blocks': []},
            'Z_right': {'count': 0, 'blocks': []}
        }
        
        results = []
        for i, cnt in enumerate(contours):
            try:
                self._debug_print(f"\n----- 处理方块 {i} -----")
                shape_type = self._determine_shape_type(cnt)
                angle, longest_edge, normal_vector = self._calculate_rotation_angle(cnt, shape_type)
                
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    # 计算中心点坐标
                    cx_raw = M["m10"] / M["m00"]
                    cy_raw = M["m01"] / M["m00"]
                    
                    # 计算L形块的偏移中心点（如果需要）
                    if l_shape_offset_enabled and shape_type == 'L' and normal_vector is not None:
                        # 原始中心点
                        original_center = np.array([cx_raw, cy_raw])
                        # 计算偏移方向：沿着最长边法向量方向偏移
                        offset_vector = normal_vector * l_shape_offset
                        # 计算偏移后的中心点
                        offset_center = original_center + offset_vector
                        self._debug_print(f"L形块偏移: 原始中心点=({cx_raw:.3f}, {cy_raw:.3f}), 偏移后中心点=({offset_center[0]:.3f}, {offset_center[1]:.3f})")
                        # 更新中心点坐标为偏移后的坐标
                        cx_raw, cy_raw = offset_center
                    
                    # 应用坐标系缩放
                    if use_coord_scale:
                        # 使用target_size作为缩放目标
                        target_width, target_height = self.target_size
                        # 将坐标从图像尺寸映射到目标尺寸，确保从0开始
                        cx_scaled = cx_raw * target_width / img_width
                        cy_scaled = cy_raw * target_height / img_height
                    else:
                        cx_scaled = cx_raw
                        cy_scaled = cy_raw
                    
                    # 应用基准点偏移获取最终坐标
                    cx = cx_scaled + origin_x
                    cy = cy_scaled + origin_y
                    
                    # 确保坐标在有效范围内
                    cx = max(0, min(cx, scale_width))
                    cy = max(0, min(cy, scale_height))
                else:
                    cx_raw = 0
                    cy_raw = 0
                    cx_scaled = 0
                    cy_scaled = 0
                    cx = origin_x
                    cy = origin_y
                
                # 保存透视变换后方块的中心点坐标
                result = {
                    'shape': shape_type,
                    'angle': angle,
                    'coords': (cx, cy),  # 使用应用了基准点偏移和缩放的坐标
                    'raw_coords': (cx_raw, cy_raw),  # 保存原始坐标
                    'scaled_coords': (cx_scaled, cy_scaled),  # 保存缩放后但未偏移的坐标
                    'contour': cnt,
                    'center_coords': (cx, cy),  # 使用校准后的中心点坐标
                    'normal_vector': normal_vector  # 保存最长边的法向量
                }
                
                # 添加L形块的偏移信息
                if l_shape_offset_enabled and shape_type == 'L':
                    result['is_offset'] = True
                    M_original = cv2.moments(cnt)
                    if M_original["m00"] != 0:
                        original_cx = M_original["m10"] / M_original["m00"]
                        original_cy = M_original["m01"] / M_original["m00"]
                        result['original_center'] = (original_cx, original_cy)
                
                # 应用origin_offset偏移量获取最终中心点坐标
                origin_x = self.config['origin_offset']['x']
                origin_y = self.config['origin_offset']['y']
                adjusted_cx = cx + origin_x
                adjusted_cy = cy + origin_y
                result['adjusted_center_coords'] = (adjusted_cx, adjusted_cy)
                
                # 如果启用了坐标系矫正，转换到机械坐标系
                if self.calibration_enabled:
                    mechanical_coords = self.board_to_mechanical((cx, cy))
                    result['mechanical_coords'] = mechanical_coords
                    self._debug_print(f"矫正后的机械坐标: {mechanical_coords}")
                
                # 将临时结果添加到results数组
                results.append(result)
                
                self._debug_print(f"方块 {i}: 类型={shape_type}, 需顺时针旋转={angle:.0f}度, 坐标={cx, cy}")
                self._debug_print(f"原始坐标: {cx_raw, cy_raw}, 缩放后坐标: {cx_scaled, cy_scaled}")
            except Exception as e:
                self._debug_print(f"处理方块 {i} 时出错: {str(e)}")
                import traceback
                self._debug_print(traceback.format_exc())
        
        # 创建输出路径
        if self.debug:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            result_path = os.path.join(output_dir, f"{base_name}_result.jpg")
            warped_path = os.path.join(output_dir, f"{base_name}_rectify.jpg")
            rotated_path = os.path.join(output_dir, f"{base_name}_rotated.jpg")
            # 为矫正后的图像添加新路径
            calibrated_rectify_path = os.path.join(output_dir, f"{base_name}_calibrated_rectify.jpg")
            calibrated_rotated_path = os.path.join(output_dir, f"{base_name}_calibrated_rotated.jpg")
        
        # 在result图像上绘制结果，包括黄色边框
        result_img = image.copy()
        # 绘制黄色边框
        cv2.drawContours(result_img, [brightest_area_result['vertices'].astype(np.int32)], 0, (0, 255, 255), 2)
        # 绘制方块轮廓和信息
        for i, result in enumerate(results):
            cv2.drawContours(result_img, [result['contour']], 0, (0, 255, 0), 2)
            points = result['contour'].reshape(-1, 2)
            max_length = 0
            longest_edge = None
            for j in range(len(points)):
                p1 = points[j]
                p2 = points[(j + 1) % len(points)]
                length = np.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))
                if length > max_length:
                    max_length = length
                    longest_edge = (p1, p2)
            if longest_edge is not None:
                cv2.line(result_img, tuple(longest_edge[0].astype(int)), 
                        tuple(longest_edge[1].astype(int)), (0, 0, 255), 2)
            
            # 绘制中心点（红色圆点）
            M = cv2.moments(result['contour'])
            if M["m00"] != 0:
                cx = M["m10"] / M["m00"]
                cy = M["m01"] / M["m00"]
                cv2.circle(result_img, (int(cx), int(cy)), 4, (0, 0, 255), -1)  # 红色实心圆
                
                # 如果是L形块且启用了偏移，绘制偏移后的中心点（蓝色圆点）
                if result.get('shape') == 'L' and l_shape_offset_enabled and l_shape_visualize:
                    offset_cx, offset_cy = result.get('raw_coords', (cx, cy))
                    cv2.circle(result_img, (int(offset_cx), int(offset_cy)), 4, (255, 0, 0), -1)  # 蓝色实心圆
                    # 绘制一条从原始中心点到偏移后中心点的线
                    if 'original_center' in result:
                        orig_cx, orig_cy = result['original_center']
                        cv2.line(result_img, (int(orig_cx), int(orig_cy)), (int(offset_cx), int(offset_cy)), (255, 255, 0), 2)
        
        # 从result图像中截取并校正亮区域
        warped = cv2.warpPerspective(result_img, brightest_area_result['perspective_matrix'], 
                                    brightest_area_result['target_size'])
        
        # 创建仅包含旋转计算结果的图像
        h, w = warped.shape[:2]
        rotated_img = np.ones((h, w, 3), dtype=np.uint8) * 255
        info_layer = np.zeros_like(rotated_img)  # 创建信息层
        
        # 创建校准后的矫正图像和旋转图像
        calibrated_rectify = warped.copy() if self.calibration_enabled else None
        calibrated_rotated = np.ones((h, w, 3), dtype=np.uint8) * 255 if self.calibration_enabled else None
        
        # 对每个方块进行透视变换和旋转
        for result in results:
            try:
                # 对轮廓进行透视变换
                cnt = result['contour']
                cnt_transformed = cv2.perspectiveTransform(
                    cnt.reshape(-1, 1, 2).astype(np.float32),
                    brightest_area_result['perspective_matrix']
                )
                
                # 计算轮廓的中心点和边界框
                M = cv2.moments(cnt_transformed)
                rect = cv2.boundingRect(cnt_transformed.astype(np.int32))
                x, y, bw, bh = rect
                
                if M["m00"] != 0:
                    cx = M["m10"] / M["m00"]
                    cy = M["m01"] / M["m00"]
                    # 处理L形块的中心点偏移
                    if l_shape_offset_enabled and result.get('shape') == 'L' and 'normal_vector' in result:
                        # 保存原始中心点
                        original_cx, original_cy = cx, cy
                        # 计算偏移后的中心点
                        normal_vector = result['normal_vector']
                        offset_vector = normal_vector * l_shape_offset
                        cx += offset_vector[0]
                        cy += offset_vector[1]
                        # 在校正图像中标记出原始中心点和偏移后的中心点
                        if l_shape_visualize:
                            # 绘制原始中心点（红色）
                            cv2.circle(warped, (int(original_cx), int(original_cy)), 4, (0, 0, 255), -1)
                            # 绘制偏移后的中心点（蓝色）
                            cv2.circle(warped, (int(cx), int(cy)), 4, (255, 0, 0), -1)
                            # 绘制一条从原始中心点到偏移后中心点的线（绿色）
                            cv2.line(warped, (int(original_cx), int(original_cy)), (int(cx), int(cy)), (0, 255, 0), 2)
                else:
                    cx = x + bw/2
                    cy = y + bh/2
                
                # 保存透视变换后方块的中心点坐标
                result['center_coords'] = (cx, cy)
                
                # 基于配置的坐标原点位置调整坐标
                transformed_cx, transformed_cy = self._transform_coordinates(
                    cx, cy, w, h, 
                    origin_position,
                    default_direction,
                    coord_origin
                )
                
                # 应用origin_offset偏移量获取最终中心点坐标
                origin_x = self.config['origin_offset']['x']
                origin_y = self.config['origin_offset']['y']
                adjusted_cx = transformed_cx + origin_x
                adjusted_cy = transformed_cy + origin_y
                result['adjusted_center_coords'] = (adjusted_cx, adjusted_cy)
                
                # 如果启用了坐标矫正，转换到机械坐标系
                mechanical_cx, mechanical_cy = None, None
                if self.calibration_enabled:
                    mechanical_coords = self.board_to_mechanical((transformed_cx, transformed_cy))
                    mechanical_cx, mechanical_cy = mechanical_coords
                    result['mechanical_coords'] = mechanical_coords
                    self._debug_print(f"方块 {result.get('shape', 'unknown')}: 机械坐标系坐标 = ({mechanical_cx:.3f}, {mechanical_cy:.3f})")
                
                # 创建掩码
                mask = np.zeros((h, w), dtype=np.uint8)
                cv2.drawContours(mask, [cnt_transformed.astype(np.int32)], 0, 255, -1)
                
                # 扩大边界框以确保旋转后不会裁剪
                padding = max(bw, bh)
                x1 = int(max(0, cx - padding))
                y1 = int(max(0, cy - padding))
                x2 = int(min(w, cx + padding))
                y2 = int(min(h, cy + padding))
                
                # 提取方块区域
                block = warped[y1:y2, x1:x2].copy()
                block_mask = mask[y1:y2, x1:x2].copy()
                
                # 计算局部坐标系中的旋转中心
                local_cx = int(cx - x1)
                local_cy = int(cy - y1)
                
                # 计算旋转矩阵 - 以局部坐标系中的中心点为旋转中心
                M_rot = cv2.getRotationMatrix2D((local_cx, local_cy), result['angle'], 1.0)
                
                # 计算旋转后的图像大小，确保足够大以容纳完整的旋转图像
                cos = abs(M_rot[0, 0])
                sin = abs(M_rot[0, 1])
                new_w = int((block.shape[1] * cos) + (block.shape[0] * sin))
                new_h = int((block.shape[1] * sin) + (block.shape[0] * cos))
                
                # 调整旋转矩阵，使旋转后的图像居中
                M_rot[0, 2] += (new_w / 2) - local_cx
                M_rot[1, 2] += (new_h / 2) - local_cy
                
                # 旋转图像和掩码
                rotated_block = cv2.warpAffine(block, M_rot, (new_w, new_h))
                rotated_mask = cv2.warpAffine(block_mask, M_rot, (new_w, new_h))
                
                # 应用掩码
                rotated_block[rotated_mask == 0] = 0
                
                # 计算旋转后图像的中心点（保留浮点数精度）
                rotated_center_x = new_w / 2
                rotated_center_y = new_h / 2
                
                # 为切片操作创建整数索引
                rotated_center_x_int = int(rotated_center_x)
                rotated_center_y_int = int(rotated_center_y)
                
                # 计算粘贴位置（以方块中心为基准）
                paste_x = cx - rotated_center_x
                paste_y = cy - rotated_center_y
                
                # 计算粘贴区域在旋转图像中的有效范围（对于图像操作使用整数）
                valid_x = int(max(0, paste_x))
                valid_y = int(max(0, paste_y))
                valid_w = int(min(new_w, w - valid_x)) if valid_x < w else 0
                valid_h = int(min(new_h, h - valid_y)) if valid_y < h else 0
                
                # 检查是否有可见部分
                if valid_w > 0 and valid_h > 0:
                    # 计算在rotated_block中的对应区域
                    block_x = int(valid_x - paste_x) if paste_x < 0 else 0
                    block_y = int(valid_y - paste_y) if paste_y < 0 else 0
                    
                    # 确保不会超出rotated_block的边界
                    block_w = int(min(valid_w, rotated_block.shape[1] - block_x))
                    block_h = int(min(valid_h, rotated_block.shape[0] - block_y))
                    
                    # 将旋转后的方块放入对应位置（底层）
                    for c in range(3):
                        if block_x >= 0 and block_y >= 0:  # 确保索引有效
                            rotated_img[valid_y:valid_y+block_h, valid_x:valid_x+block_w, c] = \
                                np.where(rotated_mask[block_y:block_y+block_h, block_x:block_x+block_w] > 0,
                                        rotated_block[block_y:block_y+block_h, block_x:block_x+block_w, c],
                                        rotated_img[valid_y:valid_y+block_h, valid_x:valid_x+block_w, c])
                
                # 根据形状类型进行细分
                original_shape = result['shape']  # 保存原始形状类型
                if result['shape'] == 'L':
                    # 计算左右两边的面积（使用整数索引）
                    left_area = np.sum(rotated_mask[:, :rotated_center_x_int])
                    right_area = np.sum(rotated_mask[:, rotated_center_x_int:])
                    
                    # 根据面积判断是L_left还是L_right
                    if left_area > right_area:
                        result['shape'] = 'L_left'
                    else:
                        result['shape'] = 'L_right'
                elif result['shape'] == 'Z':
                    # 计算四个象限的面积（使用整数索引）
                    top_left = np.sum(rotated_mask[:rotated_center_y_int, :rotated_center_x_int])
                    top_right = np.sum(rotated_mask[:rotated_center_y_int, rotated_center_x_int:])
                    bottom_left = np.sum(rotated_mask[rotated_center_y_int:, :rotated_center_x_int])
                    bottom_right = np.sum(rotated_mask[rotated_center_y_int:, rotated_center_x_int:])
                    
                    # 计算左上+右下和左下+右上的面积
                    diagonal1 = top_left + bottom_right
                    diagonal2 = bottom_left + top_right
                    
                    # 根据面积判断是Z_left还是Z_right
                    if diagonal1 > diagonal2:
                        result['shape'] = 'Z_left'
                    else:
                        result['shape'] = 'Z_right'
                
                # 更新统计信息
                # 添加到细分后的形状类型中
                stats[result['shape']]['count'] += 1
                result['number'] = stats[result['shape']]['count']  # 使用细分类型的独立编号
                
                # 创建用于统计输出的块信息
                # 如果启用了坐标系矫正，使用机械坐标；否则使用校准后方块的中心点坐标
                if self.calibration_enabled:
                    block_info = {
                        'number': result['number'],
                        'angle': round(result['angle']),
                        'coords': result['mechanical_coords']  # 使用机械坐标系中的坐标
                    }
                else:
                    block_info = {
                        'number': result['number'],
                        'angle': round(result['angle']),
                        'coords': result['adjusted_center_coords']  # 使用偏移后的中心点坐标
                    }
                
                stats[result['shape']]['blocks'].append(block_info)
                
                # 添加方块信息，使用中心点坐标
                text_type = f"{result['shape']}-{result['number']}"
                text_angle = f"Angle: {int(result['angle'])}"
                
                # 根据是否启用坐标系矫正决定显示哪个坐标
                if self.calibration_enabled:
                    coords_to_display = result['mechanical_coords']
                    text_coord = f"Mech: ({coords_to_display[0]:.3f}, {coords_to_display[1]:.3f})"
                else:
                    coords_to_display = result['adjusted_center_coords']
                    text_coord = f"Img: ({coords_to_display[0]:.3f}, {coords_to_display[1]:.3f})"
                
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                thickness = 1
                
                # 计算文本大小
                text_size_type, _ = cv2.getTextSize(text_type, font, font_scale, thickness)
                text_size_angle, _ = cv2.getTextSize(text_angle, font, font_scale, thickness)
                text_size_coord, _ = cv2.getTextSize(text_coord, font, font_scale, thickness)
                
                # 计算信息框的总宽度和高度
                info_width = max(text_size_type[0], text_size_angle[0], text_size_coord[0]) + 10
                info_height = 45  # 固定高度
                
                # 计算信息框位置（以方块中心为基准）
                pos_x = int(cx - info_width / 2)
                pos_y = int(cy - info_height / 2)
                
                # 确保不超出图像边界
                pos_x = max(0, min(pos_x, w - info_width))
                pos_y = max(0, min(pos_y, h - info_height))
                
                # 在信息层上绘制半透明背景
                cv2.rectangle(info_layer, 
                            (pos_x, pos_y),
                            (pos_x + info_width, pos_y + info_height),
                            (255, 255, 255), -1)
                
                # 在信息层上绘制文本
                cv2.putText(info_layer, text_type,
                          (pos_x + 5, pos_y + 15),
                          font, font_scale, (0, 0, 255), thickness)
                cv2.putText(info_layer, text_angle,
                          (pos_x + 5, pos_y + 30),
                          font, font_scale, (0, 0, 255), thickness)
                cv2.putText(info_layer, text_coord,
                          (pos_x + 5, pos_y + 45),
                          font, font_scale, (0, 0, 255), thickness)
                
                # 如果启用了坐标矫正，也在校准后的图像上绘制信息
                if self.calibration_enabled:
                    # 在校准后的矫正图像上绘制轮廓
                    cv2.drawContours(calibrated_rectify, [cnt_transformed.astype(np.int32)], 0, (0, 255, 0), 2)
                    
                    # 绘制矫正后的中心点和坐标文本
                    # 使用偏移后的坐标点（如果是L形块）
                    if result.get('shape') == 'L' and l_shape_offset_enabled:
                        display_cx, display_cy = result.get('raw_coords', (cx, cy))
                    else:
                        display_cx, display_cy = cx, cy
                    cv2.circle(calibrated_rectify, (int(display_cx), int(display_cy)), 4, (0, 0, 255), -1)
                    
                    # 机械坐标系中的坐标
                    mechanical_cx, mechanical_cy = result['mechanical_coords']
                    
                    # 使用更小的字体大小和更薄的线条
                    small_font_scale = 0.4  # 更小的字体大小
                    small_thickness = 1  # 更细的线条
                    
                    # 计算文本大小
                    text_size_type, _ = cv2.getTextSize(text_type, font, small_font_scale, small_thickness)
                    text_size_angle, _ = cv2.getTextSize(text_angle, font, small_font_scale, small_thickness)
                    text_size_mech, _ = cv2.getTextSize(f"M: ({mechanical_cx:.2f}, {mechanical_cy:.2f})", font, small_font_scale, small_thickness)
                    
                    # 计算信息框的总宽度和高度
                    small_info_width = max(text_size_type[0], text_size_angle[0], text_size_mech[0]) + 5
                    small_info_height = 35  # 更小的高度
                    
                    # 计算信息框位置（以方块中心为基准）
                    small_pos_x = int(cx - small_info_width / 2)
                    small_pos_y = int(cy - small_info_height / 2)
                    
                    # 确保不超出图像边界
                    small_pos_x = max(0, min(small_pos_x, w - small_info_width))
                    small_pos_y = max(0, min(small_pos_y, h - small_info_height))
                    
                    # 直接绘制文本，不使用背景矩形
                    cv2.putText(calibrated_rectify, text_type,
                              (small_pos_x, small_pos_y + 10),
                              font, small_font_scale, (0, 0, 255), small_thickness)
                    cv2.putText(calibrated_rectify, text_angle,
                              (small_pos_x, small_pos_y + 22),
                              font, small_font_scale, (0, 0, 255), small_thickness)
                    cv2.putText(calibrated_rectify, f"M: ({mechanical_cx:.2f}, {mechanical_cy:.2f})",
                              (small_pos_x, small_pos_y + 34),
                              font, small_font_scale, (0, 0, 255), small_thickness)
                    
                    # 将旋转后的方块也放入校准后的旋转图像中
                    if valid_w > 0 and valid_h > 0:
                        for c in range(3):
                            if block_x >= 0 and block_y >= 0:  # 确保索引有效
                                calibrated_rotated[valid_y:valid_y+block_h, valid_x:valid_x+block_w, c] = \
                                    np.where(rotated_mask[block_y:block_y+block_h, block_x:block_x+block_w] > 0,
                                            rotated_block[block_y:block_y+block_h, block_x:block_x+block_w, c],
                                            calibrated_rotated[valid_y:valid_y+block_h, valid_x:valid_x+block_w, c])
                
            except Exception as e:
                self._debug_print(f"处理旋转方块时出错: {str(e)}")
                continue
        
        # 将信息层叠加到旋转图像上（使用alpha混合）
        alpha = 0.7
        # 创建三通道的mask
        mask = np.any(info_layer > 0, axis=2).astype(float)
        mask = np.expand_dims(mask, axis=2)
        mask = np.repeat(mask, 3, axis=2)
        
        # 应用alpha混合
        rotated_img = (rotated_img * (1 - mask * alpha) + info_layer * alpha).astype(np.uint8)
        
        # 添加标题
        cv2.putText(rotated_img, "Rotated", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # 在图像绘制坐标系
        # 根据配置确定坐标原点位置
        if origin_position == 'top_left':
            origin_draw_x, origin_draw_y = 50, 50
        elif origin_position == 'top_right':
            origin_draw_x, origin_draw_y = w - 50, 50
        elif origin_position == 'bottom_left':
            origin_draw_x, origin_draw_y = 50, h - 50
        elif origin_position == 'bottom_right':
            origin_draw_x, origin_draw_y = w - 50, h - 50
        else:
            origin_draw_x, origin_draw_y = 50, 50
        
        axis_length = 100
        
        # 根据x轴方向绘制x轴（红色）
        x_end_x = origin_draw_x + (axis_length if x_direction == 'right' else -axis_length)
        x_end_y = origin_draw_y
        cv2.arrowedLine(rotated_img, 
                        (origin_draw_x, origin_draw_y), 
                        (x_end_x, x_end_y), 
                        (0, 0, 255), 2, tipLength=0.1)
        
        # 根据y轴方向绘制y轴（绿色）
        y_end_x = origin_draw_x
        y_end_y = origin_draw_y + (axis_length if y_direction == 'down' else -axis_length)
        cv2.arrowedLine(rotated_img, 
                        (origin_draw_x, origin_draw_y), 
                        (y_end_x, y_end_y),
                        (0, 255, 0), 2, tipLength=0.1)
        
        # 添加坐标轴标签
        x_label_pos_x = x_end_x + (10 if x_direction == 'right' else -30)
        x_label_pos_y = x_end_y + 20
        cv2.putText(rotated_img, "x", 
                    (x_label_pos_x, x_label_pos_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        y_label_pos_x = y_end_x - 20
        y_label_pos_y = y_end_y + (10 if y_direction == 'down' else -10)
        cv2.putText(rotated_img, "y", 
                    (y_label_pos_x, y_label_pos_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # 在原点添加O标签
        cv2.putText(rotated_img, "O", 
                    (origin_draw_x - 20, origin_draw_y + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # 如果启用了坐标矫正，处理校准后的图像
        if self.calibration_enabled and calibrated_rectify is not None and calibrated_rotated is not None:
            # 不再使用calibrated_info_layer进行混合
            # 直接在calibrated_rotated上绘制信息
            
            # 添加标题
            cv2.putText(calibrated_rotated, "Calibrated Rotated", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            cv2.putText(calibrated_rectify, "Calibrated Rectify", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            
            # 添加机械坐标系标识 - 移除白色背景
            cv2.putText(calibrated_rotated, "Mechanical Coordinate System", (10, 55), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 128), 1)
                        
            cv2.putText(calibrated_rectify, "Mechanical Coordinate System", (10, 55), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 128), 1)
            
            # 添加机械坐标系原点信息 - 移除白色背景
            calib_config = self.config['coordinate_calibration']
            origin_text = f"Origin: ({calib_config['origin_mechanical'][0]:.3f}, {calib_config['origin_mechanical'][1]:.3f})"
            cv2.putText(calibrated_rotated, origin_text, (10, 75), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 128), 1)
                       
            cv2.putText(calibrated_rectify, origin_text, (10, 75), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 128), 1)
            
            # 在校准后的旋转图像上绘制坐标系
            # 使用相同的坐标原点位置
            # 根据x轴方向绘制x轴（红色）
            cv2.arrowedLine(calibrated_rotated, 
                            (origin_draw_x, origin_draw_y), 
                            (x_end_x, x_end_y), 
                            (0, 0, 255), 2, tipLength=0.1)
            
            # 根据y轴方向绘制y轴（绿色）
            cv2.arrowedLine(calibrated_rotated, 
                            (origin_draw_x, origin_draw_y), 
                            (y_end_x, y_end_y),
                            (0, 255, 0), 2, tipLength=0.1)
            
            # 添加坐标轴标签
            cv2.putText(calibrated_rotated, "x", 
                        (x_label_pos_x, x_label_pos_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
            
            cv2.putText(calibrated_rotated, "y", 
                        (y_label_pos_x, y_label_pos_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            
            # 在原点添加O标签
            cv2.putText(calibrated_rotated, "O", 
                        (origin_draw_x - 15, origin_draw_y + 15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            
            # 在校准后的图像上添加机械坐标系说明 - 移除白色背景
            cv2.putText(calibrated_rotated, "Mechanical Coordinates", (10, h - 15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 128), 1)
            
            cv2.putText(calibrated_rectify, "Mechanical Coordinates", (10, h - 15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 128), 1)

        if stats and results:
            for shape_type, info in stats.items():
                if info['count'] > 0:
                    for block in info['blocks']:
                        block['coords'] = (round(block['coords'][0], 3), round(block['coords'][1], 3))

        # 保存结果
        if self.debug:
            cv2.imwrite(result_path, result_img)
            cv2.imwrite(warped_path, warped)
            cv2.imwrite(rotated_path, rotated_img)
            
            # 如果启用了坐标矫正，保存校准后的图像
            if self.calibration_enabled and calibrated_rectify is not None and calibrated_rotated is not None:
                cv2.imwrite(calibrated_rectify_path, calibrated_rectify)
                cv2.imwrite(calibrated_rotated_path, calibrated_rotated)

            self._debug_print(f"\n处理完成: {image_path}")
            self._debug_print(f"结果已保存到: {result_path}")
            self._debug_print(f"校正后图像已保存到: {warped_path}")
            self._debug_print(f"旋转后图像已保存到: {rotated_path}")
            
            if self.calibration_enabled:
                self._debug_print(f"校准后的校正图像已保存到: {calibrated_rectify_path}")
                self._debug_print(f"校准后的旋转图像已保存到: {calibrated_rotated_path}")
            
            # 生成坐标系对照图
            comparison_path = self.visualize_coordinates(results, output_dir)
            self._debug_print(f"坐标系对照图已保存到: {comparison_path}")

            if stats and results:
                number_list = []  # 分别对应 I、L_left、L_right、O、T、Z_left、Z_right 的个数
                print("\n处理结果:")
                # 按原格式输出结果
                for shape_type, info in stats.items():
                    print(f"\n{shape_type}形方块数组  共 {info['count']} 个 :")
                    number_list.append(info['count'])
                    if info['count'] > 0:
                        for block in info['blocks']:
                            print(f"  编号: {block['number']}, 角度: {block['angle']:.0f}度, 坐标: ({block['coords'][0]:.3f}, {block['coords'][1]:.3f})")

                print(f"\nI、L_left、L_right、O、T、Z_left、Z_right 分别有:{number_list}")
                return stats, number_list, results

            else:
                print("处理失败")
                return stats, None, results

        if stats and results:
            number_list = []  # 分别对应 I、L_left、L_right、O、T、Z_left、Z_right 的个数
            # 按原格式输出结果
            for shape_type, info in stats.items():
                number_list.append(info['count'])
        
            return stats, number_list, results

        else:
            print("处理失败")
            return stats, None, results

    def visualize_coordinates(self, results=None, output_dir='.'):
        """
        可视化坐标系和方块位置
        :param results: 处理结果数组
        :param output_dir: 输出目录
        :return: 可视化图像路径
        """
        # 检查是否有结果
        if not results or not isinstance(results, list) or len(results) == 0:
            self._debug_print("没有可用的结果进行可视化")
            return None
            
        # 获取坐标系配置
        origin_position = self.config['coordinate_origin']['position']
        
        # 创建白色背景图像
        width, height = self.target_size
        visualization_img = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # 绘制坐标轴
        origin_x = 50
        origin_y = height - 50
        
        # 确定坐标原点位置
        if origin_position == 'top_left':
            origin_x, origin_y = 50, 50
        elif origin_position == 'top_right':
            origin_x, origin_y = width - 50, 50
        elif origin_position == 'bottom_left':
            origin_x, origin_y = 50, height - 50
        elif origin_position == 'bottom_right':
            origin_x, origin_y = width - 50, height - 50
        
        # # 绘制坐标轴
        # cv2.line(visualization_img, (origin_x, origin_y), (origin_x + 100, origin_y), (0, 0, 255), 2)  # X轴
        # cv2.line(visualization_img, (origin_x, origin_y), (origin_x, origin_y - 100), (0, 255, 0), 2)  # Y轴
        #
        # # 标记原点
        # cv2.circle(visualization_img, (origin_x, origin_y), 5, (0, 0, 0), -1)
        # cv2.putText(visualization_img, "O", (origin_x - 20, origin_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        #
        # # 标记X轴和Y轴
        # cv2.putText(visualization_img, "X", (origin_x + 110, origin_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        # cv2.putText(visualization_img, "Y", (origin_x - 20, origin_y - 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # 在图像上绘制方块坐标
        for result in results:
            try:
                shape_type = result.get('shape', '未知')
                # 使用机械坐标或偏移后的中心点坐标
                if self.calibration_enabled and 'mechanical_coords' in result:
                    coords = self.mechanical_to_board(result['mechanical_coords'])
                else:
                    # 使用已经偏移后的坐标
                    coords = result.get('center_coords', (0, 0))
                
                # 将坐标映射到可视化图像的坐标系
                visual_x = int(coords[0])
                visual_y = int(coords[1])
                
                # 确保坐标在图像范围内
                visual_x = max(0, min(visual_x, width - 1))
                visual_y = max(0, min(visual_y, height - 1))
                
                # 绘制方块位置（圆点）
                if 'L' in shape_type:
                    color = (255, 0, 0)  # 蓝色
                elif 'Z' in shape_type:
                    color = (0, 255, 255)  # 黄色
                elif shape_type == 'I':
                    color = (0, 255, 0)  # 绿色
                elif shape_type == 'O':
                    color = (255, 0, 255)  # 紫色
                elif shape_type == 'T':
                    color = (0, 0, 255)  # 红色
                else:
                    color = (128, 128, 128)  # 灰色
                
                cv2.circle(visualization_img, (visual_x, visual_y), 5, color, -1)
                
                # 获取方块编号
                number = result.get('number', 0)
                
                # 绘制方块信息
                text = f"{shape_type}-{number}"
                cv2.putText(visualization_img, text, (visual_x + 10, visual_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                
                # 绘制坐标信息
                if self.calibration_enabled and 'mechanical_coords' in result:
                    mech_coords = result['mechanical_coords']
                    coord_text = f"({mech_coords[0]:.1f}, {mech_coords[1]:.1f})"
                else:
                    coord_text = f"({coords[0]:.1f}, {coords[1]:.1f})"
                cv2.putText(visualization_img, coord_text, (visual_x + 10, visual_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                
                # 获取旋转角度
                angle = result.get('angle', 0)
                angle_text = f"{int(angle)}°"
                cv2.putText(visualization_img, angle_text, (visual_x + 10, visual_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                
            except Exception as e:
                self._debug_print(f"可视化方块坐标时出错: {str(e)}")
                continue
        
        # 添加标题和图例
        cv2.putText(visualization_img, "coordinates_visualization", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
        
        # 添加L形块的偏移说明（如果启用）
        l_shape_offset_enabled = self.config.get('l_shape_offset', {}).get('enabled', False)
        if l_shape_offset_enabled:
            l_shape_offset = self.config.get('l_shape_offset', {}).get('offset', 0)
            cv2.putText(visualization_img, f"L_offset {l_shape_offset}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # 保存可视化图像
        if self.debug:
            visualization_path = os.path.join(output_dir, 'coordinates_visualization.jpg')
            cv2.imwrite(visualization_path, visualization_img)
            self._debug_print(f"坐标可视化图像已保存到: {visualization_path}")
            return visualization_path
        
        return None


if __name__ == '__main__':
    """
    主函数入口
    """
    # 从配置文件获取输入输出路径
    image = VISION_CONFIG['input_path']
    output = VISION_CONFIG['output_path']

    # 确保输出目录存在
    if not os.path.exists(output):
        os.makedirs(output)

    print("开始处理图像...")
    # 创建处理器实例并处理图像
    processor = TetrisProcessor()
    stats, results = processor.process_image(image, output)

    # 显示处理结果
    if stats and results:
        print("\n处理结果:")
        # 按原格式输出结果
        for shape_type, info in stats.items():
            print(f"\n{shape_type}形方块数组  共 {info['count']} 个 :")
            if info['count'] > 0:
                for block in info['blocks']:
                    print(f"  编号: {block['number']}, 角度: {block['angle']:.0f}度, 坐标: ({block['coords'][0]:.3f}, {block['coords'][1]:.3f})")
    else:
        print("处理失败")
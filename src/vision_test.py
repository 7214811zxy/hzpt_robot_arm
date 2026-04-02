from modules.tcp_client import TCPClient
from modules.vision_processor import TetrisProcessor
from modules.config import QUEUE_CONFIG, VISION_CONFIG
import os
import sys
import subprocess
import platform

def list_shapes(stats):
    """列出所有可用的方块名称"""
    print("\n可用的方块列表:")
    for shape_type, info in stats.items():
        if info['count'] > 0:
            print(f"\n{shape_type}形方块 ({info['count']}个):")
            for block in info['blocks']:
                print(f"  {shape_type}-{block['number']} 坐标: ({block['coords'][0]:.3f}, {block['coords'][1]:.3f})")
    print("\n输入示例: I-1 或 L_left-2 或 quit 退出")

def process_image(processor, image_path=None):
    """处理图像并返回结果"""
    if not image_path:
        image_path = VISION_CONFIG['input_path']
    
    output_dir = VISION_CONFIG['output_path']
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"\n处理图像: {image_path}")
    stats, numbers, results = processor.process_image(image_path, output_dir)
    
    if not stats or not results:
        print("处理图像失败，无法获取方块信息")
        return None, None, None, None
    
    return stats, numbers, results, output_dir

def open_image(image_path):
    """打开图像文件"""
    if not os.path.exists(image_path):
        print(f"错误: 找不到图像文件 '{image_path}'")
        return
    
    system = platform.system()
    try:
        if system == 'Windows':
            os.startfile(image_path)
        elif system == 'Darwin':  # macOS
            subprocess.run(['open', image_path])
        else:  # Linux或其他
            subprocess.run(['xdg-open', image_path])
        print(f"已打开图像: {image_path}")
    except Exception as e:
        print(f"无法打开图像: {e}")

def show_help():
    """显示帮助信息"""
    print("\n命令帮助:")
    print("  list              - 列出所有识别到的方块")
    print("  image <文件路径>  - 指定要处理的图像文件路径")
    print("  view map          - 查看坐标系对照图")
    print("  view result       - 查看识别结果图像")
    print("  view rectify      - 查看校正后图像")
    print("  view rotated      - 查看旋转后图像")
    print("  view calibrated   - 查看校准后的校正图像")
    print("  view calibrated_rotated - 查看校准后的旋转图像")
    print("  help              - 显示此帮助信息")
    print("  quit              - 退出程序")
    print("  AA                - 发送棋盘左下角(原点)坐标")
    print("  BB                - 发送棋盘右上角坐标")
    print("  CC                - 发送棋盘左上角坐标")
    print("  DD                - 发送棋盘右下角坐标")
    print("  <方块名称>        - 发送该方块的坐标(如 I-1 或 L_left-2)")

if __name__ == '__main__':
    # 初始化视觉处理器
    processor = TetrisProcessor()
    
    # 获取命令行参数中的图像路径
    image_path = VISION_CONFIG['input_path']
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"使用命令行指定的图像路径: {image_path}")
    
    # 处理图像
    stats, numbers, results, output_dir = process_image(processor, image_path)
    
    if not stats or not results:
        print("初始图像处理失败，程序退出")
        exit(1)
    
    # 创建方块字典，方便通过名称查找
    blocks_dict = {}
    for shape_type, info in stats.items():
        for block in info['blocks']:
            block_name = f"{shape_type}-{block['number']}"
            blocks_dict[block_name] = block['coords']
    
    # 图像文件路径
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    result_image = os.path.join(output_dir, f"{base_name}_result.jpg")
    rectify_image = os.path.join(output_dir, f"{base_name}_rectify.jpg")
    rotated_image = os.path.join(output_dir, f"{base_name}_rotated.jpg")
    calibrated_rectify_image = os.path.join(output_dir, f"{base_name}_calibrated_rectify.jpg")
    calibrated_rotated_image = os.path.join(output_dir, f"{base_name}_calibrated_rotated.jpg")
    coordinate_map = os.path.join(output_dir, "coordinate_comparison.png")
    
    # 列出所有可用的方块
    list_shapes(stats)
    show_help()
    
    # 连接TCP
    client = TCPClient()
    if not client.connect():
        print("TCP连接失败")
        use_tcp = False
        print("将在不使用TCP的情况下继续运行(仅显示坐标)")
    else:
        use_tcp = True
    
    try:
        while True:
            # 获取用户输入
            command = input("\n请输入命令或方块名称: ").strip()
            
            # 处理命令
            if command.lower() == 'quit':
                break
            
            elif command.lower() == 'list':
                list_shapes(stats)
                continue
            
            elif command.lower() == 'help':
                show_help()
                continue
            
            elif command.lower().startswith('image '):
                # 提取图像路径
                new_image_path = command[6:].strip()
                if os.path.exists(new_image_path):
                    # 重新处理图像
                    image_path = new_image_path
                    stats, numbers, results, output_dir = process_image(processor, image_path)
                    if stats and results:
                        # 更新方块字典
                        blocks_dict.clear()
                        for shape_type, info in stats.items():
                            for block in info['blocks']:
                                block_name = f"{shape_type}-{block['number']}"
                                blocks_dict[block_name] = block['coords']
                        
                        # 更新图像文件路径
                        base_name = os.path.splitext(os.path.basename(image_path))[0]
                        result_image = os.path.join(output_dir, f"{base_name}_result.jpg")
                        rectify_image = os.path.join(output_dir, f"{base_name}_rectify.jpg")
                        rotated_image = os.path.join(output_dir, f"{base_name}_rotated.jpg")
                        calibrated_rectify_image = os.path.join(output_dir, f"{base_name}_calibrated_rectify.jpg")
                        calibrated_rotated_image = os.path.join(output_dir, f"{base_name}_calibrated_rotated.jpg")
                        coordinate_map = os.path.join(output_dir, "coordinate_comparison.png")
                        
                        list_shapes(stats)
                    else:
                        print("图像处理失败，继续使用之前的结果")
                else:
                    print(f"错误: 找不到图像文件 '{new_image_path}'")
                continue
            
            elif command.lower() == 'view map':
                open_image(coordinate_map)
                continue
            
            elif command.lower() == 'view result':
                open_image(result_image)
                continue
                
            elif command.lower() == 'view rectify':
                open_image(rectify_image)
                continue
                
            elif command.lower() == 'view rotated':
                open_image(rotated_image)
                continue
                
            elif command.lower() == 'view calibrated':
                open_image(calibrated_rectify_image)
                continue
                
            elif command.lower() == 'view calibrated_rotated':
                open_image(calibrated_rotated_image)
                continue
            
            # 查找对应的方块坐标
            if command == "AA":
                # 棋盘原点
                coords = (VISION_CONFIG['coordinate_calibration']['origin_mechanical'][0],
                          VISION_CONFIG['coordinate_calibration']['origin_mechanical'][1])
                print(f"棋盘原点的机械坐标: {coords}")
                
            elif command == "BB":
                # 对角点 (根据棋盘宽度和高度计算)
                coords = (VISION_CONFIG['coordinate_calibration']['diagonal_point_mechanical'][0],
                          VISION_CONFIG['coordinate_calibration']['diagonal_point_mechanical'][1])
                print(f"棋盘右下角点的机械坐标: {coords}")
                
            elif command == "CC":
                # 左上角点 (x轴为0，y轴为height)
                coords = (VISION_CONFIG['coordinate_calibration']['y_point_mechanical'][0],
                          VISION_CONFIG['coordinate_calibration']['y_point_mechanical'][1])
                print(f"棋盘左上角点的机械坐标: {coords}")
                
            elif command == "DD":
                # 右下角点 (x轴为width，y轴为0)
                coords = (VISION_CONFIG['coordinate_calibration']['x_point_mechanical'][0],
                          VISION_CONFIG['coordinate_calibration']['x_point_mechanical'][1])
                print(f"棋盘右上角点的机械坐标: {coords}")
                
            elif command in blocks_dict:
                coords = blocks_dict[command]
                print(f"方块 {command} 坐标: {coords}")
            else:
                print(f"找不到方块 '{command}'，请检查名称是否正确")
                print("提示: 使用'list'命令查看所有可用方块")
                continue
                
            # 创建队列数据
            queue = [[round(coords[0], 3), round(coords[1], 3), 
                     QUEUE_CONFIG['vision_Z'], QUEUE_CONFIG['Rx'], 
                     QUEUE_CONFIG['Ry'], QUEUE_CONFIG['Rz']]]
            
            print(f"队列数据: {queue}")
            
            # 发送数据
            if use_tcp:
                print("等待接收数据...")
                client.set_queue(queue)
                client.start_sequence()
            else:
                print("注意: TCP未连接，仅显示坐标")
    
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        if use_tcp:
            client.disconnect()
            print("TCP连接已关闭") 
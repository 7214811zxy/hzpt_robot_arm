import cv2, time
from src.modules.config import TAKE_PHOTO_CONFIG

def take_photo(save_path = TAKE_PHOTO_CONFIG['save_path']):
    if TAKE_PHOTO_CONFIG['run']:

        # 创建摄像头对象
        cap = cv2.VideoCapture(TAKE_PHOTO_CONFIG['camera_number'])

        if not cap.isOpened():
            print("无法打开摄像头")
            return False

        # 设置曝光量（值取决于摄像头型号）
        cap.set(cv2.CAP_PROP_EXPOSURE, TAKE_PHOTO_CONFIG['exposure'])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

        # 检查是否成功设置
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"实际分辨率: {actual_width}x{actual_height}")

        try:
            if not TAKE_PHOTO_CONFIG['debug']:
                print("等待相机调整曝光……")
                time.sleep(TAKE_PHOTO_CONFIG['time'])

                # 读取一帧图像
                ret, frame = cap.read()

                if not ret:
                    print("无法获取图像帧")

                if ret:
                    # 获取原始尺寸
                    h, w = frame.shape[:2]
                    print(f"原始分辨率: {w}x{h}")

                    # 计算缩放比例，保持宽高比
                    target_width = 4096
                    target_height = 3072
                    scale = min(target_width / w, target_height / h)

                    # 调整尺寸
                    resized = cv2.resize(frame, (int(w * scale), int(h * scale)))

                    # 如果需要完全匹配1080p，可以添加黑边
                    if resized.shape[0] != target_height or resized.shape[1] != target_width:
                        top = (target_height - resized.shape[0]) // 2
                        bottom = target_height - resized.shape[0] - top
                        left = (target_width - resized.shape[1]) // 2
                        right = target_width - resized.shape[1] - left
                        resized = cv2.copyMakeBorder(resized, top, bottom, left, right,
                                                     cv2.BORDER_CONSTANT, value=[0, 0, 0])

                    # 保存图像到指定路径
                    cv2.imwrite(save_path, resized)
                    print(f"照片已保存至：{save_path}")

            if TAKE_PHOTO_CONFIG['debug']:
                print("按回车键拍照，按ESC键退出...")

                while True:
                    # 读取一帧图像
                    ret, frame = cap.read()

                    if not ret:
                        print("无法获取图像帧")
                        break

                    # 显示预览窗口
                    cv2.imshow('Camera Preview', frame)

                    # 等待按键
                    key = cv2.waitKey(1) & 0xFF

                    # 按回车键拍照
                    if key == 13:  # 13是回车键的ASCII码

                        # 获取原始尺寸
                        h, w = frame.shape[:2]
                        print(f"原始分辨率: {w}x{h}")

                        # 计算缩放比例，保持宽高比
                        target_width = 4096
                        target_height = 3072
                        scale = min(target_width / w, target_height / h)

                        # 调整尺寸
                        resized = cv2.resize(frame, (int(w * scale), int(h * scale)))

                        # 如果需要完全匹配1080p，可以添加黑边
                        if resized.shape[0] != target_height or resized.shape[1] != target_width:
                            top = (target_height - resized.shape[0]) // 2
                            bottom = target_height - resized.shape[0] - top
                            left = (target_width - resized.shape[1]) // 2
                            right = target_width - resized.shape[1] - left
                            resized = cv2.copyMakeBorder(resized, top, bottom, left, right,
                                                         cv2.BORDER_CONSTANT, value=[0, 0, 0])

                        # 保存图像到指定路径
                        cv2.imwrite(save_path, resized)
                        print(f"照片已保存至：{save_path}")

                        break

                    # 按ESC键退出
                    elif key == 27:  # 27是ESC键的ASCII码
                        print("已取消拍照")
                        break

        except Exception as e:
            print(f"发生错误：{str(e)}")
            return False

        finally:
            # 释放摄像头资源
            cap.release()
            cv2.destroyAllWindows()
            return True

# 使用示例
if __name__ == "__main__":
    # 指定保存路径（请根据实际需要修改路径）
    save_path = TAKE_PHOTO_CONFIG['save_path']  # Windows路径示例
    # save_path = "/home/username/Pictures/captured_photo.jpg"  # Linux路径示例

    # 调用拍照函数
    if take_photo(save_path):
        print("拍照成功！")
    else:
        print("拍照失败")
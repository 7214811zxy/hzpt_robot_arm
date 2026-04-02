# local_server.py
import socket
import cv2
import base64
import threading


def capture_and_send(conn):
    try:
        # 使用OpenCV拍照
        cap = cv2.VideoCapture(1)  # 0通常是默认摄像头

        if not cap.isOpened():
            print("Error: Could not open camera")
            conn.sendall(b'CAMERA_ERROR')
            return

        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("Error: Could not capture image")
            conn.sendall(b'CAPTURE_ERROR')
            return

        # 将图片编码为base64
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(img_encoded.tobytes())

        # 发送图片大小信息
        size_info = f"SIZE:{len(img_base64)}".ljust(16)
        conn.sendall(size_info.encode('utf-8'))

        # 等待客户端准备就绪
        response = conn.recv(5)
        if response == b'READY':
            # 发送图片数据
            conn.sendall(img_base64)
            print("Image sent successfully")
        else:
            print("Client not ready to receive image")

    except Exception as e:
        print(f"Error in capture_and_send: {e}")
    finally:
        conn.close()


def main():
    host = '0.0.0.0'  # 监听所有网络接口
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            # 接收命令
            command = conn.recv(1024).decode('utf-8')
            if command == 'CAPTURE':
                print("Capture command received")
                conn.sendall(b'READY_TO_SEND')
                # 在新线程中处理拍照和发送
                threading.Thread(target=capture_and_send, args=(conn,)).start()
            else:
                print(f"Unknown command: {command}")
                conn.close()


if __name__ == '__main__':
    main()
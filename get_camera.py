import cv2
import numpy as np
from naoqi import ALProxy
import main

nao_ip = main.nao_ip

def get_nao_camera_frame(cameraId):
    # Initialize the camera proxy
    camProxy = ALProxy("ALVideoDevice", nao_ip, 9559)
    resolution = 2  # VGA resolution (640x480)
    colorSpace = 13  # RGB color space
    fps = 30  # Frames per second
    cameraId = cameraId  # Top camera 0, 1
    clientName = "camera_client"

    # Subscribe to the camera
    videoClient = camProxy.subscribeCamera(
        clientName, cameraId, resolution, colorSpace, fps)

    try:
        # Retrieve the camera image
        image = camProxy.getImageRemote(videoClient)
        if image is None:
            print("Failed to retrieve image")
            return None

        # Convert the image to OpenCV format
        npimg = np.frombuffer(image[6], dtype=np.uint8)
        frame = npimg.reshape((image[1], image[0], 3))
        return frame
    finally:
        # Unsubscribe to release the camera
        camProxy.unsubscribe(videoClient)


"""
# Example usage
if __name__ == "__main__":
    while True:
        frame = get_nao_camera_frame()
        if frame is not None:
            cv2.imshow("NAO Camera", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
"""
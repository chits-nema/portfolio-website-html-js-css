# linux_client.py
import requests
import cv2
import time
import numpy as np

def capture_and_send():
    # Use webcam or video file for testing
    cap = cv2.VideoCapture(0)  # Try 0, if no camera use a test video
    
    if not cap.isOpened():
        print("No camera found, using test image instead")
        # Create a test image if no camera
        test_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        cap = None
    
    while True:
        if cap:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture")
                break
        else:
            frame = test_img  # Use test image
            
        # Convert to bytes for sending
        _, img_encoded = cv2.imencode('.jpg', frame)
        
        try:
            # Send to cluster (change IP as needed)
            files = {'image': img_encoded.tobytes()}
            response = requests.post('http://YOUR_CLUSTER_IP:5000/process', 
                                   files=files, timeout=30)
            
            print(f"Result: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(5)
        
    if cap:
        cap.release()

if __name__ == "__main__":
    capture_and_send()

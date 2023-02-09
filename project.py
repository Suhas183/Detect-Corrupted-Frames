import cv2
import imagehash
from PIL import Image
import numpy as np

def detect_corrupt_frames(video_path):
    video = cv2.VideoCapture(video_path)
    prev_hash = None
    corrupt_frames = []
    frame_idx = 0
    last_frame = 0
    corrupts = 0
    corruption = False
    num_corrupts = 1
    currIsNotCorrupted = True
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        pil_image = Image.fromarray(frame)
        current_hash = imagehash.phash(pil_image)
        if prev_hash is not None and prev_hash - current_hash > 10:
            if corruption is True:
                corruption = False
                num_corrupts = 1
            
            else:    
                corruption = True
                currIsNotCorrupted = False
                corrupt_frames.append(frame_idx)
                corrupts += 1
                file_name = "corrupt_frames" + "/frame_" + str(corrupts) + "_last_frame"  + ".jpg"
                cv2.imwrite(file_name, last_frame)
                file_name = "corrupt_frames" + "/frame_" + str(corrupts) + "_corrupted_frame_1" + ".jpg"
                cv2.imwrite(file_name, frame)
        
        
        if corruption is True and currIsNotCorrupted is True:
            corrupt_frames.append(frame_idx)
            num_corrupts += 1
            file_name = "corrupt_frames" + "/frame_" + str(corrupts) + "_corrupted_frame" + str(num_corrupts) + ".jpg"
            cv2.imwrite(file_name, frame)
        
        currIsNotCorrupted = True         
        prev_hash = current_hash
        last_frame = frame
        frame_idx += 1
    
    video.release()
    return corrupt_frames

def obtainImageMatrix(frame):
    return np.array(frame)
    
video_path = 'big_buck_bunny_720p_1mb.mp4'
corrupt_frames = detect_corrupt_frames(video_path)
print(f"Corrupt frames: {corrupt_frames}")

video_path = '202302-05-0.mp4'
corrupt_frames = detect_corrupt_frames(video_path)
print(f"Corrupt frames: {corrupt_frames}")

img = cv2.imread("random.jpg")
matrix = obtainImageMatrix(img)
print






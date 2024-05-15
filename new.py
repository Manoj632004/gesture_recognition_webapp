import cv2
from cvzone.HandTrackingModule import HandDetector
import os

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

def load_overlay_images(folderpath):
    overlaylist = []
    filelist = os.listdir(folderpath)
    for filename in filelist:
        imgpath = os.path.join(folderpath, filename)
        image = cv2.imread(imgpath)
        overlaylist.append(image)
    return overlaylist


def display_finger_count(frame, count, overlaylist):
    if count > 0:
        overlay_img = overlaylist[count - 1]
        h, w, _ = overlay_img.shape
        frame[0:h, 0:w] = overlay_img

    cv2.rectangle(frame, (0, 200), (170, 425), (0, 0, 255), cv2.FILLED)
    cv2.putText(frame, str(count), (45, 375), cv2.FONT_HERSHEY_PLAIN, 9, (255, 0, 0), 24)


class VideoCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(10, 200)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.hd = HandDetector(detectionCon=0.6)
        self.overlaylist = load_overlay_images(r'./img')
        self.video_playing = True
    """
    def toggle_video(self):
        if not self.video_playing:
            self.cap.release()
        else:
            self.cap.open(0)
        self.video_playing = not self.video_playing
        """
    def gen():
        cap = cv2.VideoCapture(0)
        cap.set(10, 200)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        hd = HandDetector(detectionCon=0.6)
        overlaylist = load_overlay_images(r'./img')

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            hands, _ = hd.findHands(frame)
            if hands:
                hand = hands[0]
                fingers_up = hd.fingersUp(hand)
                count = fingers_up.count(1)
                display_finger_count(frame, count, overlaylist)

            resize_w = cv2.resize(frame,(760,520))#width,height

            ret, jpeg = cv2.imencode('.jpg', resize_w)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


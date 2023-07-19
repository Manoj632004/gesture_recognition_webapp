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
        overlay_img = overlaylist[count-1]
        h, w, _ = overlay_img.shape
        frame[0:h, 0:w] = overlay_img

    cv2.rectangle(frame, (0, 200), (170, 425), (0, 0, 255), cv2.FILLED)
    cv2.putText(frame, str(count), (45, 375), cv2.FONT_HERSHEY_PLAIN, 9, (255, 0, 0), 24)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(10, 200)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    hd = HandDetector(detectionCon=0.6)
    overlaylist = load_overlay_images(r'C:/Users/dell/Documents/portfolio/finger-counter/img')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hands, _ = hd.findHands(frame)
        total_finger_count = 0

        for hand in hands:
            fingers_up = hd.fingersUp(hand)
            count = fingers_up.count(1)
            total_finger_count += count
            display_finger_count(frame, count, overlaylist)

        display_finger_count(frame, total_finger_count, overlaylist)
        print(total_finger_count)

        cv2.imshow('Finger Counter', frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

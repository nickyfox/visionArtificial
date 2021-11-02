import cv2
import numpy as np
from PIL import ImageColor

base_colours = ['#0000FF', '#FFFF00', '#00FF00', '#00FFFF', '#8C0B90', '#C0E4FF', '#27B502', '#7C60A8', '#CF95D7',
                '#FF6666']

our_colors=[(255, 0, 0), (0, 255, 0),  (0, 0, 255), (100, 50, 0), (0, 125, 0), (0, 0, 125), (125, 125, 0),
            (125, 0, 125), (125, 125, 125)]

def main():
    # webcam init
    cap = cv2.VideoCapture(0)
    while True:
        # read and save frame
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('Window1', frame)
        # create threshold trackbar
        if cv2.waitKey(1) & 0xFF == ord('s'):
            grab_cut(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def grab_cut(img):
    # si usamos el metodo de GC_INIT_WITH_RECT no es necesario camara por eso hacemos una matriz de 0
    mask = np.zeros(img.shape[:2], np.uint8)

    # These are arrays used by the algorithm internally. You just create two np.float64 type zero arrays
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    # usamos roi para agarrar el rect
    rect = cv2.selectROI("grab_cut", img, fromCenter=False, showCrosshair=True)

    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 10, cv2.GC_INIT_WITH_RECT)
    # ????????????
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # ?????????????
    img = img*mask2[:, :, np.newaxis]
    cv2.imshow("cut", img)
    cv2.waitKey()


main()

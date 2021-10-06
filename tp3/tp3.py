import cv2
import numpy as np


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
    rect = cv2.selectROI("img", img, fromCenter=False, showCrosshair=True)
    print(mask)

    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 10, cv2.GC_INIT_WITH_RECT)
    print(mask)
    # ????????????
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    print(mask2)

    # ?????????????
    img = img*mask2[:, :, np.newaxis]

    cv2.imshow("img", img)
    cv2.waitKey()


main()

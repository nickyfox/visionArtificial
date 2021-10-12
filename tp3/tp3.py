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
    rect = cv2.selectROI("grab_cut", img, fromCenter=False, showCrosshair=True)

    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 10, cv2.GC_INIT_WITH_RECT)
    # ????????????
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # ?????????????
    img = img*mask2[:, :, np.newaxis]

    watershed(img)

    cv2.waitKey()


def watershed(img):
    global key
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    sure_fg = cv2.erode(closing, kernel, iterations=3)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    # Marker labelling
    _, markers = cv2.connectedComponents(sure_fg)

    def onclick(event, x, y, flags, param):
        global ix, iy
        if event == 4:  # cuando levantas del click
            ix, iy = x, y
            color = get_color(key)
            markers[ix][iy] = 1
            cv2.circle(img, (x, y), 7, color, -1)
            return

    while True:
        cv2.imshow("img", img)
        key = cv2.waitKey(1)
        cv2.setMouseCallback("img", onclick)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def get_color(num):
    print("este es el numero", num)
    if num & 0xFF == ord('1'):
        return (255, 0, 0)
    if num == 2:
        return (0, 255, 0)
    if num == 3:
        return (0, 0, 255)
    if num == 4:
        return (125, 0, 0)
    if num == 5:
        return (0, 125, 0)
    if num == 6:
        return  (0, 0, 125)
    if num == 7:
        return (125, 125, 0)
    if num == 8:
        return (125, 0, 125)
    if num == 9:
        return (125, 125, 125)
    return 0


main()

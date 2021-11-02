import cv2
import numpy as np
from PIL import ImageColor

base_colours = ['#0000FF', '#FFFF00', '#00FF00', '#00FFFF', '#8C0B90', '#C0E4FF', '#27B502', '#7C60A8', '#CF95D7',
                '#FF6666']
frame_window = 'Frame-Window'
seeds_map_window = 'Seeds-Map-Window'
watershed_result_window = 'Watershed-Result-Window'
our_colors=[(255, 0, 0), (0, 255, 0),  (0, 0, 255), (100, 50, 0), (0, 125, 0), (0, 0, 125), (125, 125, 0),
            (125, 0, 125), (125, 125, 125)]


def onclick(event, x, y, flags, param):
    if event == 4:  # cuando levantas del click
        val = int(chr(selected_key))
        cv2.circle(seeds, (x, y), 7,  (val, val, val), -1)
        points.append(((x, y), val))
    

# def get_color(num):
#     if num == 1:
#         return (255, 0, 0)
#     if num == 2:
#         return (0, 255, 0)
#     if num == 3:
#         return (0, 0, 255)
#     if num == 4:
#         return (100, 50, 0)
#     if num == 5:
#         return (0, 125, 0)
#     if num == 6:
#         return (0, 0, 125)
#     if num == 7:
#         return (125, 125, 0)
#     if num == 8:
#         return (125, 0, 125)
#     if num == 9:
#         return (125, 125, 125)
#     return 0


def do_watershed(img):
    markers = cv2.watershed(img, np.int32(seeds))

    img[markers == -1] = [0, 0, 255]
    for n in range(1, 10):
        img[markers == n] = ImageColor.getcolor(base_colours[n], "RGB")

    cv2.imshow(watershed_result_window, img)
    cv2.waitKey()


def main():
    global seeds
    global frame
    global selected_key
    global points

    selected_key = 49  # 1 en ASCII
    points = []

    seeds = np.zeros((720, 1280), np.uint8)
    cv2.namedWindow(frame_window)
    cv2.namedWindow(seeds_map_window)

    cap = cv2.VideoCapture(0)
    cv2.setMouseCallback(frame_window, onclick)

    while True:
        _, frame = cap.read()
        frame_copy = frame.copy()
        seeds_copy = seeds.copy()

        for point in points:
            color = ImageColor.getcolor(base_colours[point[1]], "RGB")
            val = point[1]  # point[1] es el numero que elegi para esa coordenada
            coordenadas = point[0]  # en la posicion 0 de la tupla point hay una tupla de coordenadas

            x = coordenadas[0]
            y = coordenadas[1]

            cv2.circle(frame_copy, (x, y), 7, color, -1)
            cv2.circle(seeds_copy, (x, y), 7, color, -1)

        cv2.imshow(frame_window, frame_copy)
        map = cv2.applyColorMap(seeds_copy, cv2.COLORMAP_COOL)
        cv2.imshow(seeds_map_window, map)

        key = cv2.waitKey(100) & 0xFF
        if key == 32:  # si apreto space
            do_watershed(frame.copy())
            points = []
            seeds = np.zeros((720, 1280), np.uint8)

        if ord('1') <= key <= ord('9'):
            selected_key = key

        if key == ord('q'):
            break

    cap.release()


if __name__ == '__main__':
    main()
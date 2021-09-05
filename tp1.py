import cv2


def main():
    # define main window name
    window_name = 'Window1'
    # define threshold_trackbar name
    threshold_trackbar = 'Threshold'
    # define similarity_trackbar name
    similarity_trackbar = 'Similarity'
    # define noise_trackbar name
    noise_trackbar = 'Noise'
    # define threshold_max limit
    threshold_max = 151
    # define similarity_max limit
    similarity_max = 100
    # define noise_max limit
    noise_max = 50
    # create main window
    cv2.namedWindow(window_name)
    # webcam init
    cap = cv2.VideoCapture(0)
    # define main contour (starts null)
    biggest_contour = None
    # define red color
    color_red = (0, 0, 255)
    # define green color
    color_green = (0, 255, 0)
    # create threshold trackbar
    create_trackbar(threshold_trackbar, window_name, threshold_max)
    # create similarity trackbar
    create_trackbar(similarity_trackbar, window_name, similarity_max)
    # create noise trackbar
    create_trackbar(noise_trackbar, window_name, noise_max, 10)
    # define contours map
    saved_contours = {}
    # define obj counter
    i = 1

    while True:
        # read and save frame
        _, frame = cap.read()
        # flip frame
        frame = cv2.flip(frame, 1)
        # convert frame to grayscale to apply threshold
        gray_frame = apply_color_convertion(frame, cv2.COLOR_RGB2GRAY)
        # get threshold value form trackbar
        threshold_val = int(get_trackbar_value(threshold_trackbar, window_name) / 2) * 2 + 3
        # get similarity value form trackbar (- similar, + different)
        similarity_val = get_trackbar_value(similarity_trackbar, window_name) / 100
        # get noise value form trackbar
        noise_val = get_trackbar_value(noise_trackbar, window_name)
        # apply threshold to grayscale frame (converts to black and white, helps recognizing contours)
        adapt_frame = adaptive_threshold(gray_frame, threshold_max,
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY,
                                         threshold_val)
        # remove noise from frame
        frame_denoised = denoise(adapt_frame, cv2.MORPH_ELLIPSE, noise_val)
        # get contour from frame
        contours = get_contours(frame_denoised, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            # assign biggest contour
            biggest_contour = get_biggest_contour(contours)
            # compare biggest contour with saved contours
            if compare_contours(biggest_contour, saved_contours.values(), similarity_val):
                # draw matched contour on frame
                draw_contours(frame, biggest_contour, color_green, noise_val)
                # get recognized obj name
                obj = get_obj_name(biggest_contour, saved_contours, similarity_val)
                # draw obj name text on frame
                cv2.putText(frame, obj, (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, color_green, 2, cv2.LINE_AA)
            else:
                # draw contour on frame
                draw_contours(frame, biggest_contour, color_red, noise_val)
                # get recognized obj name
                obj = get_obj_name(biggest_contour, saved_contours, similarity_val)
                # draw obj name text on frame
                cv2.putText(frame, obj, (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, color_red, 2, cv2.LINE_AA)

        # show frame on main window
        cv2.imshow(window_name, frame_denoised)
        # show frame on recognize window
        cv2.imshow('Window2', frame)

        # save obj contour on 'k' key press
        if cv2.waitKey(1) & 0xFF == ord('k'):
            if biggest_contour is not None:
                saved_contours['Object ' + str(i)] = biggest_contour
                i = i + 1
        # exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # shut down capture
    cap.release()


def apply_color_convertion(frame, color):
    return cv2.cvtColor(frame, color)


def on_trackbar(val):
    pass


def create_trackbar(trackbar_name, window_name, slider_max, starting_val=0):
    cv2.createTrackbar(trackbar_name, window_name, starting_val, slider_max, on_trackbar)


def get_trackbar_value(trackbar_name, window_name):
    return int(cv2.getTrackbarPos(trackbar_name, window_name))


def adaptive_threshold(frame, slider_max, adaptative, binary, trackbar_value):
    return cv2.adaptiveThreshold(frame, slider_max, adaptative, binary, trackbar_value, 0)


def denoise(frame, method, radius):
    kernel = cv2.getStructuringElement(method, (radius, radius))
    opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    return closing


def get_contours(frame, mode, method):
    contours, hierarchy = cv2.findContours(frame, mode, method)
    return contours


def get_biggest_contour(contours):
    max_cnt = contours[0]
    for cnt in contours:
        if cv2.contourArea(cnt) > cv2.contourArea(max_cnt):
            max_cnt = cnt
    return max_cnt


def compare_contours(contour_to_compare, saved_contours, max_diff):
    for contour in saved_contours:
        if cv2.matchShapes(contour_to_compare, contour, cv2.CONTOURS_MATCH_I2, 0) < max_diff:
            return True
    return False


def draw_contours(frame, contours, color, thickness):
    cv2.drawContours(frame, contours, -1, color, thickness)
    return frame


def get_obj_name(contour_to_compare, saved_contours, max_diff):
    for key, contour in saved_contours.items():
        if cv2.matchShapes(contour_to_compare, contour, cv2.CONTOURS_MATCH_I2, 0) < max_diff:
            return key
    return 'Unknown'


main()
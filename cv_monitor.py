import cv2

cv_scs_img = None

def update_frame(img0):
    global cv_scs_img
    cv_scs_img = img0

def cv_start(name='window', size=(400, 300)):

    width, height = size

    while 1:
        key_pressed = cv2.waitKey(1)

        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        #cv2.resizeWindow(name, width, height)

        if cv_scs_img is not None:
            scs_img = cv_scs_img
            cv2.imshow(name, cv_scs_img)

        if key_pressed % 256 == 27:
            cv2.destroyAllWindows()
            exit()
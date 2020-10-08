import pyautogui
import cv2
import numpy as np
pyautogui.FAILSAFE = False


def get_screenshot():
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def get_roi(screenshot):
    # TODO: dynamically recognize the game rectangle on the screenshot
    #       will be implemented in the future, just return a fixed values for now
    x, y, w, h = 667, 210, 674, 468
    return x, y, w, h


def thresh(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1
    )


def get_card_size(thresh):
    contours, h = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cards = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.contourArea(cnt) > 50:
            cards.append((cnt, cv2.contourArea(cnt)))

    cards.sort(key=lambda x: x[1])

    median_cnt = cards[len(cards)//2][0]
    x, y, w, h = cv2.boundingRect(median_cnt)

    return x, y, w + 3, h + 2


def mse(image_a, image_b):
    err = np.sum((image_a.astype('float') - image_b.astype('float')) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    return err


def is_pair(image_a, image_b, allow_duplicate=True):
    score = mse(image_a, image_b)
    res = score < 1500 if not allow_duplicate else score < 1000 and score > 0
    return res


def build_loc_matrix():
    return res


def click(p):
    pyautogui.click(x=p[1], y=p[0])
    print(f'clicked at loc {p}')

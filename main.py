from time import sleep
from utils import *
import cv2
import pikachu as core

img = get_screenshot()
# img = cv2.imread('test.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = thresh(img)
card_size = get_card_size(thresh)

x, y, w, h = get_roi(img)
print(
    f'There are {round(w/card_size[2]) - 1} x {round(h/card_size[3]) - 1} cards')
roi = img[y:y+h, x:x+w]
card = img[card_size[1]:card_size[1] + card_size[3],
           card_size[0]:card_size[0] + card_size[2]]

cards = []
n_x = int(w / (round(w/card_size[2]) - 1))
n_y = int(h / (round(h/card_size[3]) - 1))

card_size = [n_x, n_y]
print(f'card size {card_size} {h}')

loc_matrix = []

for card_x in range(x, x + w - card_size[0], card_size[0]):
    row = []
    l_row = []
    for card_y in range(y, y + h, card_size[1]):
        l_row.append([card_y + card_size[1]/2, card_x + card_size[0]/3])
        row.append(gray[card_y:card_y + card_size[1],
                        card_x:card_x + card_size[0]])
    loc_matrix.append(l_row)
    cards.append(row)

temp = np.array([[i] for i in loc_matrix[0]])
for col in loc_matrix[1:]:
    t = np.array([[i] for i in col])
    temp = np.concatenate((temp, t), axis=1)

loc_matrix = np.array(temp, np.int32)

flat_list = []
for sublist in cards:
    for item in sublist:
        flat_list.append(item)

number_matrix = np.zeros((9, 16), np.int8)
unique_cards = []
unique_cards_enum = [0] * 144
for i, card in enumerate(flat_list):
    if unique_cards_enum[i] > -1:
        for j, sim in enumerate(flat_list):
            if is_pair(card, sim):
                unique_cards_enum[j] = -1

for i, card in enumerate(unique_cards_enum):
    if card == 0:
        unique_cards.append(flat_list[i])

for num, val in enumerate(unique_cards):
    for i, row in enumerate(cards):
        for j, card in enumerate(row):
            if is_pair(val, card, allow_duplicate=False):
                number_matrix[j, i] = num + 1

print(number_matrix)
core.arr = number_matrix

indices = core.get_indice()
print(len(indices))


def move():
    for point in indices:
        if core.arr[point] != 0:
            res = core.find_pair(point)
            if res != False:
                return res
    return False


# loc_matrix = loc_matrix.T
# print(loc_matrix[0])

while True:
    p = move()
    if not p:
        break
    else:
        p1, p2 = p
        sleep(0.02)
        click(loc_matrix[p1])
        sleep(0.02)
        click(loc_matrix[p2])
    print(core.arr)

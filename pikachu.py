import numpy as np

arr = np.array([[1, 0, 3, 4, 5],
                [3, 0, 3, 1, 2],
                [5, 5, 6, 4, 1],
                [3, 2, 4, 1, 2],
                [6, 5, 1, 1, 4]])

p1 = (2, 2)
p2 = (2, 3)


def get_indice():
    l = []
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            l.append((i, j))
    return l


def check_ver(p1, p2):
    if p1[1] != p2[1]:
        return False
    x = p1[1]
    y1, y2 = min(p1[0], p2[0]), max(p1[0], p2[0])
    for y in range(y1 + 1, y2):
        if arr[y][x] != 0:
            return False
    return True


def check_hor(p1, p2):
    if p1[0] != p2[0]:
        return False
    y = p1[0]
    x1, x2 = min(p1[1], p2[1]), max(p1[1], p2[1])
    for x in range(x1 + 1, x2):
        if arr[y][x] != 0:
            return False
    return True


def check_z_hor(p1, p2):
    x1, x2 = min(p1[1], p2[1]), max(p1[1], p2[1])
    for x in range(x1, x2):
        p3 = (p1[0], x)
        p4 = (p2[0], x)
        if arr[p3] or arr[p4]:
            continue
        if check_hor(p1, p3) and check_hor(p4, p2) and check_ver(p3, p4):
            return True
    return False


def check_z_ver(p1, p2):
    y1, y2 = min(p1[0], p2[0]), max(p1[0], p2[0])
    for y in range(y1, y2):
        p3 = (y, p1[1])
        p4 = (y, p2[1])
        if arr[p3] or arr[p4]:
            continue
        if check_ver(p1, p3) and check_ver(p4, p2) and check_hor(p3, p4):
            return True
    return False


def check_l_hor(p1, p2):
    p3 = (p1[0], p2[1])
    if arr[p3]:
        return False
    return check_hor(p1, p3) and check_ver(p3, p2)


def check_l_ver(p1, p2):
    p3 = (p2[0], p1[1])
    if arr[p3]:
        return False
    return check_ver(p1, p3) and check_hor(p3, p2)


def check_u_hor(p1, p2):
    ra = [i for i in range(0, min(p1[1], p2[1]))]
    ra.extend([i for i in range(max(p1[1], p2[1]), len(arr[0]))])
    # print(ra)
    # import pdb
    # pdb.set_trace()
    for x in ra:
        p1_t = (p1[0], x)
        p2_t = (p2[0], x)
        if arr[p1_t] or arr[p2_t]:
            continue
        if check_ver(p1_t, p2_t) and check_hor(p1, p1_t) and check_hor(p2, p2_t):
            return True
    # check edge
    p3 = (p1[0], -1)
    p4 = (p2[0], -1)
    if check_hor(p1, p3) and check_hor(p2, p4):
        return True

    p3 = (p1[0], len(arr[0]))
    p4 = (p2[0], len(arr[0]))
    if check_hor(p1, p3) and check_hor(p2, p4):
        return True

    return False


def check_u_ver(p1, p2):
    ra = [i for i in range(0, min(p1[0], p2[0]))]
    ra.extend([i for i in range(max(p1[0], p2[0]), len(arr))])
    for y in ra:
        p1_t = (y, p1[1])
        p2_t = (y, p2[1])
        if arr[p1_t] or arr[p2_t]:
            continue
        if check_hor(p1_t, p2_t) and check_ver(p1, p1_t) and check_ver(p2, p2_t):
            return True
    # check edge
    p3 = (-1, p1[1])
    p4 = (-1, p2[1])
    if check_ver(p1, p3) and check_ver(p2, p4):
        return True
    p3 = (len(arr), p1[1])
    p4 = (len(arr), p2[1])
    if check_ver(p1, p3) and check_ver(p2, p4):
        return True

    return False


def check_2_points(p1, p2):
    if p1 == p2:
        return False
    if check_hor(p1, p2):
        return True
    # else:
    if check_z_hor(p1, p2):
        return True

    if check_ver(p1, p2):
        return True
    # else:
    if check_z_ver(p1, p2):
        return True

    if check_l_hor(p1, p2):
        return True
    if check_l_ver(p1, p2):
        return True
    if check_u_hor(p1, p2):
        return True
    if check_u_ver(p1, p2):
        return True
    return False


def find_pair(p):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == arr[p] and check_2_points(p, (i, j)):
                print(f'found pair at {p} , {(i, j)}')
                arr[p] = 0
                arr[i][j] = 0
                return (p, (i, j))
    return False


print(check_2_points(p1, p2))

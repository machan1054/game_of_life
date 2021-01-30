import numpy as np
import cv2

kernel = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ], dtype=np.uint8)

def nextgen(arr, periodic=True):
    if periodic: # 上と下、右と左をつなげるモード
        target_arr = np.insert(arr, 0, arr[-1], axis=0)
        target_arr = np.append(target_arr, [arr[0]], axis=0)
        target_arr = np.insert(target_arr, 0, target_arr[:, -1], axis=1)
        target_arr = np.append(target_arr, target_arr[:, 1].reshape(-1, 1), axis=1)
    else:
        target_arr = arr
    # 周りの生存数を畳み込みでカウント
    c = cv2.filter2D(target_arr, -1, kernel, borderType=cv2.BORDER_CONSTANT)
    if periodic:
        c = c[1:-1, 1:-1]
    arr[(c <= 1) | (c >= 4)] = 0 # 死
    arr[c == 3] = 1 # 誕生 or 生存
    return arr


def main():
    arr = np.random.randint(0, 2, [10, 10], dtype=np.uint8)
    print(arr)
    arr = nextgen(arr)
    print(arr)

if __name__ == '__main__':
    main()

import numpy as np
import cv2
from PIL import Image, ImageTk
import tkinter as tk
import time



kernel = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ], dtype=np.uint8)




def update(arr):
    # 周りの生存数を畳み込みでカウント
    c = cv2.filter2D(arr, -1, kernel, borderType=cv2.BORDER_CONSTANT)

    arr[c <= 1] = 0
    arr[c == 3] = 1
    arr[c >= 4] = 0

    return arr

def getIndex(arr):
    return np.where(arr.flatten() == 1)[0]

def make_gif(arr_index):
    imgs = []
    for n, i in enumerate(arr_index):
        img = np.zeros(size[0] * size[1], dtype=np.uint8)
        img[i] = 255
        imgs.append(Image.fromarray(img.reshape(size)))
        print('\r', n, end='')
    imgs[0].save('output.gif', save_all=True, append_images=imgs[1:], optimize=True, duration=40, loop=0)
    print('\ndone!')

def main():
    arr_index = []
    arr = np.random.randint(0, 2, [size[1], size[0]], dtype=np.uint8)
    for i in range(5000):
        arr = update(arr)
        arr_index.append(getIndex(arr))
        if i % 10 == 0:
            print('\r', i, end='')
        for j in range(2, min(10, len(arr_index) + 1)):
            if np.allclose(arr_index[-1], arr_index[-j]):
                break
        else:
            continue
        break



def arr2img(arr):
    if 1 < m:
        arr = arr.repeat(m, axis=0).repeat(m, axis=1)
    p_img = Image.fromarray(arr * 255)
    if m < 1:
        p_img = p_img.resize((round(size[0] * m), round(size[1] * m)))
    img = ImageTk.PhotoImage(image=p_img)
    return img

def next_frame():
    global arr, imlabel
    arr = update(arr)
    imlabel.image = arr2img(arr)
    imlabel.configure(image=imlabel.image)
    root.after(round(1000/fps), next_frame)

m = 10
size = [50, 50]
fps = 60

root = tk.Tk()
tk.Canvas(root, width = size[0] * m, height = size[1] * m)

arr = np.random.randint(0, 2, [size[1], size[0]], dtype=np.uint8)

imlabel = tk.Label(root, image=arr2img(arr))
imlabel.pack()

root.after_idle(next_frame)
#print('\nmaking gif...')
#make_gif(arr_index)


root.mainloop()

"""
img = np.random.randint(0, 2, (10, 10), dtype=np.uint8)
print(img)
img = update(img)
print(img)
"""

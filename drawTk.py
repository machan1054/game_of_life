
from PIL import Image, ImageTk
import tkinter as tk
import life



class LifeGUI(tk.Frame):
    def __init__(self, root, array, magnification, fps):
        super().__init__(root)
        self.pack()

        self.root = root
        self.arr = array
        self.m = magnification if 0 < magnification else 1
        self.fps = fps

        self.w = round(array.shape[1] * self.m)
        self.h = round(array.shape[0] * self.m)
        self.play = True
        self.gen = 1
        self.title = "Conway's Game of Life ({0})"

        self.imlabel = tk.Label(self)
        self.imlabel.pack()
        self.draw()


    def draw(self):
        p_img = Image.fromarray(self.arr * 255)
        if self.m != 1:
            resample = Image.NEAREST if 1 < self.m else Image.BICUBIC
            p_img = p_img.resize((self.w, self.h), resample=resample)
        self.img = ImageTk.PhotoImage(image=p_img)
        self.imlabel.configure(image=self.img)
        self.gen += 1
        self.root.title(self.title.format(self.gen))


    def update(self):
        self.arr = life.nextgen(self.arr)
        self.draw()
        if self.play:
            self.after(round(1000/self.fps), self.update)


def main():
    import numpy as np
    size = [1500, 1500]
    root = tk.Tk()
    arr = np.random.randint(0, 2, [size[1], size[0]], dtype=np.uint8)
    gui = LifeGUI(root=root, array=arr, magnification=0.5, fps=30)
    root.after_idle(gui.update)
    root.mainloop()

if __name__ == '__main__':
    main()

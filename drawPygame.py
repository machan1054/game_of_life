import pygame
import numpy as np
import lifeCore
import cv2


class LifeGUI():
    def __init__(self, array, magnification, fps):
        self.arr = array
        self.m = magnification if 0 < magnification else 1
        self.fps = fps

        self.w = round(array.shape[1] * self.m)
        self.h = round(array.shape[0] * self.m)
        self.play = True
        self.gen = 1
        self.title = "Conway's Game of Life ({0})"

        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.draw()


    def draw(self):
        pygame.display.set_caption(self.title.format(self.gen))
        if self.m != 1:
            p_img = cv2.resize(self.arr, (self.w, self.h))
        else:
            p_img = self.arr
        p_img = cv2.cvtColor(p_img * 255, cv2.COLOR_GRAY2RGB)
        self.pg_img = pygame.image.frombuffer(p_img.tobytes(), (self.w, self.h), 'RGB')
        self.screen.blit(self.pg_img, (0, 0))
        pygame.display.update() #描画処理を実行

    def run(self):
        while self.play:
            self.gen += 1
            self.arr = life.nextgen(self.arr)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.play = False
            if self.gen % 30 == 0:
                print('\r', self.clock.get_fps(), end='')
            self.clock.tick(self.fps)


def main():
    size = [1200, 800]
    arr = np.random.randint(0, 2, [size[1], size[0]], dtype=np.uint8)
    gui = LifeGUI(array=arr, magnification=1, fps=60)
    gui.run()
    pygame.quit()  #pygameのウィンドウを閉じる


if __name__=="__main__":
    main()


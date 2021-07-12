import pygame as pyg

campos = (0, 0)
speed = 30

class Sprite(pyg.sprite.Sprite):
    def __init__(self, image, xpos, ypos, groups):
        super().__init__(groups)
        self.xpos, self.ypos = xpos, ypos
        self.draw(image)
    def draw(self, image = None):
        if image:
            self.image = image
            self.rect = self.image.get_rect()
        self.rect.x = self.xpos + campos[0]
        self.rect.y = self.ypos + campos[1]

class endpoint(Sprite):
    def __init__(self, xpos, ypos, groups = None):
        image = pyg.Surface((50, 50))
        image.fill("GREEN")
        super().__init__(image, xpos, ypos, groups)

    def update(self):
        self.draw()


def main():
    global campos, speed
    running = True
    pyg.init()
    screen = pyg.display.set_mode((500, 500))
    clock = pyg.time.Clock()
    endpoints = pyg.sprite.Group()
    endpoint(400, 400, endpoints)
    while running:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_w:    campos = (campos[0], campos[1] + speed)
                if event.key == pyg.K_a:    campos = (campos[0] + speed, campos[1])
                if event.key == pyg.K_s:    campos = (campos[0], campos[1] - speed)
                if event.key == pyg.K_d:    campos = (campos[0] - speed, campos[1])
                endpoints.update()
        screen.fill("WHITE")
        endpoints.draw(screen)
        pyg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
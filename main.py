import pygame as pyg

campos = (0, 0)
speed = 30
holding = 1

class Sprite(pyg.sprite.Sprite):
    def __init__(self, image, xpos, ypos, groups = tuple):
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
    def __init__(self, xpos, ypos, groups = tuple):
        self.held = 1
        image = pyg.Surface((50, 50))
        image.fill("GREEN")
        super().__init__(image, xpos, ypos, groups)

    def update(self):
        if self.held:
            self.xpos, self.ypos = pyg.mouse.get_pos()
            self.xpos, self.ypos = self.xpos -(self.rect.width / 2) - campos[0], self.ypos - (self.rect.height / 2) - campos[1]
        self.draw()

    def clicked(self):
        global holding
        print("clicked")
        if self.held:
            self.held, holding = 0, 0
        else:
            if not holding:
                self.held, holding = 1, 1



def main():
    global campos, speed
    running = True
    pyg.init()
    screen = pyg.display.set_mode((0, 0), pyg.FULLSCREEN)
    clock = pyg.time.Clock()
    hardware_group = pyg.sprite.Group()
    endpoint(400, 400, (hardware_group))

    #endpoint(200, 400, (hardware_group))
    while running:
        for event in pyg.event.get():
            #print(event)
            if event.type == pyg.QUIT:
                running = False
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_w:    campos = (campos[0], campos[1] + speed)
                if event.key == pyg.K_a:    campos = (campos[0] + speed, campos[1])
                if event.key == pyg.K_s:    campos = (campos[0], campos[1] - speed)
                if event.key == pyg.K_d:    campos = (campos[0] - speed, campos[1])
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == pyg.BUTTON_LEFT:
                    for X in [X for X in hardware_group]:
                        print(X.rect)
                        print(event.pos)
                        if X.rect.collidepoint(event.pos):
                            X.clicked()
            hardware_group.update()
        screen.fill("WHITE")
        hardware_group.draw(screen)
        pyg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
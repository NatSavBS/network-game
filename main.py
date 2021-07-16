import pygame as pyg

campos = [0, 0]
speed = 30
holding = 0

class Sprite(pyg.sprite.Sprite):
    def __init__(self, image, groups = tuple):
        self.xpos, self.ypos = pyg.mouse.get_pos()
        self.held = 1
        super().__init__(groups)
        self.draw(image)

    def draw(self, image = None):
        if image:
            self.image = image
            self.rect = self.image.get_rect()
        self.rect.x = self.xpos + campos[0]
        self.rect.y = self.ypos + campos[1]

    def clicked(self):
        global holding, toolbox_size
        if self.held:
            self.held, holding = 0, 0
            toolbox = pyg.rect.Rect(toolbox_size)
            if self.rect.colliderect(toolbox):
                self.kill()
        else:
            if not holding:
                self.held, holding = 1, 1

    def update(self):
        if self.held:
            self.xpos, self.ypos = pyg.mouse.get_pos()
            self.xpos, self.ypos = self.xpos -(self.rect.width / 2) - campos[0], self.ypos - (self.rect.height / 2) - campos[1]
        self.draw()

class endpoint(Sprite):
    def __init__(self, groups = tuple):
        image = pyg.Surface((50, 50))
        image.fill("GREEN")
        super().__init__(image, groups)

class server(Sprite):
    def __init__(self, groups = tuple):
        image = pyg.Surface((70, 100))
        image.fill("RED")
        super().__init__(image, groups)

class switch(Sprite):
    def __init__(self, groups = tuple):
        image = pyg.Surface((50, 150))
        image.fill("BLUE")
        super().__init__(image, groups)





class menu_button(pyg.sprite.Sprite):
    def __init__(self, image, xpos, ypos, group, cmd):
        super().__init__(group)
        self.image = image
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = xpos, ypos
        self.cmd = cmd

    def clicked(self):
        global holding
        if holding == 0:
            holding = 1
            self.cmd()



def main():
    global campos, speed, toolbox_size
    running = True
    dragging = False
    pyg.init()
    screen = pyg.display.set_mode((0, 0), (pyg.FULLSCREEN | pyg.SRCALPHA))
    clock = pyg.time.Clock()
    hardware_group = pyg.sprite.Group()
    menu_buttons = pyg.sprite.Group()
    clickable = pyg.sprite.Group()


    toolbox_size = (0, screen.get_height() / 10, (screen.get_width() / 10) * 2, (screen.get_height() / 10) * 8)
    toolbox = pyg.Surface(toolbox_size[2:], pyg.SRCALPHA)

    toolbox.fill(color=(0, 0, 0, 128))

    image = pyg.Surface((50, 50))
    image.fill("GREEN")
    menu_button(image, 20, 110, (menu_buttons, clickable), lambda: endpoint((hardware_group, clickable)))

    image = pyg.Surface((70, 100))
    image.fill("RED")
    menu_button(image, 20, 180, (menu_buttons, clickable), lambda: server((hardware_group, clickable)))

    image = pyg.Surface((50, 150))
    image.fill("BLUE")
    menu_button(image, 20, 300, (menu_buttons, clickable), lambda: switch((hardware_group, clickable)))

    while running:
        for event in pyg.event.get():
            #print(event)
            if event.type == pyg.QUIT:
                running = False
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_w:    campos = [campos[0], campos[1] + speed]
                if event.key == pyg.K_a:    campos = [campos[0] + speed, campos[1]]
                if event.key == pyg.K_s:    campos = [campos[0], campos[1] - speed]
                if event.key == pyg.K_d:    campos = [campos[0] - speed, campos[1]]
                if event.key == pyg.K_ESCAPE: running = False
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == pyg.BUTTON_LEFT:
                    
                    for X in [X for X in clickable]:
                        if X.rect.collidepoint(event.pos):
                            X.clicked()
                            break
                    else:
                        dragging = True
                        drag_cords = (pyg.mouse.get_pos(), campos.copy())
            if event.type == pyg.MOUSEBUTTONUP:
                if event.button == pyg.BUTTON_LEFT:
                    dragging = False
            hardware_group.update()
        if dragging:
            campos[0] = pyg.mouse.get_pos()[0] + drag_cords[1][0] - drag_cords[0][0]
            campos[1] = pyg.mouse.get_pos()[1] + drag_cords[1][1] - drag_cords[0][1]
            #print("dragging", campos)
        screen.fill("WHITE")
        hardware_group.draw(screen)
        screen.blit(toolbox, toolbox_size)
        menu_buttons.draw(screen)
        pyg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
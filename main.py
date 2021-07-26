import pygame as pyg
import ipaddress



class Hardware(pyg.sprite.Sprite):  # sprite class for the hardware on the screen
    def __init__(self, image, groups):
        self.xpos, self.ypos = pyg.mouse.get_pos()
        self.active = 1
        super().__init__(groups)
        self.draw(image)

    def draw(self, image=None):  # if the image has changed, reset it and reposition based on camera
        if image:
            self.image = image
            self.rect = self.image.get_rect()
        self.rect.x = self.xpos + campos[0]
        self.rect.y = self.ypos + campos[1]

    def physical_click(self):  # if clicked, check to see if should be held or dropped, if dropped onto toolbox, remove
        global toolbox_size
        print(type(self).__name__)
        if self.active:
            self.active = 0
            toolbox = pyg.rect.Rect(toolbox_size)
            if self.rect.colliderect(toolbox):
                self.kill()
                del self
        else:
            if not holding():
                self.active = 1

    def update(self):  # if held, reposition and then draw itself
        if self.active:
            self.xpos, self.ypos = pyg.mouse.get_pos()
            self.xpos, self.ypos = self.xpos - (self.rect.width / 2) - campos[0], \
                                   self.ypos - (self.rect.height / 2) - campos[1]
        self.draw()


class Endpoint(Hardware):  # class for endpoint devices
    def __init__(self, groups):
        image = pyg.image.load("endpoint.png")
        Nic(self, -5, 20)
        super().__init__(image, groups)

    def logical_click(self):
        logical_menu.empty()
        # create menu to set remote server
        # create static menu elements
        MenuText(standard.render("Remote server IP", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 60,
                 logical_menu)
        MenuText(standard.render("Remote server Port", True, (0, 0, 0)), 20, toolbox_size[1] + 110, logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 150,
                 logical_menu)



class Server(Hardware):  # class for server devices
    def __init__(self, groups):
        image = pyg.image.load("server.png")
        for X in [[-5, 35], [-5, 65], [65, 35], [65, 65]]:
            Nic(self, X[0], X[1])
        super().__init__(image, groups)

    def logical_click(self):
        logical_menu.empty()
        # create menu to set IP's and ports to listen on
        # create static menu elements
        MenuText(standard.render("Service 1", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)
        MenuText(standard.render("IP's to listen on", True, (0, 0, 0)), 20, toolbox_size[1] + 60, logical_menu)
        # TODO tickbox class
        MenuText(standard.render("Port", True, (0, 0, 0)), 20, toolbox_size[1] + 110, logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 150,
                 logical_menu)

        MenuText(standard.render("Service 2", True, (0, 0, 0)), 20, toolbox_size[1] + 220, logical_menu)
        MenuText(standard.render("IP's to listen on", True, (0, 0, 0)), 20, toolbox_size[1] + 260, logical_menu)
        # TODO tickbox class
        MenuText(standard.render("Port", True, (0, 0, 0)), 20, toolbox_size[1] + 310, logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 350,
                 logical_menu)

        MenuText(standard.render("Service 3", True, (0, 0, 0)), 20, toolbox_size[1] + 420, logical_menu)
        MenuText(standard.render("IP's to listen on", True, (0, 0, 0)), 20, toolbox_size[1] + 460, logical_menu)
        # TODO tickbox class
        MenuText(standard.render("Port", True, (0, 0, 0)), 20, toolbox_size[1] + 510, logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 550,
                 logical_menu)



class Switch(Hardware):  # class for switch devices
    def __init__(self, groups):
        image = pyg.image.load("switch.png")
        for X in [4, 16]:
            for Y in [15, 25, 35, 45, 55, 65, 75, 85]:
                Nic(self, X, Y)
        super().__init__(image, groups)

    def logical_click(self):
        logical_menu.empty()
        # create menu to set routing rules
        # create static menu elements
        MenuText(standard.render("Routing", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)

        MenuText(standard.render("Route 1", True, (0, 0, 0)), 20, toolbox_size[1] + 60, logical_menu)
        MenuText(standard.render("IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 90,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 120,
                 logical_menu)
        MenuText(standard.render("Netmask", True, (0, 0, 0)), 20, toolbox_size[1] + 150,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 180,
                 logical_menu)

        MenuText(standard.render("Route 2", True, (0, 0, 0)), 20, toolbox_size[1] + 230, logical_menu)
        MenuText(standard.render("IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 260,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 290,
                 logical_menu)
        MenuText(standard.render("Netmask", True, (0, 0, 0)), 20, toolbox_size[1] + 320,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 350,
                 logical_menu)

        MenuText(standard.render("Rule 3", True, (0, 0, 0)), 20, toolbox_size[1] + 400, logical_menu)
        MenuText(standard.render("IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 430,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 460,
                 logical_menu)
        MenuText(standard.render("Netmask", True, (0, 0, 0)), 20, toolbox_size[1] + 490,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 520,
                 logical_menu)


class Firewall(Hardware):  # class for firewalls
    def __init__(self, groups):
        image = pyg.Surface((70, 30))
        image.fill("PURPLE")
        for X in [[9, -5], [23, -5], [37, -5], [51, -5], [30, 25]]:
            Nic(self, X[0], X[1])
        super().__init__(image, groups)

    def logical_click(self):
        logical_menu.empty()
        # create menu to set firewall allow rules
        # create static menu elements
        MenuText(standard.render("Firewall Rules", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)

        MenuText(standard.render("Rule 1", True, (0, 0, 0)), 20, toolbox_size[1] + 60, logical_menu)
        MenuText(standard.render("Source Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 90,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 120,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 120,
                 logical_menu)
        MenuText(standard.render("Destination Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 150,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 180,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 180,
                 logical_menu)

        MenuText(standard.render("Rule 2", True, (0, 0, 0)), 20, toolbox_size[1] + 230, logical_menu)
        MenuText(standard.render("Source Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 260,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 290,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 290,
                 logical_menu)
        MenuText(standard.render("Destination Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 320,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 350,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 350,
                 logical_menu)

        MenuText(standard.render("Rule 3", True, (0, 0, 0)), 20, toolbox_size[1] + 400, logical_menu)
        MenuText(standard.render("Source Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 430,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 460,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 460,
                 logical_menu)
        MenuText(standard.render("Destination Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 490,
                 logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 520,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 520,
                 logical_menu)


class Router(Hardware):  # class for firewalls
    def __init__(self, groups):
        image = pyg.Surface((30, 30))
        image.fill("CYAN")
        Nic(self, 10, -5)
        super().__init__(image, groups)

    def logical_click(self):
        logical_menu.empty()
        # create menu to set external ip and port forwarding rules
        # create static menu elements
        MenuText(standard.render("External IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 60,
                 logical_menu)
        MenuText(standard.render("Port Forwarding", True, (0, 0, 0)), 20, toolbox_size[1] + 110, logical_menu)

        MenuText(standard.render("Rule 1", True, (0, 0, 0)), 20, toolbox_size[1] + 150, logical_menu)
        MenuText(standard.render("External Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 180, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 210,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 210,
                 logical_menu)
        MenuText(standard.render("Internal Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 240, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 270,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 270,
                 logical_menu)

        MenuText(standard.render("Rule 2", True, (0, 0, 0)), 20, toolbox_size[1] + 320, logical_menu)
        MenuText(standard.render("External Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 350, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 380,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 380,
                 logical_menu)
        MenuText(standard.render("Internal Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 410, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 440,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 440,
                 logical_menu)

        MenuText(standard.render("Rule 3", True, (0, 0, 0)), 20, toolbox_size[1] + 490, logical_menu)
        MenuText(standard.render("External Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 520, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 550,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 550,
                 logical_menu)
        MenuText(standard.render("Internal Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 580, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 610,
                 logical_menu)
        MenuText(standard.render("     ", True, (0, 0, 0), (255, 255, 255)), 150, toolbox_size[1] + 610,
                 logical_menu)



class Nic(pyg.sprite.Sprite):  # class for NIC's
    def __init__(self, parent, x_off, y_off, type="physical"):
        self.image = pyg.image.load("NIC.png")
        self.parent, self.x_off, self.y_off, self.active, self.type = parent, x_off, y_off, False, type
        super().__init__(NICs)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = self.parent.xpos + self.x_off + campos[0]
        self.rect.y = self.parent.ypos + self.y_off + campos[1]
        if self.active:
            pyg.draw.line(screen, (0, 0, 0), (self.rect.x + 5, self.rect.y + 5), pyg.mouse.get_pos(), 3)
        if not hardware_group.has(self.parent):
            self.kill()
            for X in connections:
                if X[0] == self or X[1] == self:
                    connections.remove(X)
            del self

    def physical_click(self):
        global connections
        print(type(self).__name__)
        if holding():
            for X in connections:
                if X[0] == self or X[1] == self:
                    connections.remove(X)
                    break
            remote_nic = [X for X in NICs if X.active]
            remote_nic[0].active = False
            connections.append([self, remote_nic[0]])
        else:
            for X in connections:
                if X[0] == self or X[1] == self:
                    connections.remove(X)
                    break
            self.active = True

    def logical_click(self):
        logical_menu.empty()
        # create menu to set ip, netmask and gateway
        # create static menu elements
        MenuText(standard.render("IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 60,
                 logical_menu)
        MenuText(standard.render("Netmask", True, (0, 0, 0)), 20, toolbox_size[1] + 110, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 150,
                 logical_menu)
        MenuText(standard.render("Default gateway", True, (0, 0, 0)), 20, toolbox_size[1] + 200, logical_menu)
        MenuText(standard.render("   .   .   .   ", True, (0, 0, 0), (255, 255, 255)), 20, toolbox_size[1] + 240,
                 logical_menu)




class MenuButton(pyg.sprite.Sprite):  # class for menu buttons
    def __init__(self, image, xpos, ypos, group, cmd):
        self.active = 0  # needed for compatibility
        super().__init__(group)
        self.image = image
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = xpos, ypos
        self.cmd = cmd

    # if menu button is clicked, check to see if holding anything before calling cmd (spawn hardware)
    def physical_click(self):
        if not holding():
            self.cmd()

class MenuText(pyg.sprite.Sprite):  # class for non clickable menu elements
    def __init__(self, image, xpos, ypos, group):
        self.active = 0  # needed for compatibility
        super().__init__(group)
        self.image = image
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = xpos, ypos

def draw():
    global state
    screen.fill("WHITE")  # blank the screen
    for X in connections:  # draw the connection lines
        pyg.draw.line(screen, (0, 0, 0), (X[0].rect.x + 5, X[0].rect.y + 5), (X[1].rect.x + 5, X[1].rect.y + 5), 3)
    hardware_group.draw(screen)  # draw the hardware
    NICs.draw(screen)  # draw the NIC's (need to do separately to ensure they afe drawn over the hardware)
    screen.blit(toolbox, toolbox_size)  # draw te toolbox
    if state == "physical":
        physical_menu.draw(screen)  # draw the menu buttons
        for X in [X for X in NICs if X.active]:
            pyg.draw.line(screen, (0, 0, 0), (X.rect.x + 5, X.rect.y + 5), pyg.mouse.get_pos(), 3)
    if state == "logical":
        logical_menu.draw(screen)
    screen.blit(state_button, state_button_size)
    pyg.display.flip()  # flip the screen buffer
    clock.tick(60)  # wait 1/60th of a second from the last time a frame was drawn

def main():
    global campos, speed, toolbox, toolbox_size, state_button, state_button_size, connections, state
    running = True
    dragging = False
    drag_cords = [[0, 0], [0, 0]]
    connections = []

    # create the toolbox surface
    toolbox_size = (0, screen.get_height() / 10, (screen.get_width() / 10) * 2, (screen.get_height() / 10) * 8)
    toolbox = pyg.Surface(toolbox_size[2:], pyg.SRCALPHA)
    toolbox.fill(color=(0, 0, 0, 128))  # colour the toolbox surface

    state_button_size = ((screen.get_width() / 10) * 8, (screen.get_height() / 10) * 8, (screen.get_width() / 10),
                         (screen.get_height() / 10))
    state_button = pyg.Surface(state_button_size[2:], pyg.SRCALPHA)

    # create menu buttons for endpoint server and switch
    image = pyg.image.load("endpoint.png")
    MenuButton(image, 20, toolbox_size[1] + 20, (physical_menu, clickable),
               lambda: Endpoint((hardware_group, clickable)))
    image = pyg.image.load("server.png")
    MenuButton(image, 20, toolbox_size[1] + 90, (physical_menu, clickable),
               lambda: Server((hardware_group, clickable)))
    image = pyg.image.load("switch.png")
    MenuButton(image, 20, toolbox_size[1] + 210, (physical_menu, clickable),
               lambda: Switch((hardware_group, clickable)))
    image = pyg.Surface((70, 30))
    image.fill("PURPLE")
    MenuButton(image, 20, toolbox_size[1] + 330, (physical_menu, clickable),
               lambda: Firewall((hardware_group, clickable)))
    image = pyg.Surface((30, 30))
    image.fill("CYAN")
    MenuButton(image, 20, toolbox_size[1] + 380, (physical_menu, clickable),
               lambda: Router((hardware_group, clickable)))

    while running:
        toolbox.fill(color=(0, 0, 0, 128))
        state_button.fill(color=(0, 0, 0, 128))
        state_button_text = large.render("Physical", True, (0, 0, 0, 128))
        state_button.blit(state_button_text, (state_button_size[2] / 2 - state_button_text.get_width() / 2,
                                              state_button_size[3] / 2 - state_button_text.get_height() / 2))
        while state == "physical" and running:
            for event in pyg.event.get():  # For Every Event
                if event.type == pyg.QUIT:  # Break on quit button
                    running = False
                if event.type == pyg.KEYDOWN:  # Move canvas with WASD
                    if event.key == pyg.K_w:    campos = [campos[0], campos[1] + speed]
                    if event.key == pyg.K_a:    campos = [campos[0] + speed, campos[1]]
                    if event.key == pyg.K_s:    campos = [campos[0], campos[1] - speed]
                    if event.key == pyg.K_d:    campos = [campos[0] - speed, campos[1]]
                    if event.key == pyg.K_ESCAPE: running = False  # Break on esc
                if event.type == pyg.MOUSEBUTTONDOWN:  # if a mouse button was pressed
                    if event.button == pyg.BUTTON_LEFT:  # if the left button was pressed
                        print(event.pos, pyg.rect.Rect(state_button_size))
                        if pyg.rect.Rect(state_button_size).collidepoint(event.pos):
                            if not holding():
                                state = "logical"
                                break
                        for X in [X for X in NICs] + [X for X in clickable]:  # for the nics and the clickable group
                            if X.rect.collidepoint(event.pos):  # if it was clicked
                                try: X.physical_click()  # call the clicked function
                                except AttributeError: pass
                                break  # stop looking for collisions
                        else:  # if nothing was clicked
                            dragging = True  # start dragging the canvas
                            drag_cords = (pyg.mouse.get_pos(), campos.copy())
                    if event.button == pyg.BUTTON_RIGHT:  # if the right mouse button was pressed
                        try: [X for X in NICs if X.active][0].active = False  # if holding a wire, stop
                        except IndexError: pass  # dont crash if not holding a wire
                if event.type == pyg.MOUSEBUTTONUP:  # if a mouse button was released
                    if event.button == pyg.BUTTON_LEFT:  # if the left mouse button was released
                        dragging = False  # stop dragging the canvas
                hardware_group.update()  # redraw the hardware assets (probably have moved)
                NICs.update()  # update the NIC's (move with the hardware)
            if dragging:  # if dragging the canvas, move the camera with the mouse
                campos[0] = pyg.mouse.get_pos()[0] + drag_cords[1][0] - drag_cords[0][0]
                campos[1] = pyg.mouse.get_pos()[1] + drag_cords[1][1] - drag_cords[0][1]

            draw()

        toolbox.fill(color=(0, 0, 0, 128))
        state_button.fill(color=(0, 0, 0, 128))
        state_button_text = large.render("Logical", True, (0, 0, 0, 128))
        state_button.blit(state_button_text, (state_button_size[2] / 2 - state_button_text.get_width() / 2,
                                              state_button_size[3] / 2 - state_button_text.get_height() / 2))
        while state == "logical" and running:
            for event in pyg.event.get():  # For Every Event
                if event.type == pyg.QUIT:  # Break on quit button
                    running = False
                if event.type == pyg.KEYDOWN:  # Move canvas with WASD
                    if event.key == pyg.K_w:    campos = [campos[0], campos[1] + speed]
                    if event.key == pyg.K_a:    campos = [campos[0] + speed, campos[1]]
                    if event.key == pyg.K_s:    campos = [campos[0], campos[1] - speed]
                    if event.key == pyg.K_d:    campos = [campos[0] - speed, campos[1]]
                    if event.key == pyg.K_ESCAPE: running = False  # Break on esc
                if event.type == pyg.MOUSEBUTTONDOWN:
                    if pyg.rect.Rect(state_button_size).collidepoint(event.pos):
                        state = "physical"
                        break
                    for X in [X for X in NICs] + [X for X in clickable]:  # for the nics and the clickable group
                        if X.rect.collidepoint(event.pos):  # if it was clicked
                            try: X.logical_click()  # call the clicked function
                            except AttributeError: pass
                    else:  # if nothing was clicked
                        dragging = True  # start dragging the canvas
                        drag_cords = (pyg.mouse.get_pos(), campos.copy())
                if event.type == pyg.MOUSEBUTTONUP:  # if a mouse button was released
                    if event.button == pyg.BUTTON_LEFT:  # if the left mouse button was released
                        dragging = False  # stop dragging the canvas
                hardware_group.update()  # redraw the hardware assets (probably have moved)
                NICs.update()  # update the NIC's (move with the hardware)
            if dragging:  # if dragging the canvas, move the camera with the mouse
                campos[0] = pyg.mouse.get_pos()[0] + drag_cords[1][0] - drag_cords[0][0]
                campos[1] = pyg.mouse.get_pos()[1] + drag_cords[1][1] - drag_cords[0][1]
            draw()


if __name__ == "__main__":
    campos = [0, 0]
    speed = 30

    state = "physical"
    pyg.init()
    screen = pyg.display.set_mode((0, 0), (pyg.FULLSCREEN | pyg.SRCALPHA))
    clock = pyg.time.Clock()
    hardware_group = pyg.sprite.Group()
    physical_menu = pyg.sprite.Group()
    logical_menu = pyg.sprite.Group()
    clickable = pyg.sprite.Group()
    NICs = pyg.sprite.Group()  # nics need a seperate group to ensure they get click and draw z priority
    holding = lambda: bool([X for X in [X for X in NICs] + [X for X in clickable] if X.active])
    # function to determine if any instances have the held flag set
    large = pyg.font.SysFont("arial", 40)
    standard = pyg.font.SysFont("arial", 25)
    main()

import pygame as pyg
import ipaddress
import math
import time


class Hardware(pyg.sprite.Sprite):  # sprite class for the hardware on the screen
    def __init__(self, image, groups):
        self.xpos, self.ypos = pyg.mouse.get_pos()  # set initial position to that of the mouse cursor
        self.active = True  # set the active flag (hardware is held when created)
        # noinspection PyTypeChecker
        super().__init__(groups)  # initialise the parent class
        self.draw(image)  # call to have the image applied and the rect placed

    def draw(self, image=None):  # if the image has changed, reset it and reposition based on camera
        if image:  # if an image was supplied
            self.image = image  # give scope
            self.rect = self.image.get_rect()  # get size of image
        self.rect.x, self.rect.y = self.xpos + campos[0], self.ypos + campos[1]  # place image onto screen

    def physical_click(self):  # if clicked, in physical mode
        global toolbox_size
        if self.active:  # if held
            self.active = False  # stop holding
            toolbox = pyg.rect.Rect(toolbox_size)
            if self.rect.colliderect(toolbox):  # if "dropped" onto toolbox, destroy
                self.kill()
                del self
        else:  # if not held
            if not holding():  # if not holding anything else
                self.active = True  # hold

    def update(self):  # if held, reposition and then draw itself
        if self.active:  # if held
            self.xpos, self.ypos = pyg.mouse.get_pos()  # reposition middle to mouse cursor
            self.xpos, self.ypos = self.xpos - (self.rect.width / 2) - campos[0], \
                                   self.ypos - (self.rect.height / 2) - campos[1]
        self.draw()  # call draw


class Endpoint(Hardware):  # class for endpoint devices
    def __init__(self, groups):
        image = pyg.image.load("endpoint.png")
        self.interface = Nic(self, -5, 20)
        super().__init__(image, groups)
        self.last_pkt = 0.0

    def logical_click(self):  # if clicked in logical mode
        for X in [X for X in logical_menu]: X.kill()  # clear logical menu
        # create menu to set remote server
        # create static menu elements
        MenuText(standard.render("Remote server IP", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)
        MenuText(standard.render("Remote server Port", True, (0, 0, 0)), 20, toolbox_size[1] + 110, logical_menu)
        # create dynamic menu elements
        QuadOctetEntry(self, 20, toolbox_size[1] + 60, "remote_ip", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 20, toolbox_size[1] + 150, "remote_port", (clickable, logical_menu))

    def simulate(self):
        if self.last_pkt < time.time() - 1:
            self.last_pkt = time.time()
            print("pkt")
            print(connections)
            print(self.interface.ip)


class Server(Hardware):  # class for server devices
    def __init__(self, groups):
        image = pyg.image.load("server.png")
        for X in [[-5, 35], [-5, 65], [65, 35], [65, 65]]:
            Nic(self, X[0], X[1])
        super().__init__(image, groups)

    def logical_click(self):  # if clicked in logical mode
        for X in [X for X in logical_menu]: X.kill()  # clear logical menu
        # create menu to set IP's and ports to listen on
        # create menu elements
        MenuText(standard.render("Service 1", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)
        MenuText(standard.render("IP's to listen on", True, (0, 0, 0)), 20, toolbox_size[1] + 60, logical_menu)
        MenuText(standard.render("Port", True, (0, 0, 0)), 20, toolbox_size[1] + 110, logical_menu)
        MenuEntry(self, 5, 20, toolbox_size[1] + 150, "port_1", (clickable, logical_menu))

        MenuText(standard.render("Service 2", True, (0, 0, 0)), 20, toolbox_size[1] + 220, logical_menu)
        MenuText(standard.render("IP's to listen on", True, (0, 0, 0)), 20, toolbox_size[1] + 260, logical_menu)
        MenuText(standard.render("Port", True, (0, 0, 0)), 20, toolbox_size[1] + 310, logical_menu)
        MenuEntry(self, 5, 20, toolbox_size[1] + 350, "port_2", (clickable, logical_menu))

        MenuText(standard.render("Service 3", True, (0, 0, 0)), 20, toolbox_size[1] + 420, logical_menu)
        MenuText(standard.render("IP's to listen on", True, (0, 0, 0)), 20, toolbox_size[1] + 460, logical_menu)
        MenuText(standard.render("Port", True, (0, 0, 0)), 20, toolbox_size[1] + 510, logical_menu)
        MenuEntry(self, 5, 20, toolbox_size[1] + 550, "port_3", (clickable, logical_menu))

        interfaces = [X.ip for X in NICs if X.parent == self]  # find nics parented by self
        MenuSelector(interfaces, self, 140, toolbox_size[1] + 70, "interfaces_1", (logical_menu, clickable))
        MenuSelector(interfaces, self, 140, toolbox_size[1] + 270, "interfaces_2", (logical_menu, clickable))
        MenuSelector(interfaces, self, 140, toolbox_size[1] + 470, "interfaces_3", (logical_menu, clickable))

    def simulate(self):
        pass


class Switch(Hardware):  # class for switch devices
    def __init__(self, groups):
        image = pyg.image.load("switch.png")
        for X in [4, 16]:  # create menu elements
            for Y in [15, 25, 35, 45, 55, 65, 75, 85]:
                Nic(self, X, Y)
        super().__init__(image, groups)

    def logical_click(self):
        for X in [X for X in logical_menu]: X.kill()
        # create menu to set routing rules
        # create menu elements
        MenuText(standard.render("Routing", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)

        MenuText(standard.render("Route 1", True, (0, 0, 0)), 20, toolbox_size[1] + 60, logical_menu)
        MenuText(standard.render("IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 90, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 120, "ip_1", logical_menu, (logical_menu, clickable))
        MenuText(standard.render("Netmask", True, (0, 0, 0)), 20, toolbox_size[1] + 150, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 180, "netmask_1", logical_menu, (logical_menu, clickable))

        MenuText(standard.render("Route 2", True, (0, 0, 0)), 20, toolbox_size[1] + 230, logical_menu)
        MenuText(standard.render("IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 260, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 290, "ip_2", logical_menu, (logical_menu, clickable))
        MenuText(standard.render("Netmask", True, (0, 0, 0)), 20, toolbox_size[1] + 320, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 350, "netmask_2", logical_menu, (logical_menu, clickable))

        MenuText(standard.render("Rule 3", True, (0, 0, 0)), 20, toolbox_size[1] + 400, logical_menu)
        MenuText(standard.render("IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 430, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 460, "ip_3", logical_menu, (logical_menu, clickable))
        MenuText(standard.render("Netmask", True, (0, 0, 0)), 20, toolbox_size[1] + 490, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 520, "netmask_3", logical_menu, (logical_menu, clickable))

    def simulate(self):
        pass


class Firewall(Hardware):  # class for firewalls
    def __init__(self, groups):
        image = pyg.Surface((70, 30))
        image.fill("PURPLE")
        for X in [[9, -5], [23, -5], [37, -5], [51, -5], [30, 25]]:  # create NIC's
            Nic(self, X[0], X[1])
        super().__init__(image, groups)  # create parent class

    def logical_click(self):
        for X in [X for X in logical_menu]: X.kill()
        # create menu to set firewall allow rules
        # create static menu elements
        MenuText(standard.render("Firewall Rules", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)

        MenuText(standard.render("Rule 1", True, (0, 0, 0)), 20, toolbox_size[1] + 60, logical_menu)
        MenuText(standard.render("Source Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 90,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 120, "source_ip_1", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 190, toolbox_size[1] + 120, "ext_port_1", (clickable, logical_menu))
        MenuText(standard.render("Destination Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 150,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 180, "dest_ip_1", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 190, toolbox_size[1] + 180, "internal_port_1", (clickable, logical_menu))

        MenuText(standard.render("Rule 2", True, (0, 0, 0)), 20, toolbox_size[1] + 230, logical_menu)
        MenuText(standard.render("Source Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 260,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 290, "source_ip_2", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 190, toolbox_size[1] + 290, "ext_port_2", (clickable, logical_menu))
        MenuText(standard.render("Destination Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 320,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 350, "dest_ip_2", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 190, toolbox_size[1] + 350, "internal_port_2", (clickable, logical_menu))

        MenuText(standard.render("Rule 3", True, (0, 0, 0)), 20, toolbox_size[1] + 400, logical_menu)
        MenuText(standard.render("Source Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 430,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 460, "source_ip_1", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 190, toolbox_size[1] + 460, "ext_port_3", (clickable, logical_menu))
        MenuText(standard.render("Destination Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 490,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 520, "dst_ip_3", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 190, toolbox_size[1] + 520, "internal_port_3", (clickable, logical_menu))

    def simulate(self):
        pass


class Router(Hardware):  # class for routers
    def __init__(self, groups):
        image = pyg.Surface((30, 30))
        image.fill("CYAN")
        Nic(self, 10, -5)
        super().__init__(image, groups)

    def logical_click(self):
        for X in [X for X in logical_menu]: X.kill()
        # create menu to set external ip and port forwarding rules
        # create static menu elements
        MenuText(standard.render("External IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 60, "ip", logical_menu, (logical_menu, clickable))
        MenuText(standard.render("Port Forwarding", True, (0, 0, 0)), 20, toolbox_size[1] + 110, logical_menu)

        MenuText(standard.render("Rule 1", True, (0, 0, 0)), 20, toolbox_size[1] + 150, logical_menu)
        MenuText(standard.render("External Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 180,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 210, "ext_ip_1", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 180, toolbox_size[1] + 210, "ext_port_1", (clickable, logical_menu))
        MenuText(standard.render("Internal Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 240,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 270, "int_ip_1", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 180, toolbox_size[1] + 270, "int_port_1", (clickable, logical_menu))

        MenuText(standard.render("Rule 2", True, (0, 0, 0)), 20, toolbox_size[1] + 320, logical_menu)
        MenuText(standard.render("External Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 350,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 380, "ext_ip_2", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 180, toolbox_size[1] + 380, "ext_port_2", (clickable, logical_menu))
        MenuText(standard.render("Internal Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 410,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 440, "int_ip_2", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 180, toolbox_size[1] + 440, "int_port_2", (clickable, logical_menu))

        MenuText(standard.render("Rule 3", True, (0, 0, 0)), 20, toolbox_size[1] + 490, logical_menu)
        MenuText(standard.render("External Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 520,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 550, "ext_ip_3", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 180, toolbox_size[1] + 550, "ext_port_3", (clickable, logical_menu))
        MenuText(standard.render("Internal Ip Address and Port", True, (0, 0, 0)), 20, toolbox_size[1] + 580,
                 logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 610, "int_ip_3", logical_menu, (logical_menu, clickable))
        MenuEntry(self, 5, 180, toolbox_size[1] + 610, "int_port_3", (clickable, logical_menu))

    def simulate(self):
        pass


class Nic(pyg.sprite.Sprite):  # class for NIC's
    def __init__(self, parent, x_off, y_off):
        self.ip, self.netmask, self.gateway = "...", "...", "..."
        self.image = pyg.image.load("NIC.png")
        self.parent, self.x_off, self.y_off, self.active, self.type, self.ip = parent, x_off, y_off, False, type, "..."
        super().__init__(NICs)  # create parent class and add to NIC group
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
        for X in [X for X in logical_menu]: X.kill()
        # create menu to set ip, netmask and gateway
        # create static menu elements
        MenuText(standard.render("IP address", True, (0, 0, 0)), 20, toolbox_size[1] + 20, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 60, "ip", logical_menu, (logical_menu, clickable))
        MenuText(standard.render("Netmask", True, (0, 0, 0)), 20, toolbox_size[1] + 110, logical_menu)
        QuadOctetEntry(self, 20, toolbox_size[1] + 150, "netmask", logical_menu, (logical_menu, clickable))
        MenuText(standard.render("Default gateway", True, (0, 0, 0)), 20, toolbox_size[1] + 200, logical_menu)
        if len([X.gateway for X in NICs if X.parent == self.parent and (X.gateway != "..." and X != self)]) > 0:
            QuadOctetEntry(self, 20, toolbox_size[1] + 240, "gateway", logical_menu, (logical_menu, clickable), True)
        else:
            QuadOctetEntry(self, 20, toolbox_size[1] + 240, "gateway", logical_menu, (logical_menu, clickable))


class MenuButton(pyg.sprite.Sprite):  # class for physical menu buttons
    def __init__(self, image, xpos, ypos, group, cmd):
        self.active = False  # needed for compatibility
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
        self.active = False  # needed for compatibility
        super().__init__(group)
        self.image = image
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = xpos, ypos


class MenuEntry(pyg.sprite.Sprite):  # class for menu numeric text entries
    def __init__(self, parent, length, xpos, ypos, var, group):
        self.active, self.parent, self.length, self.xpos, self.ypos, self.var = False, parent, length, xpos, ypos, var
        if self.length == 3: self.max_value = 256  # inhibit impossible values
        if self.length == 5: self.max_value = 65536
        super().__init__(group)  # call parent class
        try:
            self.parent.__getattribute__(self.var)  # test if parent var already exists
        except:
            self.parent.__setattr__(self.var, "")  # create parent var
        self.image = standard.render(self.parent.__getattribute__(self.var).ljust(self.length, " "), True, (0, 0, 0),
                                     (255, 255, 255))  # draw from parent var and pad with spaces
        self.rect = self.image.get_rect()  # update rect
        self.rect.x, self.rect.y = self.xpos, self.ypos

    def logical_click(self):  # if clicked in logical mode
        if self.active:  # if active (selected)
            self.active = False  # deselect
            self.image = standard.render(self.parent.__getattribute__(self.var).ljust(self.length, " "), True,
                                         (0, 0, 0), (255, 255, 255))  # redraw
        else:  # if not holding
            if holding(): [X for X in clickable if X.active][0].logical_click()  # deselect anything else
            self.active = True  # make active
            self.image = standard.render(self.parent.__getattribute__(self.var).ljust(self.length, " "), True,
                                         (0, 0, 0), (200, 200, 200))  # redraw

    def keyboard_event(self, event):  # if keystroke while active
        print(event.key)
        # if 0-9 are pressed and there is space to type them
        if 47 < event.key < 58 and len(self.parent.__getattribute__(self.var).strip()) < self.length:
            if int(self.parent.__getattribute__(self.var) + event.unicode) < self.max_value:  # if value is legal
                self.parent.__setattr__(self.var,  # update parent var
                                        (self.parent.__getattribute__(self.var).strip() + event.unicode))
                self.image = standard.render(self.parent.__getattribute__(self.var).ljust(self.length, " "), True,
                                             (0, 0, 0), (200, 200, 200))  # redraw
                self.rect = self.image.get_rect()  # update rect
                self.rect.x, self.rect.y = self.xpos, self.ypos
            try:
                self.parent.callback()  # quad octet uses callback to update itself when entry is updates
            except:
                pass  # "raw" entries dont have a callback class
        if event.key == 8:  # if backspace is pressed
            self.parent.__setattr__(self.var, self.parent.__getattribute__(self.var).strip()[0:-1])  # remove last char
            self.image = standard.render(self.parent.__getattribute__(self.var).ljust(self.length, " "), True,
                                         (0, 0, 0), (200, 200, 200))  # redraw
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.xpos, self.ypos
            try:
                self.parent.callback()
            except:
                pass
        if event.key == 27: # esc key
            self.logical_click()
        if event.key == 9:
            try:
                self.parent.callback #  test for quad octet
                self.logical_click()
                next = self.var[0]
                for X in [X for X in logical_menu]:
                    if X.parent == self.parent:
                        pass #  TODO tab order code
            except:
                pass



class QuadOctetEntry(pyg.sprite.Sprite):  # helper class for quad octet based entries
    def __init__(self, parent, xpos, ypos, var, group, child_group, disabled=False):
        self.parent, self.xpos, self.ypos, self.var, self.disabled = parent, xpos, ypos, var, disabled
        if disabled:
            self.image = standard.render("   .   .   .   ", True, (0, 0, 0), (60, 60, 60))
            super().__init__(group)  # call parent
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.xpos, self.ypos
        else:
            try:  # test if parent already has var set
                octs = self.parent.__getattribute__(self.var).strip().split(".")
                self.oct1, self.oct2, self.oct3, self.oct4 = octs[0], octs[1], octs[2], octs[3]  # load octets
                self.oct1e = MenuEntry(self, 3, self.xpos, self.ypos, "oct1", child_group)  # make entries
                self.oct2e = MenuEntry(self, 3, self.xpos + 24, self.ypos, "oct2", child_group)
                self.oct3e = MenuEntry(self, 3, self.xpos + 48, self.ypos, "oct3", child_group)
                self.oct4e = MenuEntry(self, 3, self.xpos + 72, self.ypos, "oct4", child_group)
                self.callback()  # call callback to accommodate entries
            except:  # if the var doesnt exist
                self.parent.__setattr__(self.var, "...")  # set the var
                self.oct1e = MenuEntry(self, 3, self.xpos, self.ypos, "oct1", child_group)  # make entries
                self.oct2e = MenuEntry(self, 3, self.xpos + 24, self.ypos, "oct2", child_group)
                self.oct3e = MenuEntry(self, 3, self.xpos + 48, self.ypos, "oct3", child_group)
                self.oct4e = MenuEntry(self, 3, self.xpos + 72, self.ypos, "oct4", child_group)
            self.image = standard.render(self.oct1.ljust(3, " ") + "." + self.oct2.ljust(3, " ")  # set the image (dots)
                                         + "." + self.oct3.ljust(3, " ") + "." + self.oct4.ljust(3, " "), True,
                                         (0, 0, 0))
            super().__init__(group)  # call parent
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.xpos, self.ypos

    def callback(self):  # used to update parent class and accommodate entries
        # combine octets into quad octet
        self.parent.__setattr__(self.var, self.oct1 + "." + self.oct2 + "." + self.oct3 + "." + self.oct4)
        self.image = standard.render(self.oct1.ljust(3, " ") + "." + self.oct2.ljust(3, " ")  # redraw
                                     + "." + self.oct3.ljust(3, " ") + "." + self.oct4.ljust(3, " "), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.xpos, self.ypos
        self.oct2e.rect.x = self.oct1e.rect.x + self.oct1e.rect.width + 6  # cascade spacing along the octets for dots
        self.oct3e.rect.x = self.oct2e.rect.x + self.oct2e.rect.width + 6
        self.oct4e.rect.x = self.oct3e.rect.x + self.oct3e.rect.width + 6


class MenuSelector:
    def __init__(self, items, parent, xpos, ypos, var, subgroup):
        self.items, self.parent, self.xpos, self.ypos, self.var, self.subgroup \
            = items, parent, xpos, ypos, var, subgroup
        try:
            self.selection = self.parent.__getattribute__(self.var)
        except:
            self.selection = []
        for Y, X in enumerate(self.items):
            if Y in self.selection:
                self.Selection(Y, X, self.xpos, self.ypos + (35 * (Y + 1)), self.subgroup, self, True)
            else:
                self.Selection(Y, X, self.xpos, self.ypos + (35 * (Y + 1)), self.subgroup, self, False)

    def callback(self):
        self.parent.__setattr__(self.var, self.selection)
        print(self.selection)

    class Selection(pyg.sprite.Sprite):
        def __init__(self, id, lable, xpos, ypos, group, parent, state):
            self.id, self.lable, self.xpos, self.ypos, self.group, self.parent = id, lable, xpos, ypos, group, parent
            self.active, self.selected = False, state
            if self.selected:
                self.image = standard.render(self.lable, True, (0, 0, 0), (200, 200, 200))
            else:
                self.image = standard.render(self.lable, True, (0, 0, 0), (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.xpos, self.ypos
            super().__init__(group)

        def logical_click(self):
            if self.selected:
                self.selected = False
                self.image = standard.render(self.lable, True, (0, 0, 0), (255, 255, 255))
                self.parent.selection.remove(self.id)
            else:
                self.selected = True
                self.image = standard.render(self.lable, True, (0, 0, 0), (200, 200, 200))
                self.parent.selection.append(self.id)
            self.parent.callback()


class Packet(pyg.sprite.Sprite):
    def __init__(self, src, dst, i_dst):
        super().__init__(packets)
        self.src, self.dst, self.i_src, self.i_dst, self.bearing = src, dst, src, i_dst, 0
        self.image = pyg.Surface((4, 4))
        self.image.fill("Blue")
        self.dist, self.traveling = 0, True
        src_point = (
        self.i_src.rect.x + (self.i_src.rect.width / 2) - 2, self.i_src.rect.y + (self.i_src.rect.height / 2) - 2)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = src_point[0], src_point[1]

    def update(self):
        if self.traveling:
            self.dist += packet_speed
            src_point = (
            self.i_src.rect.x + (self.i_src.rect.width / 2) - 2, self.i_src.rect.y + (self.i_src.rect.height / 2) - 2)
            dst_point = (
            self.i_dst.rect.x + (self.i_dst.rect.width / 2) - 2, self.i_dst.rect.y + (self.i_dst.rect.height / 2) - 2)
            self.bearing = math.degrees(math.atan2(dst_point[1] - src_point[1], dst_point[0] - src_point[0])) + 270
            self.rect.x, self.rect.y = src_point[0] - self.dist * math.sin(math.radians(self.bearing)), \
                                       src_point[1] + self.dist * math.cos(math.radians(self.bearing))
            if self.rect.colliderect(self.dst.rect):
                self.traveling = False


def draw():
    global state
    screen.fill("WHITE")  # blank the screen
    for X in connections:  # draw the connection lines
        pyg.draw.line(screen, (0, 0, 0), (X[0].rect.x + 5, X[0].rect.y + 5), (X[1].rect.x + 5, X[1].rect.y + 5), 3)
    hardware_group.draw(screen)  # draw the hardware
    NICs.draw(screen)  # draw the NIC's (need to do separately to ensure they afe drawn over the hardware)
    packets.draw(screen)  # draw the packets
    screen.blit(toolbox, toolbox_size)  # draw te toolbox
    if state == "physical":  # if in physical mode
        physical_menu.draw(screen)  # draw the menu buttons
        for X in [X for X in NICs if X.active]:  # if drawing a connection, draw a line between the nic and the mouse
            pyg.draw.line(screen, (0, 0, 0), (X.rect.x + 5, X.rect.y + 5), pyg.mouse.get_pos(), 3)
    if state == "logical":  # if in logical mode
        logical_menu.draw(screen)  # draw the menu
    screen.blit(state_button, state_button_size)  # draw the state button
    pyg.display.flip()  # flip the screen buffer
    clock.tick(60)  # wait 1/60th of a second from the last time a frame was drawn


def main():  # main gameloop function
    global campos, speed, toolbox, toolbox_size, state_button, state_button_size, connections, state
    running = True  # set gameloop vars
    dragging = False
    drag_cords = [[0, 0], [0, 0]]
    connections = []

    # create the toolbox surface
    toolbox_size = (0, screen.get_height() / 10, (screen.get_width() / 10) * 2, (screen.get_height() / 10) * 8)
    toolbox = pyg.Surface(toolbox_size[2:], pyg.SRCALPHA)
    toolbox.fill(color=(0, 0, 0, 128))  # colour the toolbox surface

    # create state button
    state_button_size = ((screen.get_width() / 10) * 8, (screen.get_height() / 10) * 8, (screen.get_width() / 10),
                         (screen.get_height() / 10))
    state_button = pyg.Surface(state_button_size[2:], pyg.SRCALPHA)

    # create menu buttons for endpoint, server, switch, firewall and router
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
        toolbox.fill(color=(0, 0, 0, 128))  # clear the toolbox and state button
        state_button.fill(color=(0, 0, 0, 128))
        state_button_text = large.render("Physical", True, (0, 0, 0, 128))  # draw state button text
        state_button.blit(state_button_text, (state_button_size[2] / 2 - state_button_text.get_width() / 2,
                                              state_button_size[3] / 2 - state_button_text.get_height() / 2))
        while state == "physical" and running:  # while the game is in physical mode
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
                        if pyg.rect.Rect(state_button_size).collidepoint(event.pos):  # if state button was clicked
                            if not holding():  # if not holding
                                state = "logical"  # flip states
                                break  # break event loop
                        for X in [X for X in NICs] + [X for X in clickable]:  # for the nics and the clickable group
                            if X.rect.collidepoint(event.pos):  # if it was clicked
                                try:
                                    X.physical_click()  # call the clicked function
                                except AttributeError:
                                    pass  # not everything has a click function in physical mode
                                break  # stop looking for collisions
                        else:  # if nothing was clicked
                            dragging = True  # start dragging the canvas
                            drag_cords = (pyg.mouse.get_pos(), campos.copy())
                    if event.button == pyg.BUTTON_RIGHT:  # if the right mouse button was pressed
                        try:
                            [X for X in NICs if X.active][0].active = False  # if holding a wire, stop
                        except IndexError:
                            pass  # don't crash if not holding a wire
                if event.type == pyg.MOUSEBUTTONUP:  # if a mouse button was released
                    if event.button == pyg.BUTTON_LEFT:  # if the left mouse button was released
                        dragging = False  # stop dragging the canvas
                hardware_group.update()  # redraw the hardware assets (probably have moved)
                NICs.update()  # update the NIC's (move with the hardware)
            if dragging:  # if dragging the canvas, move the camera with the mouse
                campos[0] = pyg.mouse.get_pos()[0] + drag_cords[1][0] - drag_cords[0][0]
                campos[1] = pyg.mouse.get_pos()[1] + drag_cords[1][1] - drag_cords[0][1]
            for X in [X for X in hardware_group]: X.simulate()
            packets.update()
            draw()  # call for the game to draw a frame

        toolbox.fill(color=(0, 0, 0, 128))  # clear the toolbox
        state_button.fill(color=(0, 0, 0, 128))  # clear the state button
        state_button_text = large.render("Logical", True, (0, 0, 0, 128))  # draw the state button text
        state_button.blit(state_button_text, (state_button_size[2] / 2 - state_button_text.get_width() / 2,
                                              state_button_size[3] / 2 - state_button_text.get_height() / 2))
        while state == "logical" and running:  # while the game is in logical mode
            for event in pyg.event.get():  # For Every Event
                if event.type == pyg.QUIT:  # Break on quit button
                    running = False
                if event.type == pyg.KEYDOWN:  # if a keyboard key is pressed
                    if holding():  # if holding (a menu element)
                        [X for X in clickable if X.active][0].keyboard_event(event)  # pass event to element
                    else:  # if not holding a menu element
                        if event.key == pyg.K_w:    campos = [campos[0], campos[1] + speed]  # move with wasd
                        if event.key == pyg.K_a:    campos = [campos[0] + speed, campos[1]]
                        if event.key == pyg.K_s:    campos = [campos[0], campos[1] - speed]
                        if event.key == pyg.K_d:    campos = [campos[0] - speed, campos[1]]
                        if event.key == pyg.K_ESCAPE: running = False  # Break on esc
                if event.type == pyg.MOUSEBUTTONDOWN:  # if a mouse button was pressed
                    if pyg.rect.Rect(state_button_size).collidepoint(event.pos):  # if the state button was pressed
                        state = "physical"  # change state to physical
                        if holding(): [X for X in clickable if X.active][
                            0].active = False  # if holding ,drop whatever is held
                        break  # stop looking for collisions
                    for X in [X for X in NICs] + [X for X in clickable]:  # for the nics and the clickable group
                        if X.rect.collidepoint(event.pos):  # if it was clicked
                            try:
                                X.logical_click()  # call the clicked function
                                break
                            except AttributeError:  # not everything has a logical click function
                                pass
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
            for X in [X for X in hardware_group]: X.simulate()
            packets.update()
            draw()


if __name__ == "__main__":
    campos = [0, 0]  # set camera origin
    speed = 30  # set distance of wasd presses
    state = "physical"  # start the game in physical UI mode
    packet_speed = 1
    pyg.init()  # initialise pygame
    screen = pyg.display.set_mode((0, 0), (pyg.FULLSCREEN | pyg.SRCALPHA))  # create the screen object
    clock = pyg.time.Clock()  # create a frameclock object
    # create sprite groups for the hardware, the physical menu, the logical menu, clickable elements and NIC's
    hardware_group, physical_menu, logical_menu, clickable, NICs, packets = \
        pyg.sprite.Group(), pyg.sprite.Group(), pyg.sprite.Group(), pyg.sprite.Group(), pyg.sprite.Group(), pyg.sprite.Group(),
    # nics need a separate group to ensure they get click and draw z priority
    holding = lambda: bool([X for X in [X for X in NICs] + [X for X in clickable] if X.active])
    # function to determine if any instances have the held flag set
    large = pyg.font.SysFont("arial", 40)  # create type objects to use ingame
    standard = pyg.font.SysFont("arial", 25)
    main()  # call the main gameloop

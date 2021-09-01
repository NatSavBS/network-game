import pygame as pyg
import math

class Packet(pyg.sprite.Sprite):
    def __init__(self, src, dst, i_dst):
        super().__init__(packets)
        self.src, self.dst, self.i_src, self.i_dst = src, dst, src, i_dst
        self.image = pyg.Surface((4, 4))
        self.image.fill("Blue")
        self.dist, self.traveling = 0, True
        src_point = (self.i_src.rect.x + (self.i_src.rect.width / 2) - 2, self.i_src.rect.y + (self.i_src.rect.height / 2) - 2)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = src_point[0], src_point[1]

    def update(self):
        if self.traveling:
            self.dist += packet_speed
            src_point = (self.i_src.rect.x + (self.i_src.rect.width / 2) - 2, self.i_src.rect.y + (self.i_src.rect.height / 2) - 2)
            dst_point = (self.i_dst.rect.x + (self.i_dst.rect.width / 2) - 2, self.i_dst.rect.y + (self.i_dst.rect.height / 2) - 2)
            self.bearing = math.degrees(math.atan2(dst_point[1] - src_point[1], dst_point[0] - src_point[0])) + 270
            self.rect.x, self.rect.y = src_point[0] - self.dist * math.sin(math.radians(self.bearing)), \
                                       src_point[1] + self.dist * math.cos(math.radians(self.bearing))
            if self.rect.colliderect(dst.rect):
                self.traveling = False


packet_speed = 1
pyg.init()
screen = pyg.display.set_mode((0, 0), (pyg.FULLSCREEN | pyg.SRCALPHA))
running = True
packets = pyg.sprite.Group()

clock = pyg.time.Clock()

src, dst = pyg.sprite.Sprite(), pyg.sprite.Sprite()
spr_surf = pyg.Surface((20, 20))
spr_surf.fill("green")
src.image, dst.image = spr_surf, spr_surf
src.rect, dst.rect = pyg.rect.Rect(100, 100, 20, 20), pyg.rect.Rect(100, 200, 20, 20)
sprites = pyg.sprite.Group(src, dst)

t_p = Packet(src, dst, dst)

while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                running = False

    screen.fill("white")
    packets.update()
    sprites.draw(screen)
    packets.draw(screen)
    pyg.display.flip()
    clock.tick(60)
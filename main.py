import pygame as pyg

def main():
    pyg.init()
    screen = pyg.display.set_mode((500, 500))
    clock = pyg.time.Clock()
    while True:
        clock.tick(60)

if __name__ == "__main__":
    main()
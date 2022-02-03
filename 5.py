import os
import sys

import pygame
import requests
import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
lll = '49.214913 53.556812'


def main():
    global lll
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(100, 100, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        print("Введите воординату через пробел")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        lll = text
                        text = ''
                        done = True
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)


def draw_map(ll, spn):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll[0]},{ll[1]}8&spn={spn},{spn}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

if __name__ == '__main__':
    main()
    pygame.init()
    pygame.display.init()

    clock = pygame.time.Clock()

    size = WIDTH, HEIGHT = 600, 450
    screen = pygame.display.set_mode(size)

    ll = lll.split(' ')
    spn = 0.005

    draw_map(ll, spn)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    spn += 0.001 if spn < 0.009 else 0
                    draw_map(ll, spn)
                elif event.key == pygame.K_PAGEUP:
                    spn -= 0.001 if spn > 0.001 else 0
                    draw_map(ll, spn)
                elif event.key == pygame.K_UP:
                    ll[1] += 0.001
                    draw_map(ll, spn)
                elif event.key == pygame.K_DOWN:
                    ll[1] -= 0.001
                    draw_map(ll, spn)
                elif event.key == pygame.K_LEFT:
                    ll[0] -= 0.001
                    draw_map(ll, spn)
                elif event.key == pygame.K_RIGHT:
                    ll[0] += 0.001
                    draw_map(ll, spn)
                print(spn)
        pygame.display.flip()
        clock.tick(60)

os.remove('map.png')
import os
import sys

import pygame
import requests


def draw_map(ll, spn, mode):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll[0]},{ll[1]}8&spn={spn},{spn}&l={mode}"
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


def draw_text(screen):
    map_text = pygame.font.Font(None, 30).render('схема', True, 'black')
    sat_text = pygame.font.Font(None, 30).render('спутник', True, 'black')
    skl_text = pygame.font.Font(None, 30).render('гибрид', True, 'black')
    screen.blit(map_text, (5, 5, 57, 11))
    screen.blit(sat_text, (5, 25, 78, 11))
    screen.blit(skl_text, (5, 45, 71, 11))


if __name__ == '__main__':
    pygame.init()
    pygame.display.init()

    clock = pygame.time.Clock()

    size = WIDTH, HEIGHT = 600, 450
    screen = pygame.display.set_mode(size)

    ll = [49.214913, 53.556812]
    spn = 0.005
    mode = 'map'

    draw_map(ll, spn, mode)
    draw_text(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    spn += 0.001 if spn < 0.009 else 0
                    draw_map(ll, spn, mode)
                    draw_text(screen)
                elif event.key == pygame.K_PAGEUP:
                    spn -= 0.001 if spn > 0.001 else 0
                    draw_map(ll, spn, mode)
                    draw_text(screen)
                elif event.key == pygame.K_UP:
                    ll[1] += 0.001
                    draw_map(ll, spn, mode)
                    draw_text(screen)
                elif event.key == pygame.K_DOWN:
                    ll[1] -= 0.001
                    draw_map(ll, spn, mode)
                    draw_text(screen)
                elif event.key == pygame.K_LEFT:
                    ll[0] -= 0.001
                    draw_map(ll, spn, mode)
                    draw_text(screen)
                elif event.key == pygame.K_RIGHT:
                    ll[0] += 0.001
                    draw_map(ll, spn, mode)
                    draw_text(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 5 <= event.pos[0] <= 62 and \
                        5 <= event.pos[1] <= 16:
                    mode = 'map'
                    draw_map(ll, spn, mode)
                    draw_text(screen)
                elif 5 <= event.pos[0] <= 83 and \
                        25 <= event.pos[1] <= 36:
                    mode = 'sat'
                    draw_map(ll, spn, mode)
                    draw_text(screen)
                if 5 <= event.pos[0] <= 76 and \
                        45 <= event.pos[1] <= 56:
                    mode = 'sat,skl'
                    draw_map(ll, spn, mode)
                    draw_text(screen)
        pygame.display.flip()
        clock.tick(60)

os.remove('map.png')

import os
import sys

import pygame
import requests


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
    pygame.init()
    pygame.display.init()

    clock = pygame.time.Clock()

    size = WIDTH, HEIGHT = 600, 450
    screen = pygame.display.set_mode(size)

    ll = [49.214913, 53.556812]
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
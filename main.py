from mapapi_PG import show_map
import pygame

n1 = input()
n2 = input()
ll_spn = f'll={n1},{n2}8&spn=0.016457,0.00619'
pygame.init()
screen = pygame.display.set_mode((600, 450))
show_map(ll_spn)
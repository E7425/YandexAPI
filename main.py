import os
import sys

import pygame
import requests

map_request = "http://static-maps.yandex.ru/1.x/?ll=135.746300,-27.483800&spn=18,18&l=map"
response = requests.get(map_request)


map_file = "australia.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((550, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
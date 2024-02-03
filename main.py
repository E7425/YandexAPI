import sys

import pygame
import requests


def get_params(json_data, z=18, l="map"):
    toponym = json_data["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "l": l,
        "z": str(z),
    }
    return map_params


toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    exit(0)
json_response = response.json()
map_params = get_params(json_response)
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
spn = (0.005, 0.005)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

z = 1
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN or event.key == pygame.K_PAGEUP:
                if event.key == pygame.K_PAGEDOWN:
                    z -= 1
                    if z < 1:
                        z = 1
                if event.key == pygame.K_PAGEUP:
                    z += 1
                    if z > 21:
                        z = 21
                map_params = get_params(json_response, z=z)
                response = requests.get(map_api_server, params=map_params)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
pygame.quit()

import sys

import pygame
import requests

run = True

fl = True


def get_params(toponym_longitude, toponym_lattitude, z=18):
    map_params = {
        "ll": ",".join([str(toponym_longitude), str(toponym_lattitude)]),
        "z": str(z),
        "l": "map",
    }
    return map_params


toponym_to_find = " ".join(sys.argv[1:])
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
response = requests.get(geocoder_api_server, params=geocoder_params)
z = 18


def z_to_degrees(z):
    tile_size = 256
    degrees = 360 / (2 ** z * tile_size / 700)
    return degrees


if not response:
    exit(0)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
toponym_longitude = float(toponym_longitude)
toponym_lattitude = float(toponym_lattitude)

map_params = get_params(toponym_longitude, toponym_lattitude)
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"

with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
screen = pygame.display.set_mode((550, 450))
screen.blit(pygame.image.load_extended(map_file), (0, 0))
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:

            if event.key == pygame.K_LEFT:
                toponym_longitude -= z_to_degrees(z)
                if toponym_longitude < 0:
                    toponym_longitude = 0
            if event.key == pygame.K_RIGHT:
                toponym_longitude += z_to_degrees(z)
                if toponym_longitude > 180:
                    toponym_longitude = 180
            if event.key == pygame.K_DOWN:
                toponym_lattitude -= z_to_degrees(z)
                if toponym_lattitude < 0:
                    toponym_lattitude = 0
            if event.key == pygame.K_UP:
                toponym_lattitude += z_to_degrees(z)
                print(toponym_lattitude, toponym_longitude)
                if toponym_lattitude > 180:
                    toponym_lattitude = 180
                    print(toponym_lattitude, toponym_longitude)
            map_params = get_params(toponym_longitude, toponym_lattitude, z=z)
            response = requests.get(map_api_server, params=map_params)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            screen.blit(pygame.image.load_extended(map_file), (0, 0))

        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_PAGEDOWN or event.key == pygame.K_PAGEUP):
            if event.key == pygame.K_PAGEDOWN:
                z -= 1
                if z < 1:
                    z = 1
            if event.key == pygame.K_PAGEUP:
                z += 1
                if z > 21:
                    z = 21
            map_params = get_params(toponym_longitude, toponym_lattitude, z=z)
            response = requests.get(map_api_server, params=map_params)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

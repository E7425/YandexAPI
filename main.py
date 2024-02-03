import sys

import pygame
import requests

run = True

toponym = json_data["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
argshir = toponym_longitude
argdolg = toponym_lattitude

pygame.init()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                argshir += 10
            if event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_DOWN:
                pass
            if event.key == pygame.K_UP:
                pass


    def get_params(json_data, spn=("0.005", "0.005")):
        toponym = json_data["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join(spn),
            "l": "map",
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

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    pygame.init()
    screen = pygame.display.set_mode((550, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.flip()
pygame.quit()

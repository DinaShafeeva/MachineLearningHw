import numpy as np
import pygame
from sklearn.svm import SVC
import random


def getLineCoordinates(svc):
    w = svc.coef_[0]
    a = -w[0] / w[1]
    xx = np.array([0, width])
    yy = a * xx - (svc.intercept_[0]) / w[1]

    return [xx[0], yy[0]], [xx[-1], yy[-1]]


def generateData(point_count_in_class, class_count):
    radius = 50
    data = []
    for classNum in range(class_count):
        center_x, center_y = random.randint(radius, width - radius), random.randint(radius, height - radius)
        for rowNum in range(point_count_in_class):
            data.append([[random.gauss(center_x, radius / 2), random.gauss(center_y, radius / 2)], classNum])
    return data


def draw_pygame():
    screen = pygame.display.set_mode((width, height))

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = list(event.pos)
                cls = svc.predict([pos])[0]
                points.append([pos, cls])
        for point in points:
            pygame.draw.circle(screen, colors[point[1]], point[0], 3)

        pygame.draw.line(screen, 'blue', p1, p2, 1)
        pygame.display.update()


if __name__ == '__main__':
    width = 600
    height = 400
    colors = {-1: 'red', 1: 'green'}

    points = generateData(10, 2)

    for point in points:
        if point[1] == 0:
            point[1] = -1

    x_coordinates = np.array(list(map(lambda x: x[0], points)))
    y_coordinates = np.array(list(map(lambda x: x[1], points)))
    svc = SVC(kernel='linear')
    svc.fit(x_coordinates, y_coordinates)

    p1, p2 = getLineCoordinates(svc)

    draw_pygame()

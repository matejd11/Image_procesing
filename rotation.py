#!/usr/bin/python

import sys
from PIL import Image
from math import *

def generateMatrix(alfa):
    alfa = radians(alfa)
    return [[float(cos(alfa)), float(-sin(alfa))],[float(sin(alfa)),float(cos(alfa))]]

def getHightAndWidth(sizex, sizey, angle):

    diagonal = sqrt(sizex**2 + sizey**2)
    diagonalAngle = atan(sizex/sizey)
    print(diagonal, diagonalAngle)

    heigh1 = ceil(diagonal * sin(radians(angle) - diagonalAngle))
    heigh2 = ceil(diagonal * sin(radians(180 - angle) - diagonalAngle))

    if heigh1 > heigh2:
        newHeigh = heigh1
    else: 
        newHeigh = heigh2

    width1 = ceil(diagonal * cos(radians(angle) - diagonalAngle))
    width2 = ceil(diagonal * cos(radians(180 - angle) - diagonalAngle))

    if width1 > width2:
        newWidth = width1
    else: 
        newWidth = width2


    return newHeigh, newWidth

def half(img, sizex, sizey):
    tmp = [[[0,0,0] for x in range(sizex)] for y in range(sizey)]

    for row in range(sizex):
        for col in range(sizey):
            tmp[int(col-(sizey/2))][int(row-(sizex/2))] = [int((img[row, col])[0]), int((img[row, col])[1]), int((img[row, col])[2])]

    return tmp

def transform(i, j, grid, width, hight):
    newi = (i) * grid[0][0]
    newi += (j) * grid[0][1]
    
    newj = (i) * grid[1][0]
    newj += (j) * grid[1][1]
    return int(round(newi)), int(round(newj))

def main(inputFile = "input", outputFile = "output", alfa = 90):
    im = Image.open(inputFile + '.png', 'r')
    pix_val = im.load()

    a, b = getHightAndWidth(im.size[0], im.size[1], alfa)

    matrix = generateMatrix(alfa)
    #imx = im.size[0]+int(sin(radians(alfa))*im.size[1])
    #imy = im.size[1]+int(sin(radians(alfa))*im.size[0])

    imx = a
    imy = b

    newData = [[[0,0,0] for x in range(imx)] for y in range(imy)]

    k = int(imx/2)
    l = int(imy/2)

    for i in range(im.size[1]):
        for j in range(im.size[0]):
            newi, newj = transform(i, j, matrix, im.size[0], im.size[1])
            if k+newi >= 0 and k+newi < len(newData):
                if l+newj >= 0 and l+newj < len(newData[0]):
                    newData[newi][newj] = [(pix_val[j, i])[0], (pix_val[j, i])[1], (pix_val[j, i])[2]]

    newData = half(pix_val, im.size[0], im.size[1])
    newConvertedData = []
    for x in range(len(newData)):
        newConvertedData += [tuple(pixel) for pixel in newData[x]]

    new = Image.new('RGB', [imx, imy])
    #new = Image.new('RGB', im.size)
    new.putdata(newConvertedData)
    new.save(outputFile + '.png', 'PNG')

if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
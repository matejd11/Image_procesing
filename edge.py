#!/usr/bin/python

import sys
from PIL import Image
from math import *

def hor(size):
    if size == 1:
        return 8, [[1,0,-1],[2,0,-2],[1,0,-1]] 
    if size == 2:
        return 46, [[1,2,0,-2,-1],[2,3,0,-3,-2],[3,4,0,-4,-3],[2,3,0,-3,-2],[1,2,0,-2,-1]] 

def ver(size):
    if size == 1:
        return 8,[[1,2,1],[0,0,0],[-1,-2,-1]] 
    if size == 2:
        return 46, [[1,2,3,2,1],[2,3,4,3,2],[0,0,0,0,0],[-2,-3,-4,-3,-2],[-1,-2,-3,-2,-1]] 

def getValue(size, pixels, j, i, grid, div):
    sum = [0.0 for x in range(3)]
    for x in range(3):
        for k in range(len(grid)):
            for l in range(len(grid[k])):
                ii = i + k - len(grid)/2 + 1 
                jj = j + l - len(grid)/2 + 1
                if ii > 0 and ii < size[0]:
                    if jj > 0 and jj < size[1]:
                        sum[x] += grid[k][l] * (pixels[ii, jj])[x]
    sum[0] = abs(int(sum[0]))
    sum[1] = abs(int(sum[1]))
    sum[2] = abs(int(sum[2]))

    d = int((sum[0] + sum[1] + sum[2]) / 3)

    sum[0] = d
    sum[1] = d
    sum[2] = d

    return sum

def main(inputFile = "skuska", outputFile = "skuska3", data = 1):
    im = Image.open(inputFile + '.png', 'r')
    pix_val = im.load()

    supervalue, grid = hor(data)

    newDataHor = [[0 for x in range(im.size[0])] for x in range(im.size[1])]
    for i in range(im.size[1]):
        for j in range(im.size[0]):
            newDataHor[i][j] = getValue(im.size, pix_val, i, j, grid, supervalue)
    newConvertedDataHor = []
    for x in range(len(newDataHor)):
        newConvertedDataHor += [tuple(pixel) for pixel in newDataHor[x]]
    newHor = Image.new('RGB', im.size)
    newHor.putdata(newConvertedDataHor)
    newHor.save(outputFile+"h" + '.png', 'PNG')
    
    supervalue, grid = ver(data)
    newDataVer = [[0 for x in range(im.size[0])] for x in range(im.size[1])]
    for i in range(im.size[1]):
        for j in range(im.size[0]):
            newDataVer[i][j] = getValue(im.size, pix_val, i, j, grid, supervalue)
    newConvertedDataVer = []
    for x in range(len(newDataVer)):
        newConvertedDataVer += [tuple(pixel) for pixel in newDataVer[x]]
    newVer = Image.new('RGB', im.size)
    newVer.putdata(newConvertedDataVer)
    newVer.save(outputFile+"v" + '.png', 'PNG')

    newData = [[0 for x in range(im.size[0])] for x in range(im.size[1])]
    for i in range(im.size[1]):
        for j in range(im.size[0]):
            a = int(sqrt(newDataHor[i][j][0]**2 + newDataVer[i][j][0]**2))
            b = int(sqrt(newDataHor[i][j][1]**2 + newDataVer[i][j][1]**2))
            c = int(sqrt(newDataHor[i][j][2]**2 + newDataVer[i][j][2]**2))
            if a+b+c != 0:
                d = int((a+b+c)/3)
            else:
                d = int(0)
            newData[i][j] = [d, d, d]
    newConvertedData = []
    for x in range(len(newData)):
        newConvertedData += [tuple(pixel) for pixel in newData[x]]
    new = Image.new('RGB', im.size)
    new.putdata(newConvertedData)
    new.save(outputFile + '.png', 'PNG')


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
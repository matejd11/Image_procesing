#!/usr/bin/python

import sys
from PIL import Image
from math import *

def getWindow(filter, dataA, dataB):
    if "inversegaussian" in filter:
        return inverseGaussianBlure(dataA, dataB)
    elif "gaussian" in filter:
        return gaussianBlure(dataA, dataB)
    elif "box" in filter:
        return boxBlure(dataA)
    else:
        print("unknown type of blure. exiting...")
        return

def boxBlure(size):
    size *= 2
    size += 1
    return [[1 for x in range(size)] for x in range(size)] 

def gaussianBlure(size, slope):
    size *= 2
    size += 1
    res = [[0.0 for x in range(size)] for x in range(size)]
    for i in range(size):
        for j in range(size):
            x = int(i - (size-1)/2.0)
            y = int(j - (size-1)/2.0)
            xx = abs(x)
            yy = abs(y)
            val = ((xx + yy)/(size-1))
            res[i][j] = 1 - tanh(val*slope)
    return  res

def inverseGaussianBlure(size, slope):
    size *= 2
    size += 1
    res = [[0.0 for x in range(size)] for x in range(size)]
    for i in range(size):
        for j in range(size):
            x = int(i - (size-1)/2.0)
            y = int(j - (size-1)/2.0)
            xx = abs(x)
            yy = abs(y)
            val = ((xx + yy)/(size-1))
            res[i][j] = tanh(val*slope)
    return  res

def getaverage(size, pixels, j, i, grid):
    sum = [0.0 for x in range(3)]
    for x in range(3):
        count = 0.0
        for k in range(len(grid)):
            for l in range(len(grid[k])):
                ii = i + k - len(grid)/2 + 1 
                jj = j + l - len(grid)/2 + 1
                if ii > 0 and ii < size[0]:
                    if jj > 0 and jj < size[1]:
                        sum[x] += grid[k][l] * (pixels[ii, jj])[x]
                        count += grid[k][l]
        if count != 0:
            sum[x] = int(sum[x] / count)
        else:
            sum[x] = 0
    return sum

def applyBlure(data, size, grid):
    newData = [[0.0 for x in range(size[0])] for x in range(size[1])]
    for i in range(size[1]):
        for j in range(size[0]):
            newData[i][j] = getaverage(size, data, i, j, grid)
    return newData

def loadImage(name):
    im = Image.open(name + '.png', 'r')
    pix_val = im.load()
    return im, pix_val

def saveImage(data, size, name, grid):
    newData = []
    for x in range(len(data)):
        newData += [tuple(pixel) for pixel in data[x]]
    new = Image.new('RGB', size)
    new.putdata(newData)
    new.save(name + '.png', 'PNG')    

def main(inputFile = "input", outputFile = "output", filter = "box", dataA = 1, dataB = 1):
    im, pix_val = loadImage(inputFile)

    window = getWindow(filter, dataA, dataB)

    newData = applyBlure(pix_val, im.size, window)

    saveImage(newData, im.size, outputFile, window)

if __name__ == '__main__':
    if len(sys.argv) == 6:
        main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    elif len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()

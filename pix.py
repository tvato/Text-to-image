#!/usr/bin/python3

"""
Script to save text into an image.
Works by converting char ASCII codes into RGBA value (first char to R, second to G and so on).
Can be also used to convert from image back to text.
"""

from PIL import Image
import math
import sys

def getImage(fileName):
	return Image.open(fileName)

def getPixels(im):
	return im.load()

def readText(fileName):
	with open(fileName, "r") as f:
		data = f.read()

	return data

def getTextChunks(data):
	chunks = []
	for i in range(0, len(data), 4):
		sub = []
		for j in range(4):
			try:
				sub.append(ord(data[i+j]))
			except IndexError:
				sub.append(ord('\0'))
		chunks.append(tuple(sub))

	return chunks

def saveText(fileName, data):
	with open(fileName, "w") as f:
		f.write(data)

def modifyImage(pix, im, chunks):
	x_dim = im.size[0]
	y_dim = im.size[1]

	i = 0

	for x in range(x_dim):
		for y in range(y_dim):
			if i >= len(chunks):
				pix[x,y] = (0,0,0,0)
			else:
				pix[x,y] = chunks[i]
				i += 1

	return pix


def readImage(im, pix):
	x_dim = im.size[0]
	y_dim = im.size[1]

	data = ""

	for x in range(x_dim):
		for y in range(y_dim):
			for i in range(4):
				if(chr(pix[x,y][i]) != '\0'):
					data += chr(pix[x,y][i])

	return data

def imageDimFromTextLen(data):
	dim = math.ceil(					# round up, to fit everything
		math.sqrt(						# square root for square image
			math.ceil(len(data) / 4)	# divide by 4 so we get pixel count
			)
		)

	return dim

def newImage(mode, width, height):
	im = Image.new(mode, (width, height))

	return im

def saveImage(im, fileName):
	im.save(fileName)

def textToImage(textFile):
	data = readText(textFile)
	chunks = getTextChunks(data)
	dim = imageDimFromTextLen(data)
	im = newImage("RGBA", dim, dim)
	pix = getPixels(im)
	newPix = modifyImage(pix, im, chunks)
	saveImage(im, f"{textFile[:-4]}.png")

def imageToText(imageFile):
	im = getImage(imageFile)
	pix = getPixels(im)
	data = readImage(im, pix)
	saveText(f"{imageFile[:-4]}.txt", data)

def main():
    c = sys.argv[1]
    if c == "-t":
        try:
            textToImage(sys.argv[2])
        except IndexError:
            print("Usage: -t <textfile>")
    elif c == "-i":
        try:
            imageToText(sys.argv[2])
        except IndexError:
            print("Usage: -i <imagefile>")
    else:
        print("""Usage: python3 pix.py <arg> <file>\n\targs:\n\t-t <textfile>\n\t\tconvert text file to image\n\t-i <imagefile>\n\t\tconvert image file to text""")

if __name__ == "__main__":
    main()

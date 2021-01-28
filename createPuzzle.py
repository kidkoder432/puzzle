# Puzzle Maker
# Makes a puzzle and structure out of an image


# Imports
import json
import pickle
import random
from PIL import Image
import pyautogui

SCREENSIZE = pyautogui.size()

# Get the size of the pieces


def getPieceSize(im):
    print(
        "Note: Each piece of the puzzle is a square.\nIf the size of the image cannot create a whole number of pieces, the extra pixels will be cropped.\nIf the image is too big for your screen, it will be resized to fit your screen."
    )
    pieceSize = int(
        input("How big should I make each piece? Please enter the size in pixels. > ")
    )
    numPieces = (im.width // pieceSize) * (im.height // pieceSize)
    while numPieces <= 1:
        pieceSize = int(
            input(
                "How big should I make each piece? Please enter the size in pixels. > "
            )
        )
        numPieces = (im.width // pieceSize) * (im.height // pieceSize)
        print(
            "Sorry, the size of your piece is bigger than the size of the image. Please try again."
        )
    return pieceSize


# Make the pieces


def makePieces(im, pieceSize):
    pieceArray = []
    for y in range((im.height // pieceSize)):
        pieceArray.append([])
        for x in range((im.width // pieceSize)):
            newPiece = im.crop((x * pieceSize, y * pieceSize, (x + 1) * (pieceSize), (y + 1) * pieceSize))
            pieceArray[-1].append(newPiece)
    return pieceArray


def loadPuzzle(pieceArray, pieceSize, shuffle=False):
    arr = pieceArray[:]
    print(len(pieceArray[0]), len(pieceArray))
    puzzle = Image.new(
        'RGB', (len(pieceArray[0]) * (pieceSize + 1), len(pieceArray) * (pieceSize + 1)))
    pieceY = 0
    pieces = arr
    if shuffle:
        random.shuffle(arr)
        for x in arr:
            random.shuffle(x)
        #createPieceStrPickle(arr, 'shuffledPieceStr.pickle')
        pieces = arr
    for y in pieces:
        pieceX = 0
        for piece in y:
            puzzle.paste(piece, (pieceX, pieceY))
            pieceX += (pieceSize + 1)
        pieceY += (pieceSize + 1)
    return puzzle


def resizeImageToFitWindow(img, pieceSize):
    if img.width + 0 > SCREENSIZE[0]:
        img = img.resize((int(img.width * (SCREENSIZE[0] / (img.width + 0))), int(img.height * (SCREENSIZE[0] / (img.width + 0)))))
    if img.height + 0 > SCREENSIZE[1]:
        img = img.resize((int(img.width * (SCREENSIZE[1] / (img.height + 0))), int(img.height * (SCREENSIZE[1] / (img.height + 0)))))
    return img


def convertPiecesToRGB(pieceArray):
    rgbArray = []
    for row in pieceArray:
        rgbArray.append([])
        for piece in row:
            print(piece)
            rgbArray[-1].append([])
            for py in range(piece.width):
                rgbArray[-1][-1].append([])
                for px in range(piece.height):
                    rgbArray[-1][-1][-1].append(piece.getpixel((px, py)))
    return rgbArray


def createPieceStrPickle(pieceArray, fn='pieceStr.pickle'):
    pieceStr = []
    for y in pieceArray:
        pieceStr.append([])
        for piece in y:
            pieceStr[-1].append(piece.tobytes())
    with open(fn, 'wb') as f:
        pickle.dump(pieceStr, f)


def createNumArray(w, h):
    return [[x for x in range(w)] for y in range(h)]


def main():
    # Get the image name and open the image
    imageName = input(
        "Which image would you like to convert into a puzzle? The image must be in the images directory. For example: forest.jpg > "
    )
    im = Image.open("images/" + imageName)
    print(im.size)
    print(im.size)
    pieceSize = getPieceSize(im)
    im = resizeImageToFitWindow(im, pieceSize)
    shuffle = (
        input('Should I shuffle the pieces? (y or n) > ').lower().startswith('y'))
    pieceArray = makePieces(im, pieceSize)
    print(pieceArray[0][0])
    with open('pieceArray.json', 'w') as f:
        json.dump({'imageFilePath': 'images/' + imageName, 'screenSize': SCREENSIZE, 'puzzlePixelSize': [im.width, im.height], 'puzzlePieceSize': [im.width // pieceSize, im.height // pieceSize], 'pieceSize': pieceSize, 'puzzleSize': [im.width // pieceSize, im.height // pieceSize], 'data': convertPiecesToRGB(
            pieceArray)}, f, indent=0)

    numPieces = (im.width // pieceSize) * (im.height // pieceSize)
    print(
        f"Created a {im.width // pieceSize} by {im.height // pieceSize} puzzle with {numPieces} pieces"
    )
    createPieceStrPickle(pieceArray)
    puzzle = loadPuzzle(pieceArray, pieceSize, shuffle)
    print(pieceArray[0][0])
    puzzle.save('puzzleGridShuffled.png')



if __name__ == "__main__":
    main()

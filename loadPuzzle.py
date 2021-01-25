import json
from PIL import Image

data = json.load(open('pieceArray.json'))
puzzleWidth, puzzleHeight = data['puzzlePieceSize']
pieceSize = data['pieceSize']

im = Image.new('RGB', ((pieceSize + 1) * puzzleWidth, (pieceSize + 1) * puzzleHeight))
print(im.size)
pieces = data['data']
pieceY = 0
for py, pieceRow in enumerate(pieces):
    pieceX = 0
    for px, piece in enumerate(pieceRow[:-1]):
        for y, pixelRow in enumerate(piece):
            for x, pixel in enumerate(pixelRow):
                try:
                    im.putpixel((pieceX + x, pieceY + y), tuple(pixel))
                except IndexError:
                    print(x, y, px, py)
        pieceX += (pieceSize + 1)
    pieceY += (pieceSize + 1)

# im = im.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
im.save('puzzleGrid.png')
print('Done.')
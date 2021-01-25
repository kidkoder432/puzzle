import pickle
import json
import pygame
from pygame.locals import *
import os; os.environ['SDL_VIDEO_WINDOW_POS'] = '100, 100'
import ctypes
pygame.init()
print(ctypes.windll.user32.SetProcessDPIAware())

pieceSize = json.load(open('pieceArray.json'))['pieceSize']
puzzleWidth, puzzleHeight = json.load(open('pieceArray.json'))[
    'puzzlePieceSize']

displayPieceSize = int(pieceSize * 0.7)
window = pygame.display.set_mode(
    (puzzleWidth * (displayPieceSize + 1), puzzleHeight * (displayPieceSize + 1)))


pieces = []
pieceImages = pickle.load(open('pieceStr.pickle', 'rb'))
for y, r in enumerate(pieceImages):
    for x, pieceImage in enumerate(r):
        pieces.append({'pos': [x * (displayPieceSize + 1), y * (displayPieceSize + 1)], 'img': pygame.image.frombuffer(
            pieceImage, (pieceSize, pieceSize), 'RGB').convert()})


clock = pygame.time.Clock()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    pygame.quit()
                    exit(0)
                return

puzzleSize = (puzzleWidth * (displayPieceSize + 1), puzzleHeight * (displayPieceSize + 1))
puzzle = pygame.Surface(puzzleSize)

for piece in pieces:
    img = piece['img']
    img = pygame.transform.scale(img, (20, 20))
    imgRect = img.get_rect()
    imgRect.topleft = piece['pos']
    puzzle.blit(img, imgRect)

puzzleRect = pygame.Rect(
    0, 0, puzzleWidth * (pieceSize + 1), puzzleHeight * (pieceSize + 1))
puzzleRect.topleft = (0, 0)
print(puzzleRect, puzzle, window)
window.blit(puzzle, puzzleRect)



while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit(0)
    pygame.display.flip()



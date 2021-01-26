import ctypes
import pickle
import random
import json
import pygame
from pygame.locals import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100, 100'
pygame.init()
print(ctypes.windll.user32.SetProcessDPIAware())

font = pygame.font.SysFont(None, 48)
pieceSize = json.load(open('pieceArray.json'))['pieceSize']
puzzleWidth, puzzleHeight = json.load(open('pieceArray.json'))[
    'puzzlePieceSize']

displayPieceSize = int(pieceSize * 0.7)
window = pygame.display.set_mode(
    (puzzleWidth * (displayPieceSize + 1), (puzzleHeight - 1) * (displayPieceSize + 1)))


def pause(key=K_ESCAPE):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == key:
                    paused = False


def message(text, px, py):
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    for l in text.split('\n'):
        tr = font.render(l, 1, (255, 255, 255), (0, 0, 0)).get_rect()
        tr.center = (px, py)
        window.blit(font.render(l, 1, (255, 255, 255), (0, 0, 0)), tr)
        py += fontHeight


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


solvedPieces = []
solvedPieceImages = pickle.load(open('pieceStr.pickle', 'rb'))

solvedPuzzleImg = pygame.image.load(
    json.load(open('pieceArray.json'))['imageFilePath'])
solvedPuzzleImg = pygame.transform.scale(
    solvedPuzzleImg, (int(solvedPuzzleImg.get_width() * 0.7), int(solvedPuzzleImg.get_height() * 0.7)))

for y, r in enumerate(solvedPieceImages):
    for x, pieceImage in enumerate(r):
        solvedPieces.append({'pos': [x * (displayPieceSize + 1), y * (displayPieceSize + 1)], 'img': pygame.image.frombuffer(
            pieceImage, (pieceSize, pieceSize), 'RGB').convert()})

pieces = []
pieceImages = pickle.load(open('shuffledPieceStr.pickle', 'rb'))

for y, r in enumerate(pieceImages):
    for x, pieceImage in enumerate(r):
        pieces.append({'pos': [x * (displayPieceSize + 1), y * (displayPieceSize + 1)], 'img': pygame.image.frombuffer(
            pieceImage, (pieceSize, pieceSize), 'RGB').convert()})


clock = pygame.time.Clock()

pieceClicked = None
pieceSwapped = None
clickpos = 0


puzzleSize = (puzzleWidth * (displayPieceSize + 1),
              puzzleHeight * (displayPieceSize + 1))
puzzle = pygame.Surface(puzzleSize)

message('''PUZZLE GAME
Instructions:
Click and drag a piece to another piece to swap them
Press I to view the puzzle image, and press I to stop viewing
Press H to show this screen
Press S to solve the puzzle
Press ESC to quit
Press P to pause
Press any key to start''', window.get_rect().centerx, window.get_rect().centery - 100)
pygame.display.flip()
waitForPlayerToPressKey()
window.fill(0)
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
        if event.type == QUIT:
            pygame.quit()
            exit(0)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
            if event.key == K_i:
                window.fill(0)

                rect = solvedPuzzleImg.get_rect()
                rect.center = window.get_rect().center
                window.blit(solvedPuzzleImg, rect)
                pygame.display.flip()
                pause(K_i)
            if event.key == K_h:
                window.fill(0)
                message('''PUZZLE GAME
Instructions:
Click and drag a piece to another piece to swap them
Press I to view the puzzle image, and press I to stop viewing
Press H to show this screen
Press S to solve the puzzle
Press ESC to quit
Press P to pause
Press any key to continue''', window.get_rect().centerx, window.get_rect().centery - 100)
                pygame.display.flip()
                waitForPlayerToPressKey()

            if event.key == K_p:
                window.fill(0)
                message('''Paused
Press any key to resume''', window.get_rect().centerx, window.get_rect().centery)
                pygame.display.flip()
                waitForPlayerToPressKey()


        if event.type == MOUSEBUTTONDOWN:
            for piece in pieces:
                p = piece['pos']
                if event.pos[0] in range(p[0], p[0] + displayPieceSize + 1) and event.pos[1] in range(p[1], p[1] + displayPieceSize + 1):
                    clickpos = p
                    pieceClicked = piece

        elif event.type == MOUSEBUTTONUP:
            for piece in pieces:
                s = piece['pos']
                if event.pos[0] in range(s[0], s[0] + displayPieceSize + 1) and event.pos[1] in range(s[1], s[1] + displayPieceSize + 1):
                    swapPos = s
                    pieceSwapped = piece
                    if pieceClicked and pieceSwapped:
                        pieceClicked['pos'] = swapPos
                        pieceSwapped['pos'] = clickpos
                        print('swapped', pieceClicked, 'and', pieceSwapped)
                        pieceSwapped, pieceClicked, clickpos, swapPos = None, None, None, None

    for piece in pieces:
        img = piece['img']
        img = pygame.transform.scale(img, (20, 20))
        imgRect = img.get_rect()
        imgRect.topleft = piece['pos']
        puzzle.blit(img, imgRect)
    window.blit(puzzle, puzzleRect)

    if pieces == solvedPieces:
        print('YOU WIN')
    pygame.display.flip()

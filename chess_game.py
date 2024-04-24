import pygame
import chess
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os

pygame.init()

WIDTH, HEIGHT = 512, 512
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
LIGHT_BROWN = (205, 133, 63)
PIECE_DIRECTORY = "PR24MVDBACSAJR/images/figures/"

board = chess.Board()

piece_images = {}
pieces = ['bishop', 'king', 'knight', 'pawn', 'queen', 'rook']
for piece in pieces:
    svg_file = f'images/{piece}_svg_withShadow.svg'
    try:
        drawing = svg2rlg(svg_file)
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        renderPM.drawToFile(drawing, f'{piece}.png', fmt="PNG")
        piece_images[piece] = pygame.image.load(f'{piece}.png')
    except Exception as e:
        print(f"Failed to load input file: {svg_file} ({e})")

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

def draw_board():
    colors = [WHITE, LIGHT_BROWN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

"""def draw_pieces():
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece is not None:
                fen = board.fen()
                ranks = fen.split()[0].split('/')
                piece_name = ranks[7 - row][col]
                piece_name = piece_name.lower() if piece.color == chess.BLACK else piece_name.upper()
                try:
                    piece_path = f"{PIECE_DIRECTORY}{'b' if piece.color == chess.BLACK else 'w'}_{pieces[piece.piece_type]}_svg_withShadow.svg"
                    piece_image = pygame.image.load(piece_path)
                    win.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                except pygame.error as e:
                    print(f"Failed to load input file: {piece_path} ({e})")"""

def draw_pieces():
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece is not None:
                fen = board.fen()
                ranks = fen.split()[0].split('/')
                piece_name = ranks[7 - row][col]
                piece_name = piece_name.lower() if piece.color == chess.BLACK else piece_name.upper()
                try:
                    piece_path = f"{PIECE_DIRECTORY}{'b' if piece.color == chess.BLACK else 'w'}_{pieces[piece.piece_type]}_svg_withShadow.svg"
                    piece_image = pygame.image.load(piece_path)
                    win.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                except pygame.error as e:
                    print(f"Failed to load input file: {piece_path} ({e})")





def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board()
        draw_pieces()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

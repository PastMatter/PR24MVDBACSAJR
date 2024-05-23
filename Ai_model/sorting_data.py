import chess
import chess.pgn
from stockfish import Stockfish
import pandas as pd
import numpy as np

# Initialize Stockfish
stockfish = Stockfish("c:\\Users\\mvuck\\AppData\\Local\\Temp\\Rar$EXa608.43681\\stockfish\\stockfish-windows-x86-64-sse41-popcnt.exe")

def evaluate_position(fen):
    stockfish.set_fen_position(fen)
    evaluation = stockfish.get_evaluation()
    if evaluation['type'] == 'cp':
        return evaluation['value']  
    elif evaluation['type'] == 'mate':
        return 1000 * np.sign(evaluation['value'])  
    return 0

def parse_pgn(pgn_file):
    positions = []
    with open(pgn_file) as f:
        i=0
        while True:
            print(f'Game: {i}')
            game = chess.pgn.read_game(f)
            if game is None:
                break
            board = game.board()
            for move in game.mainline_moves():
                fen = board.fen()
                board.push(move)
                black_score = evaluate_position(fen)
                positions.append({
                    'id': len(positions),
                    'board': fen,
                    'black_score': black_score,
                    'best_move': move.uci()
                })
            i+=1    
    return positions


positions = parse_pgn('Carlsen.pgn')


df = pd.DataFrame(positions)

df.to_csv('positions.csv', index=False)

print(f"Saved {len(df)} positions to magnus_pos.csv")

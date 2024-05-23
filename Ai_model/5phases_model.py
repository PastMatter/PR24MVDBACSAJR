import chess
from IPython.display import SVG, display
import numpy as np
import pandas as pd
import tensorflow as tf
from stockfish import Stockfish


def play_game(ai_function):
    board = chess.Board()

    while board.outcome() is None:
        display(SVG(board._repr_svg_()))

        if board.turn == chess.WHITE:
            user_move = input('Your move in UCI format (e2e4): ')
            if user_move == 'quit':
                break
            while user_move not in [str(move) for move in board.legal_moves]:
                print('Please enter valid move!')
                user_move = input('Your move in UCI format (e2e4): ')
            board.push_san(user_move)    

        elif board.turn == chess.BLACK:
            ai_move = ai_function(board.fen())
            print(f'AI move: {ai_move}')
            board.push_san(ai_move)
        print(str(board))
    print(board.outcome())


def one_hot_encoded_piece(piece):
    pieces = list('rnbqkpRNBQKP.')
    array = np.zeros(len(pieces))
    pieces_to_idx = {p: i for i, p in enumerate(pieces)}
    index = pieces_to_idx[piece]
    array[index] = 1
    return array


def encode_board(board):
    board_str = str(board)
    board_str = board_str.replace(' ', '')
    board_list = []
    for row in board_str.split('\n'):
        row_list = []
        for piece in row:
            row_list.append(one_hot_encoded_piece(piece))
        board_list.append(row_list)
    return np.array(board_list)


def encode_fen_string(fen_str):
    board = chess.Board(fen=fen_str)
    return encode_board(board)


df = pd.read_csv('adj_magnus_pos_with_phases.csv', index_col='id')

opening_df = df[df['phase'] == 'opening']
postopening_df = df[df['phase'] == 'postopening']
middlegame_df = df[df['phase'] == 'middlegame']
postmiddlegame_df = df[df['phase'] == 'postmiddlegame']
endgame_df = df[df['phase'] == 'endgame']

def prepare_data(df):
    X = np.stack(df['board'].apply(encode_fen_string))
    y = df['black_score']
    return X, y

def split_data(df):
    train_df = df.sample(frac=0.8, random_state=42)
    val_df = df.drop(train_df.index)
    return train_df, val_df

opening_train_df, opening_val_df = split_data(opening_df)
postopening_train_df, postopening_val_df = split_data(postopening_df)
middlegame_train_df, middlegame_val_df = split_data(middlegame_df)
postmiddlegame_train_df, postmiddlegame_val_df = split_data(postmiddlegame_df)
endgame_train_df, endgame_val_df = split_data(endgame_df)

datasets = {
    'opening': (opening_train_df, opening_val_df),
    'postopening': (postopening_train_df, postopening_val_df),
    'middlegame': (middlegame_train_df, middlegame_val_df),
    'postmiddlegame': (postmiddlegame_train_df, postmiddlegame_val_df),
    'endgame': (endgame_train_df, endgame_val_df)
}

def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        #tf.keras.layers.Dropout(0.2),
        #tf.keras.layers.Dense(256, activation='relu'),
        #tf.keras.layers.Dropout(0.3),
        #tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='rmsprop', loss='mean_squared_error')
    return model

models = {}
histories = {}

for phase, (train_df, val_df) in datasets.items():
    X_train, y_train = prepare_data(train_df)
    X_val, y_val = prepare_data(val_df)
    
    model = build_model()
    history = model.fit(X_train, y_train, epochs=15, validation_data=(X_val, y_val))
    
    models[phase] = model
    histories[phase] = history

stockfish = Stockfish(path="c:\\Users\\mvuck\\AppData\\Local\\Temp\\Rar$EXa2208.42793\\stockfish\\stockfish-windows-x86-64-sse41-popcnt.exe")

def play_nn(fen, show_move_evaluation=True):
    board = chess.Board(fen=fen)

    ply_count = board.fullmove_number * 2 - 1 if board.turn == chess.BLACK else board.fullmove_number * 2
    
    if ply_count <= 8:
        model = models['opening']
    elif 8 < ply_count <= 15:
        model = models['postopening']
    elif 15 < ply_count <= 25:
        model = models['middlegame']
    elif 25 < ply_count <= 45:
        model = models['postmiddlegame']
    else:
        model = models['endgame']

    moves = []
    input_vectors = []
    for move in board.legal_moves:
        candidate_board = board.copy()
        candidate_board.push(move)
        moves.append(move)
        input_vectors.append(encode_board(str(candidate_board)).astype(np.int32))

    input_vectors = np.stack(input_vectors)

    scores = model.predict(input_vectors, verbose=0)

    if board.turn == chess.BLACK:
        index_of_best_move = np.argmax(scores)
    else:
        index_of_best_move = np.argmax(-scores)

    best_move = moves[index_of_best_move]

    if show_move_evaluation:
        for move, score in zip(moves, scores):
            print(f"Move: {move}, Score: {score}")

    stockfish.set_fen_position(board.fen())
    original_evaluation = stockfish.get_evaluation()['value']

    board.push(best_move)
    stockfish.set_fen_position(board.fen())
    new_evaluation = stockfish.get_evaluation()['value']
    
    evaluation_drop = original_evaluation - new_evaluation
    print(f'New_eval: {new_evaluation}, original_eval: {original_evaluation}')

    if evaluation_drop < 15.0:  
        print(f"Move {best_move} drops the evaluation by {evaluation_drop} centipawns. Looking for alternatives...")
        
        scores[index_of_best_move] = -99999999 if board.turn == chess.BLACK else 99999999
        
        while evaluation_drop < 40.0:
            if board.turn == chess.BLACK:
                index_of_best_move = np.argmax(scores)
            else:
                index_of_best_move = np.argmax(-scores)
            
            best_move = moves[index_of_best_move]
            print(f'New best move: {best_move}')

            board.pop()  
            board.push(best_move)
            stockfish.set_fen_position(board.fen())
            new_evaluation = stockfish.get_evaluation()['value']
            
            evaluation_drop = original_evaluation - new_evaluation
            print(f'new_eval: {new_evaluation}, curr_eval: {original_evaluation}, eval_drop: {evaluation_drop}')

            if evaluation_drop >= -40.0:
                print(f'Chosen Move: {best_move}')
                break

            scores[index_of_best_move] = -99999999 if board.turn == chess.BLACK else 99999999

    return str(best_move)

play_game(play_nn)

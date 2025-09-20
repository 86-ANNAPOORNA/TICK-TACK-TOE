from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Initialize game state
games = {}

@app.route('/start', methods=['POST'])
def start_game():
    game_id = len(games)
    games[game_id] = {'board': [' ']*9, 'turn': 'X', 'mode': 'multi'}
    return jsonify({'game_id': game_id})

@app.route('/start_ai', methods=['POST'])
def start_game_ai():
    game_id = len(games)
    games[game_id] = {'board': [' ']*9, 'turn': 'X', 'mode': 'ai'}
    return jsonify({'game_id': game_id})

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    game_id = data['game_id']
    position = data['position']

    if games[game_id]['board'][position] == ' ':
        games[game_id]['board'][position] = games[game_id]['turn']
        winner = check_winner(games[game_id]['board'])
        if winner or ' ' not in games[game_id]['board']:
            reset_game(game_id)
        else:
            games[game_id]['turn'] = 'O' if games[game_id]['turn'] == 'X' else 'X'
            if games[game_id]['mode'] == 'ai' and games[game_id]['turn'] == 'O':
                ai_move(game_id)
        return jsonify({'board': games[game_id]['board'], 'winner': winner})
    return jsonify({'error': 'Invalid move'})

def ai_move(game_id):
    board = games[game_id]['board']
    available_moves = [i for i, x in enumerate(board) if x == ' ']
    position = random.choice(available_moves)
    board[position] = 'O'
    winner = check_winner(board)
    if winner or ' ' not in board:
        reset_game(game_id)
    else:
        games[game_id]['turn'] = 'X'  # Switch turn back to player

def check_winner(board):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None

def reset_game(game_id):
    games[game_id]['board'] = [' ']*9
    games[game_id]['turn'] = 'X'

if __name__ == '__main__':
    app.run(debug=True)

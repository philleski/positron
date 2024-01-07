import json
import random
import sys

import chess
import chess.pgn

if len(sys.argv) != 4:
    print("Usage: python make_pgn.py num_positions input_file output_file")
    print("Example: python make_pgn.py 10 lichess_db_eval_filtered.json sample.pgn")
    raise Exception

num_positions = int(sys.argv[1])
input_file = sys.argv[2]
output_file = sys.argv[3]

all_positions = open(input_file).read().split('\n')
positions = random.sample(all_positions, num_positions)

with open(output_file, 'w') as output_file_handle:
    for position_str in positions:
        position = json.loads(position_str)
        fen = position['fen']
        pv = position['pv']
        game = chess.pgn.Game()
        game.setup(fen)
        line = [chess.Move.from_uci(uci) for uci in pv.split(' ')]
        game.add_line(line)
        print(game, file=output_file_handle)
        print('', file=output_file_handle)

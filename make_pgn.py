import argparse
import json
import random
import sys

import chess
import chess.pgn

parser = argparse.ArgumentParser(description='Make PGN file out of a random subset of filtered positions')
parser.add_argument('input_file')
parser.add_argument('output_file')
parser.add_argument('-n', '--num-positions', type=int, default=10, help='number of positions to include in PGN file')

args = parser.parse_args()

all_positions = open(args.input_file).read().split('\n')
positions = random.sample(all_positions, args.num_positions)

with open(args.output_file, 'w') as output_file_handle:
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

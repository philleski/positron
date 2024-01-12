import argparse
import json
import sys

import chess
import chess.pgn

parser = argparse.ArgumentParser(description='Filter chess positions to get interesting ones for study')
parser.add_argument('input_file')
parser.add_argument('output_file')
parser.add_argument('-c', '--ceiling', type=int, default=150, help='max centipawns for absolute value of second-best line')
parser.add_argument('-d', '--diff', type=int, default=80, help='min difference between best and second-best line in centipawns')
parser.add_argument('-n', '--num-lines', type=int, default=None, help='number of lines to read from the input file, useful for testing')

args = parser.parse_args()

def eval_pv(pv):
    if 'mate' in pv:
        if pv['mate'] > 0:
            return 10 ** 6 - pv['mate']
        return -10 ** 6 + pv['mate']
    return pv['cp']

positions = []
with open(args.input_file) as input_file_handle:
    with open(args.output_file, 'w') as output_file_handle:
        for ctr, line in enumerate(input_file_handle):
            if args.num_lines is not None and ctr > args.num_lines:
                break
            position = json.loads(line)
            fen = position['fen']
            game = chess.pgn.Game()
            try:
                game.setup(fen)
            except ValueError:
                continue
            turn = game.board().turn
            pvs = [pv for evaluation in position['evals'] for pv in evaluation['pvs']]
            if len(pvs) < 2:
                continue
            if turn == chess.WHITE:
                pvs = sorted(pvs, key=lambda pv: -eval_pv(pv))
            else:
                pvs = sorted(pvs, key=lambda pv: eval_pv(pv))
            if abs(eval_pv(pvs[0]) - eval_pv(pvs[1])) < args.diff:
                # Only publish positions where the best PV is substantially better than the second-best PV.
                continue
            if abs(eval_pv(pvs[1])) > args.ceiling:
                # Positions where the second-best line is very strong are typically very easy, so filter them out.
                continue
            position_new = {'fen': fen, 'pv': pvs[0]['line']}
            print(json.dumps(position_new), file=output_file_handle)

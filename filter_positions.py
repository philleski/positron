import json
import sys

import chess
import chess.pgn

if len(sys.argv) != 4:
    print("Usage: python filter_positions.py threshold_centipawns input_file output_file")
    print("Example: python filter_positions.py 80 lichess_db_eval.json lichess_db_eval_filtered.json")

threshold_centipawns = int(sys.argv[1])
input_file = sys.argv[2]
output_file = sys.argv[3]

def eval_pv(pv):
    if 'mate' in pv:
        if pv['mate'] > 0:
            return 10 ** 6 - pv['mate']
        return -10 ** 6 + pv['mate']
    return pv['cp']

positions = []
with open(input_file) as input_file_handle:
    with open(output_file, 'w') as output_file_handle:
        for ctr, line in enumerate(input_file_handle):
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
            if abs(eval_pv(pvs[0]) - eval_pv(pvs[1])) < threshold_centipawns:
                # Only publish positions where the best PV is substantially better than the second-best PV.
                continue
            position_new = {'fen': fen, 'pv': pvs[0]['line']}
            print(json.dumps(position_new), file=output_file_handle)

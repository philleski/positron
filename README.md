# Positron
Filters a list of evaluated chess positions and creates PGNs from that list.

This is done in two parts. First we run filter_positions.py to take the list of lichess open database evaluations and pare down to a subset of higher quality positions. This process can take a few hours but only needs to be done once, as long as the criteria for selecting positions doesn't change. Next we run make_pgn.py on this intermediate filtered file to create a PGN out of randomly selected positions. This process normally finishes within seconds and can be done repeatedly. From this PGN one can go over the positions and select the best quality ones manually.

## Setup

1. Install python, recommended version 3.11 or later.
2. Install the python-chess library: `pip install python-chess`
3. Download and unzip the lichess open database evaluations: https://database.lichess.org/#evals

## Filter Positions

This script goes through the lichess evaluations and selects the ones where the best evaluation minus the second best evaluation is over a certain threshold.

The filter positions script takes three command-line arguments:
1. threshold_centipawns: the minimum difference between the best evaluation and the second best evaluation, in order for a position to pass
2. input_file: the path to the (unzipped) input file, e.g. lichess_db_eval.json
3. output_file: the path to the intermediate output file that filter_positions.py will write to

Usage:
```
python filter_positions.py threshold_centipawns input_file output_file
```

Example:
```
python filter_positions.py 80 lichess_db_eval.json lichess_db_eval_filtered.json
```

## Make PGN

This script goes through the intermediate list of filtered positions, selects a random subset, and writes them to a PGN file.

The make PGN script takes three command-line arguments:
1. num_positions: the number of positions to select from the intermediate file and write to the PGN file
2. input_file: the path to the intermediate filtered positions file, the one written by filter_positions.py
3. output_file: the path to the output PGN file

Usage:
```
python make_pgn.py num_positions input_file output_file
```

Example:
```
python make_pgn.py 10 lichess_db_eval_filtered.json sample.pgn
```

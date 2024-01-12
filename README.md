# Positron
Filters a list of evaluated chess positions and creates PGNs from that list.

This is done in two parts. First we run filter_positions.py to take the list of lichess open database evaluations and pare down to a subset of higher quality positions. This process can take a few hours but only needs to be done once, as long as the criteria for selecting positions doesn't change. It is possible to run this script on only the beginning of the input file, adjusting the parameters until the quality is high enough. Next we run make_pgn.py on this intermediate filtered file to create a PGN out of randomly selected positions. This process normally finishes within seconds and can be done repeatedly. From this PGN one can go over the positions and select the best quality ones manually.

## Setup

1. Install python, recommended version 3.11 or later.
2. Install the python-chess library: `pip install python-chess`
3. Download and unzip the lichess open database evaluations: https://database.lichess.org/#evals

## Filter Positions

This script goes through the lichess evaluations and selects the ones where the best evaluation minus the second best evaluation is over a certain threshold.

The filter positions script takes two mandatory arguments and three optional arguments.

**Mandatory Arguments:**
1. input_file: the path to the (unzipped) input file, e.g. lichess_db_eval.json
2. output_file: the path to the intermediate output file that filter_positions.py will write to

**Optional Arguments:**
1. -c CEILING: max centipawns for absolute value of second-best line (default 150)
2. -d DIFF: min difference between best and second-best line in centipawns (default 80)
3. -n NUM_LINES: number of lines to read from the input file, useful for testing (default None)

**Usage:**
```
python filter_positions.py [-c CEILING] [-d DIFF] [-n NUM_LINES] <input_file> <output_file>
```

**Examples:**
```
# Run the script with defaults
python filter_positions.py lichess_db_eval.json lichess_db_eval_filtered.json

# Run the script quickly on the first 10,000 lines to check the quality of the positions
python filter_positions.py -n 10000 lichess_db_eval.json lichess_db_eval_filtered.json

# Run the script with ceiling 200 and diff 60
python filter_positions.py -c 200 -d 60 lichess_db_eval.json lichess_db_eval_filtered.json
```

## Make PGN

This script goes through the intermediate list of filtered positions, selects a random subset, and writes them to a PGN file.

The make PGN script takes two mandatory arguments and one optional argument.

**Mandatory Arguments:**
1. input_file: the path to the intermediate filtered positions file, the one written by filter_positions.py
2. output_file: the path to the output PGN file

**Optional Arguments:**
1. -n NUM_POSITIONS: the number of positions to select from the intermediate file and write to the PGN file (default 10)

**Usage:**
```
python make_pgn.py [-n NUM_POSITIONS] <input_file> <output_file>
```

**Examples:**
```
# Run the script with the defaults
python make_pgn.py lichess_db_eval_filtered.json sample.pgn

# Run the script, generating a PGN with 20 positions
python make_pgn.py -n 20 lichess_db_eval_filtered.json sample.pgn
```

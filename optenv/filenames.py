#!/usr/bin/env python3

import argparse
import parameters


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-e', '--experiment', choices=['zeroguess', 'rampdown'])
parser.add_argument('-t', '--type', choices=['optcontrols', 'reports'])
args = parser.parse_args()


print(' '.join(getattr(parameters, args.experiment)[args.type]))

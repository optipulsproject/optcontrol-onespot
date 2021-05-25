import argparse
import re
import numpy as np
from optipuls.visualization import plot_control


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
parser.add_argument('-i', '--infile')
args = parser.parse_args()


regex = re.compile(r'\d\d\d\d-\d.\d\d\d')
P_YAG, T = (lambda si, sf: (int(si), float(sf))) (
                *regex.search(args.infile).group().split('-'))

control = np.load(args.infile)

plot_control(control, outfile=args.outfile, size_inches=(T*200, P_YAG/750),
             title=f'P_YAG={P_YAG}, T={T:5.3f}')

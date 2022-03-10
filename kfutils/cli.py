#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals, division, print_function

import os
import sys
import logging
import textwrap
import argparse
import glob
import numpy as np


class CustomParser(argparse.ArgumentParser):

    def error(self, message):
        sys.stderr.write('\033[91mError: %s\n\033[0m' % message)
        self.print_help()
        sys.exit(2)


def listOfInts(val):
    try:
        val = int(val)
        if val < 0:
            raise ValueError
    except:
        raise argparse.ArgumentTypeError("Only list of positive are allowed")
    return val


def createParser():
    #main parser
    parser = CustomParser(prog="kutils",
                          formatter_class=argparse.RawTextHelpFormatter,
                          description="A tool for common file operations.")

    #adding options for numerical jobs
    parser.add_argument("--ifile",
                        '-i',
                        type=str,
                        help="File name",
                        metavar="FILE",
                        required=True)
    parser.add_argument('--ofile',
                        '-o',
                        type=str,
                        help="Output file name",
                        metavar="FILE")
    parser.add_argument('--cols',
                        '-c',
                        help="index of grid columns",
                        nargs='+',
                        metavar='COLS',
                        required=True,
                        type=listOfInts)
    parser.add_argument(
        '--rad2deg',
        '-rd',
        help="index of columns to convert to degree from radian",
        nargs='+',
        metavar='COLS',
        type=listOfInts)
    parser.add_argument('--deg2rad',
                        '-dr',
                        help="index of columns to convert to radian to degree",
                        nargs='+',
                        metavar='COLS',
                        type=listOfInts)
    parser.add_argument('--dropcols',
                        '-dc',
                        help="index of columns to drop",
                        nargs='+',
                        metavar='COLS',
                        type=listOfInts)
    return parser.parse_args()


def main():
    args = createParser()
    inpFile = args.ifile

    cols = args.cols

    # read file
    data = np.loadtxt(inpFile)

    # rad to deg
    if (args.rad2deg):
        data[:, args.rad2deg] = np.rad2deg(data[:, args.rad2deg])
    # deg to rad
    if (args.deg2rad):
        data[:, args.deg2rad] = np.deg2rad(data[:, args.deg2rad])
    # delete columns
    if (args.dropcols):
        data = np.delete(data, args.dropcols, axis=1)

    # now write file
    outFile = args.ofile
    if not outFile: outFile = inpFile + '_out'

    if len(cols) < 1:  #1D file
        np.savetxt(outFile, data, delimiter='\t', fmt='%.8f')
    else:
        with open(outFile, 'w') as f:
            for th in np.unique(data[:, cols[0]]):
                np.savetxt(f,
                           data[data[:, cols[0]] == th],
                           delimiter='\t',
                           fmt='%.8f')
                f.write('\n')

    print(f"File saved as {outFile}")

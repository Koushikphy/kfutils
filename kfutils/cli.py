#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals, division, print_function

import os
import sys
import logging
import textwrap
import argparse
import glob
import numpy as np

from funcs import *


__all__ = []


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
    parser.add_argument('-i', type=str, help="File name", metavar="FILE", required=True)
    parser.add_argument('-o', type=str, help="Output file name", metavar="FILE")
    parser.add_argument('-s', type=str, help="Stats about this file.", metavar="FILE")
    parser.add_argument('-c', help="index of grid columns", nargs='+', metavar='COLS', required=True, type=listOfInts)
    parser.add_argument('-rd', help="index of columns to convert to degree from radian",
                        nargs='+', metavar='COLS',type=listOfInts)
    parser.add_argument('-dr', help="index of columns to convert to radian to degree",
                        nargs='+', metavar='COLS', type=listOfInts)
    parser.add_argument('-dc', help="index of columns to drop", nargs='+', metavar='COLS', type=listOfInts)
    return parser.parse_args()


def main():
    args = createParser()
    inpFile = args.i

    cols = args.c

    # read file
    data = np.loadtxt(inpFile)

    # rad to deg
    if (args.rd):
        data[:, args.rd] = np.rad2deg(data[:, args.rd])
    # deg to rad
    if (args.dr):
        data[:, args.dr] = np.deg2rad(data[:, args.dr])
    # delete columns
    if (args.dc):
        data = np.delete(data, args.dc, axis=1)

    # now write file
    outFile = args.o
    if not outFile:
        outFile = "{}_out{}".format(*os.path.splitext(inpFile))

    if len(cols) == 1:  #1D file
        write1DFile(outFile, data)
    else:
        write2DFile(outFile, data, cols[0])



    print(f"File saved as {outFile}")


if __name__ == "__main__":
    main()
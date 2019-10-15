from __future__ import absolute_import, unicode_literals,division, print_function
__doc__='''

This python file parses the command line arguments associated with 'adt' command. It uses subparser either to
devise analytic functional forms of several adiabatic to diabatic transformation (ADT) quantities or to solve the
stiff ADT equations for any `N' coupled electronic states. While carrying out symbolic manipulation, it employes
the definitions of adt_analytic.py. On the other hand, adt_numeric.py is involved for numerical calculation of
ADT angles, ADT matrcies, diabatic potential energy matrices and residue of ADT angles. In order to monitor the
progress of a job, a auto-generated log file, 'ADT.log' is created during the execution.

Any user can easily get the help message by typing 'adt -h' for the overall outline of this program. On the other
hand, 'adt ana -h' or 'adt num -h' can be executed for more specific informations about analytical or numerical
jobs.

'''
__authors__  = '''
Koushik Naskar, Soumya Mukherjee, Bijit Mukherjee, Satyam Ravi, Saikat Mukherjee, Subhankar Sardar and Satrajit Adhikari
'''

import os
import sys
import logging
import textwrap
import argparse
import glob

#


class CustomParser(argparse.ArgumentParser):
    # subcommands are mandatory arguments in python 2 but not in python 3.
    # So, absence of any subcommand will throw an error in python 2 and thus
    # trigger this function to show the full manual but not in python 3
    def error(self, message):
        sys.stderr.write('\033[91mError: %s\n\033[0m' % message)
        self.print_help()
        sys.exit(2)



def make_logger(log_name):
    #Create the logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    # file = os.path.join(os.path.expanduser('~'), 'ADT.log' )
    fh = logging.FileHandler("ADT.log")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] - %(name)22s - [%(levelname)6s] - %(message)s","%d-%m-%Y %I:%M:%S %p")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def main():
    #main parser
    parser = CustomParser(
        prog="adt",
        formatter_class=argparse.RawTextHelpFormatter,
        description = textwrap.dedent('''
    A generalised ADT program for analytical and numerical calculation. This is applicable for any
    'N' electronic state sub-Hilbert space. The analytical segment can be used to generate symbolic
    expressions of eigth adiabatic to diabatic transformation (ADT) quantities (elements of adiabatic
    potential energy matrix, elements of nonadiabatic coupling matrix, ADT matrix elements, partially
    substituted ADT equations, completely substituted ADT equations, elements of coefficient matrix of
    gradient of ADT angles, elements  of coefficient matrix of nonadiabatic coupling terms (NACTs) and
    the diabatic potential energy matrix elements) for any arbitrary number of coupled electronic
    states. On the other hand, the numerical portion computes ADT angles, ADT matrix elements, diabatic
    potential energy matrix elements and residue of ADT angles for any 'N' coupled electronic states
    with multiple degrees of freedom. Any user can solve the differential equations along eight
    different paths over the nuclear configuration space (CS).''')
        )

    #adding subparsers
    subparsers = parser.add_subparsers(title='Available sub-commands', dest="choice", help="choose from one of these")


    #subparser for analytical jobs
    analytical = subparsers.add_parser("ana",
        formatter_class=argparse.RawTextHelpFormatter,
        description = textwrap.dedent('''
    Devise analytical expressions of any one of the ADT quantities for a given number of states'''),
        help ="Formulate analytical expressions")
    analytical_required = analytical.add_argument_group("Required arguments")



    #subparser for numerical jobs
    numeric = subparsers.add_parser("num",
        formatter_class=argparse.RawTextHelpFormatter,
        description = textwrap.dedent('''
    Calculate ADT angle and diabatic potential energy matrix for a given number of electronic states along a specific path.
    '''),
        help= "Calculate ADT angle and diabatic potential energy matrix")
    numeric_required = numeric.add_argument_group("Required arguments")


    molpro = subparsers.add_parser('mol',
        formatter_class=argparse.RawTextHelpFormatter,
        description = textwrap.dedent('''
    Calculate the Adiabatic potential energy surfaces(PESs) and noadiabatic coupling matrix(NACM)
    and subsequently calculate the Numerical quantities using the numerical section.'''),
        help= "Run MOLPRO and calculate ADT angles and diabatic surfaces and couplings")
    molpro_required = molpro.add_argument_group("Required arguments")


    #adding options for analytical jobs
    analytical_required.add_argument("-nstate",
                                    type=int,
                                    help="Number of states", required=True)
    analytical         .add_argument("-anajob",
                                    type=int,
                                    help="Specify the type of expression (default: %(default)s - completely substituted ADT equation) ",
                                    choices=range(1,9),
                                    metavar="[1-6]",
                                    default=3)



    #adding options for numerical jobs
    numeric_required.add_argument("-nfile",
                        type     = str,
                        help     = "Need to specify the path of the input \nNACT file, which is required both for \n1D as well as 2D calculation. This file \nrepresents the component of NACT for \nthe circular coordinate (e.g. {0,2pi}).\n ",
                        metavar  = "FILE",
                        required = True)
    numeric.add_argument("-mfile",
                        type     = str,
                        help     = "Specify the path of the input NACT file. \nrepresenting the component of NACT \nfor the non-circular coordinate \n(e.g. {0,pi/2} or {0,pi} or \n{0,infinity}).\n ",
                        metavar  = "FILE")
    numeric.add_argument("-intpath",
                        type    = int,
                        help    = "Specify the path for calculation (default: %(default)s).\n ",
                        choices = range(1,9),
                        metavar = "[1-8]",
                        default = 1)
    numeric.add_argument("-efile",
                        type    = str,
                        help    = "Specify the path of the adiabatic PES file for \ncalculating the diabatic potential energy matrix \nelements.\n ",
                        metavar = "FILE")
    numeric.add_argument('-nstate',
                        type = int,
                        help = "Specify the number of states to do the calculation.\nBy default it includes all the data for calculation.\n  ")
    numeric.add_argument('-order',
                        type = str,
                        help = "Write the order of multiplication of elementary rotation matrices.\n  ")
    numeric.add_argument("-ofile",
                        type    = str,
                        help    = "Specify the output folder/file name (w/o extension) \n(default: %(default)s).\n ",
                        metavar = "FILE",
                        default="'ADT_numeric'")
    numeric.add_argument("-n",
                        type    =str,
                        help="Specify number of OpenMP threads for parallel jobs. \n(default: 1)\n ",
                        default= False)
    numeric.add_argument("-h5",
                        action = 'store_true',
                        help   = "Write results in a HDF5 file (.h5). \nFast IO, smaller file size and hierarchical filesystem-like data format,\npreferable for saving and sharing large datasets in an organised way.\n " )
    numeric.add_argument("-nb",
                        action = 'store_true',
                        help   = 'Write results in Numpy binary file (.npy). \nPreferable when working with numpy for its much faster IO and easy portability.\n ')
    numeric.add_argument("-txt" ,
                        action = "store_true",
                         help="Write results in a text file.(default behaviour).")
    numeric.set_defaults(h5=False,txt=False, nb = False)



    molpro_required.add_argument('-config',
                        type    = str,
                        metavar = "FILE",
                        required = True,
                        help='Specify the molpro configuration file containing\nthe necessary keywords of MOLPRO software.\n  ')
    molpro_required.add_argument('-atomfile',
                        type    = str,
                        metavar = "FILE",
                        required = True,
                        help='Specify the information file constituting atomic\nsymbols and atomic masses. \n ')
    molpro.add_argument('-geomfile',
                        type    = str,
                        metavar = "FILE",
                        default='geomfile.dat',
                        help='Specify the geometry file containing the initial\ngrid point in "xyz" format (in Angstrom)\n(default: %(default)s). \n(Ignore for scattering system). \n ')
    molpro.add_argument('-freqfile',
                        type    = str,
                        metavar = "FILE",
                        default = 'frequency.dat',
                        help='Specify the frequency information file, where\nfrequencies of normal modes are written in cm-1\n(default: %(default)s). \n(Ignore for scattering system). \n ')
    molpro.add_argument('-wilsonfile',
                        type    = str,
                        metavar = "FILE",
                        default = 'wilson.dat',
                        help='Specify the filename containing the Wilson matrix\nof a molecular species (default: wilson.dat).\n(default: %(default)s).\n(Ignore for scattering system). \n ')
    molpro.add_argument("-intpath",
                        type    = int,
                        help    = "Specify the path for calculation (default: %(default)s).\n ",
                        choices = range(1,9),
                        metavar = "[1-8]",
                        default = 1)
    molpro.add_argument('-order',
                        type = str,
                        help = "Write the order of multiplication of elementary rotation matrices.\n  ")
    molpro.add_argument("-ofile",
                        type    = str,
                        help    = "Specify the output file name (w/o extension) \n(default: %(default)s).\n ",
                        metavar = "FILE",
                        default="'ADT_numeric'")
    molpro.add_argument("-n",
                         type=str,
                         help="Specify number of OpenMP threads to use for parallel calculation. \n(default: 1)\n ",
                         default=False)
    molpro.add_argument("-mo" ,
                        action = "store_true",
                        help="Terminate the execution only after completion of MOLPRO jobs.\n ")
    molpro.add_argument("-h5",
                        action = 'store_true',
                        help   = "Write results in a HDF5 file (.h5).\nFast IO, smaller file size and hierarchical filesystem-like data format,\npreferable for saving and sharing large datasets in an organised way.\n " )
    molpro.add_argument("-nb",
                        action = 'store_true',
                        help   = 'Write results in Numpy binary file (.npy). \nPreferable when working with numpy for its much faster IO and easy portability.\n ')
    molpro.add_argument("-txt" ,
                        action = "store_true",
                        help="Write results in a text file. (default behaviour).")
    molpro.set_defaults(h5=False,txt=False, nb = False, mo = False)


    args = parser.parse_args()
    print (args)
main()
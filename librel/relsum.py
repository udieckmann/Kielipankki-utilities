#! /usr/bin/env python3
# -*- mode: Python; -*-

# Implementation of a command-line tool ../rel-sum,
# hopefully also usable with synthetic arguments in
# a Mylly (Chipster) tool, to be tested.

from subprocess import Popen
import sys
 
from .args import transput_args
from .args import BadData
from .names import makenames
from .data import readhead, groups

def parsearguments(argv, *, prog = None):
    description = '''

    Sum of two or more relations of the same type, records tagged with
    origin 1, 2, ... in a new field. The order of the fields is what
    it happened to be in the first relation, followed by the tag.

    '''

    parser = transput_args(description = description, summing = True)

    parser.add_argument('--tag', '-t', metavar = 'name', required = True,
                        help = '''

                        tag field name

                        ''')

    args = parser.parse_args(argv)
    args.prog = prog or parser.prog

    return args

def main(args, ins, ous):

    # transput arranges so that all input records are in ins, with
    # tags of origin, so ins already is the sum; Boolean tools work
    # more (rel-union, rel-meet, rel-sans, rel-symm).

    Popen([ 'cat' ],
          stdin = ins,
          stdout = ous,
          stderr = None)

    return 0

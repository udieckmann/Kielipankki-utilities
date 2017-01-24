#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Scramble (randomly shuffle) structures in a VRT input."""


import sys
import re
import random

import korpimport.util


class VrtScrambler(korpimport.util.InputProcessor):

    def __init__(self):
        super(VrtScrambler, self).__init__()
        self._scramble_units = []
        self._rnd = random.Random(self._opts.random_seed)

    def process_input_stream(self, stream, filename=None):
        within_begin_re = re.compile(
            ur'<' + self._opts.scramble_within + '[>\s]')
        scramble_begin_re = re.compile(
            ur'<' + self._opts.scramble_unit + '[>\s]')
        scramble_end = '</' + self._opts.scramble_within + '>'
        collecting = False
        units = []
        current_unit = []
        for line in stream:
            if collecting:
                if line.startswith(scramble_end):
                    if current_unit:
                        units.append(current_unit)
                    collecting = False
                    for line2 in self._scramble(units):
                        sys.stdout.write(line2)
                    sys.stdout.write(line)
                elif scramble_begin_re.match(line):
                    if current_unit:
                        units.append(current_unit)
                    current_unit = [line]
                else:
                    current_unit.append(line)
            else:
                sys.stdout.write(line)
                if within_begin_re.match(line):
                    units = []
                    current_unit = []
                    collecting = True

    def _scramble(self, units):
        self._rnd.shuffle(units)
        for unit in units:
            for line in unit:
                yield line

    def getopts(self, args=None):
        self.getopts_basic(
            dict(usage="%progname [options] [input] > output",
                 description=(
"""Scramble (randomly shuffle) given structures (elements), such as sentences,
within larger structures, such as texts, in the VRT input and output the
scrambled VRT.

Note that the input may not have intermediate structures between the
containing structures and the structures to be scrambled; for example, if
sentences are scrambled within texts, the input may not have paragraphs.
""")
             ),
            args,
            ['scramble-unit|unit =STRUCT', dict(
                default='sentence',
                help=('shuffle STRUCT structures (elements)'
                      ' (default: %default)'))],
            ['scramble-within|within =STRUCT', dict(
                default='text',
                help=('shuffle structures within STRUCT structures (elements):'
                      ' structures are not moved across STRUCT boundaries'
                      ' (default: %default)'))],
            ['random-seed|seed =SEED', dict(
                type='int',
                default=2017,
                help=('set random number generator seed to SEED (an integer);'
                      ' use 0 for a random seed (non-repeatable output)'
                      ' (default: %default)'))],
        )
        if self._opts.random_seed == 0:
            self._opts.random_seed = None


if __name__ == "__main__":
    VrtScrambler().run()

#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import codecs
import re

from optparse import OptionParser
# collections.OrderedDict requires Python 2.7
from collections import defaultdict, OrderedDict


class TimespanExtractor(object):

    DEFAULT_PATTERN = r'((?:1[0-9]|20)[0-9][0-9])'
    DEFAULT_PATTERN_2 = r'((?:1[0-9]|20)?[0-9][0-9])'

    def __init__(self, opts):
        self._opts = opts
        self._make_extract_patterns()
        self._make_excludes()
        self._time_tokencnt = defaultdict(int)

    def _make_extract_patterns(self):
        self._extract_patterns = defaultdict(list)
        default_pattern = (self.DEFAULT_PATTERN_2 if self._opts.two_digit_years
                           else self.DEFAULT_PATTERN)
        if (self._opts.extract_pattern == [] and not self._opts.unknown
            and not self._opts.fixed):
            self._opts.extract_pattern.append('* * ' + default_pattern)
        for source in self._opts.extract_pattern:
            parts = source.split(None, 3)
            elemnames = parts[0].split('|')
            attrnames = parts[1].split('|') if len(parts) > 1 else ['*']
            pattern = parts[2] if len(parts) > 2 else default_pattern
            templ = parts[3] if len(parts) > 3 else r'\1'
            for elemname in elemnames:
                for attrname in attrnames:
                    self._extract_patterns[elemname].append(
                        (attrname, pattern, templ))

    def _make_excludes(self):
        self._excludes = defaultdict(list)
        for exclude in self._opts.exclude:
            parts = exclude.split(None, 2)
            elemnames = parts[0].split('|')
            attrnames = parts[1].split('|') if len(parts) > 1 else ['*']
            for elemname in elemnames:
                self._excludes[elemname].extend(attrnames)

    def process_files(self, files):
        if isinstance(files, list):
            for file_ in files:
                self.process_files(file_)
        elif isinstance(files, basestring):
            with codecs.open(files, 'r', encoding='utf-8') as f:
                self._extract_timespans(f)
        else:
            self._extract_timespans(files)

    def _extract_timespans(self, f):
        time = '' if not self._opts.fixed else self._opts.fixed
        structdepth = 0
        timestruct = 0
        for line in f:
            if ((self._opts.unknown or self._opts.fixed)
                and not line.startswith('<')):
                self._time_tokencnt[time] += 1
            elif line.startswith('</'):
                structdepth -= 1
                if time and structdepth < timestruct:
                    time = ''
                    timestruct = 0
            elif line.startswith('<'):
                structdepth += 1
                if not time:
                    time = self._extract_time(line)
                    if time:
                        timestruct = structdepth
            else:
                self._time_tokencnt[time] += 1

    def _extract_time(self, line):
        if '*' in self._excludes.get('*', []):
            return ''
        mo = re.match(r'<(.*?)( .*)?>', line)
        if not mo or not mo.group(2):
            return ''
        elemname = mo.group(1)
        if '*' in self._excludes.get(elemname, []):
            return ''
        attrlist = mo.group(2)
        attrs = OrderedDict(re.findall(r' (.*?)="(.*?)"', attrlist))
        real_elemname = elemname
        if not elemname in self._extract_patterns:
            elemname = '*'
        for (patt_attr, pattern, templ) in self._extract_patterns[elemname]:
            if patt_attr in attrs:
                check_attrs = [patt_attr]
            elif patt_attr == '*':
                check_attrs = attrs.iterkeys()
            else:
                continue
            for attrname in check_attrs:
                if (attrname in self._excludes.get(real_elemname, [])
                    or attrname in self._excludes.get('*', [])):
                    continue
                mo = re.search(pattern, attrs[attrname])
                if mo:
                    return mo.expand(templ)
        return ''  

    def output_timespans(self):
        for (time, tokencnt) in sorted(self._time_tokencnt.iteritems()):
            if self._opts.two_digit_years and len(time) == 2:
                # FIXME: These should be based either on the current
                # century or on an explicitly specified one.
                if int(time) > self._opts.century_pivot:
                    time = '19' + time
                else:
                    time = '20' + time
            sys.stdout.write('\t'.join([time, str(tokencnt)]) + '\n')


def getopts():
    optparser = OptionParser()
    optparser.add_option('--unknown', action='store_true', default=False)
    optparser.add_option('--fixed', default=None)
    optparser.add_option('--extract-pattern', '--pattern', action='append',
                         default=[])
    optparser.add_option('--two-digit-years', action='store_true',
                         default=False)
    optparser.add_option('--exclude', action='append', default=[])
    # FIXME: The default could be based on the current year
    optparser.add_option('--century-pivot', default='20')
    (opts, args) = optparser.parse_args()
    return (opts, args)


def main():
    input_encoding = 'utf-8'
    output_encoding = 'utf-8'
    sys.stdin = codecs.getreader(input_encoding)(sys.stdin)
    sys.stdout = codecs.getwriter(output_encoding)(sys.stdout)
    (opts, args) = getopts()
    extractor = TimespanExtractor(opts)
    extractor.process_files(args if args else sys.stdin)
    extractor.output_timespans()


if __name__ == "__main__":
    main()

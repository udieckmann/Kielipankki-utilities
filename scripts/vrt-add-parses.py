#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import sqlite3
import os
import os.path
import errno
import re

import cStringIO as strio

from optparse import OptionParser


class ParseAdder(object):

    def __init__(self, opts):
        self._opts = opts
        self._sentnr = 0

    def process_files(self, files):
        if isinstance(files, list):
            for file_ in files:
                self.process_files(file_)
        elif isinstance(files, basestring):
            with codecs.open(files, 'r', encoding='utf-8') as f:
                self._add_parses(f)
        else:
            self._add_parses(files)

    def _add_parses(self, infile):
        file_sentnr = 0
        sent_line = None
        tokens = []
        parses = self._get_sentence_parses(infile.name)
        self._infile_name = infile.name
        with codecs.open(self._make_outfilename(infile.name), 'w',
                         encoding='utf-8') as outfile:
            for line in infile:
                if line.startswith('<'):
                    if line.startswith('<sentence '):
                        sent_line = line
                    elif line.startswith('</sentence>'):
                        self._add_sentence_parse(tokens, parses[file_sentnr][0],
                                                 file_sentnr)
                        self._write_sentence(outfile, sent_line, tokens,
                                             parses[file_sentnr][1])
                        tokens = []
                        file_sentnr += 1
                        self._sentnr += 1
                    elif not tokens:
                        outfile.write(line)
                        if not line.endswith('\n'):
                            outfile.write('\n')
                else:
                    tokens.append(line[:-1].split('\t'))

    def _get_sentence_parses(self, vrt_fname):
        parses = []
        with sqlite3.connect(self._opts.database) as con:
           cur = con.cursor()
           sens = cur.execute(
               '''select tok, stt from doc, sen
                  where doc.nme = :nme and sen.yno = doc.yno
                        and sen.dno = doc.dno
                  order by sno''',
               {'nme': self._make_filename_key(vrt_fname)})
           for sen, stt in sens:
               parses.append((self._split_sentence(sen), stt))
        # print repr(parses)
        return parses

    def _make_filename_key(self, vrt_fname):
        dirname, fname = os.path.split(vrt_fname)
        _, lastdir = os.path.split(dirname)
        return os.path.join(lastdir, fname)

    def _split_sentence(self, sen):
        return [re.split(r'\t+', token) for token in sen[:-1].split('\n')]

    def _make_outfilename(self, infilename):
        outfilename = self._make_filename_key(infilename)
        dirname = os.path.dirname(outfilename)
        # http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary
        try:

            os.makedirs(os.path.join(self._opts.output_dir, dirname))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        return os.path.join(self._opts.output_dir, outfilename)

    def _add_sentence_parse(self, tokens, parsed_tokens, file_sentnr):
        for tokennr, token_fields in enumerate(tokens):
            parsed_token = self._add_parse(
                token_fields, parsed_tokens[tokennr], file_sentnr)
            if (self._opts.lemma_without_compound_boundary
                and len(parsed_token) > 1):
                parsed_token[1:1] = [parsed_token[1].replace('|', '')]
            tokens[tokennr] = parsed_token

    def _add_parse(self, token_fields, parsed_token_fields, file_sentnr):
        if token_fields[0] != parsed_token_fields[1]:
            if token_fields[0] == '' and len(token_fields) == 1:
                return []
            sys.stderr.write(
                u'Warning: parse does not match original: "{0}" != "{1}", '
                u'file {2}, sentence {3:d}\n'.format(
                    token_fields[0], parsed_token_fields[1],
                    self._infile_name, file_sentnr))
            # print >>sys.stderr, repr(token_fields)
            # print >>sys.stderr, repr(parsed_token_fields)
        return [parsed_token_fields[fieldnum]
                for fieldnum in [1, 3, 5, 7, 9, 11, 0]] + token_fields[1:]

    def _write_sentence(self, outfile, sent_line, tokens, parse_state):
        outfile.write(''.join([sent_line[:-2].replace(' id=', ' local_id='),
                               ' id="', str(self._sentnr),
                               '" parse_state="', parse_state, '">\n']))
        for token_fields in tokens:
            outfile.write('\t'.join(token_fields) + '\n')
        outfile.write('</sentence>\n')


def getopts():
    optparser = OptionParser()
    optparser.add_option('--database')
    optparser.add_option('--output-dir', default='.')
    optparser.add_option('--no-lemma-without-compound-boundary',
                         action='store_false', default=True,
                         dest='lemma_without_compound_boundary')
    (opts, args) = optparser.parse_args()
    return (opts, args)


def main():
    input_encoding = 'utf-8'
    output_encoding = 'utf-8'
    sys.stdin = codecs.getreader(input_encoding)(sys.stdin)
    sys.stdout = codecs.getwriter(output_encoding)(sys.stdout)
    (opts, args) = getopts()
    parse_adder = ParseAdder(opts)
    parse_adder.process_files(args)


if __name__ == "__main__":
    main()

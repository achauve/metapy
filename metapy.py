#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path as osp
import sys
import traceback
from functools import partial
import hashlib


SEP='//#'
SEP_BEGIN='/*#'
SEP_END='#*/'


HASH_BODY = """ This file was autogenerated. Hash of autogenerated content:
%s
"""
HEADER = SEP_BEGIN + HASH_BODY + SEP_END + '\n'

class ListOut(object):
    def __init__(self, l):
        self._l = l
    def write(self, txt):
        self._l.append(txt)


def run_code(code, global_context, output):
    sys.stdout = ListOut(output)
    try:
        exec(code, global_context)
    except:
        sys.stdout = sys.__stdout__
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    sys.stdout = sys.__stdout__


def include_h(filename, global_context):
    remove_ext = lambda f : osp.splitext(f)[0]
    basename = remove_ext(remove_ext(filename))
    for ext in ('.h', '.hxx', '.hpp', '.txx'):
        new_filename = basename + ext + '.meta'
        if osp.exists(new_filename):
            parse_file(new_filename, global_context)


def parse_file(filename, global_context=None):
    f = open(filename)
    output = []
    current_code_block = None

    if global_context is None:
        global_context = {}
        global_context['include_h'] = partial(include_h, filename, global_context)

    global_context['__file__'] = filename
    run = partial(run_code, global_context=global_context, output=output)

    for line in f:
        line = line.rstrip()
        if current_code_block is not None:
            if line.endswith(SEP_END):
                run('\n'.join(current_code_block))
                current_code_block = None
            else:
                current_code_block.append(line)
        else:
            if line.startswith(SEP_BEGIN):
                current_code_block = []
            elif line.startswith(SEP):
                run(line.split(SEP)[1])
            else:
                output.append(line + '\n')

    return output


def usage():
    print """usage: python %s file1.x.meta [file2.x.meta ... fileN.x]

Generates files file1.x, file2.x, ..., fileN.x.
""" % sys.argv[0]
    exit(1)


def compute_sha(data):
    sha = hashlib.sha1()
    sha.update(data)
    return sha.hexdigest()


def check_generated_file_was_not_manually_edited(out_filename):
    out_file = open(out_filename)
    lines = out_file.readlines()
    parsed_sha = lines[1].strip()
    out_file_content = ''.join(lines[3:])
    computed_sha = compute_sha(out_file_content)

    if computed_sha != parsed_sha:
        print '>'*100
        print 'ERROR file %s was edited manually. Plese delete your modifications' \
                ' or delete the file!' % out_filename
        print '>'*100
        exit(1)

    return parsed_sha


def main():
    if len(sys.argv) < 2:
        usage()

    for filename in sys.argv[1:]:
        out_filename = osp.splitext(filename)[0]

        old_sha = None
        if osp.exists(out_filename):
            old_sha = check_generated_file_was_not_manually_edited(out_filename)

        new_content = ''.join(parse_file(filename))
        new_sha = compute_sha(new_content)

        if osp.exists(out_filename) and new_sha == old_sha:
            # do not overwrite the generated file if the content has not changed
            continue
        else:
            out_file = open(out_filename, 'w')
            out_file.write(HEADER % new_sha)
            out_file.write(new_content)


if __name__ == '__main__':
    main()

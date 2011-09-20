# -*- coding: utf-8 -*-

import unittest
import os.path as osp
from metapy import parse_file

TEST_DIR = 'tests'

TEST_FILES = (
    'test_make_vector.cpp',
    'test_includeh.h',
    'test_includeh.cpp',
    )

class TestMetaPy(unittest.TestCase):

    def test(self):
        for test_file in TEST_FILES:
            test_file = osp.join(TEST_DIR, test_file)
            metapy_output = parse_file(test_file + '.meta')
            ref_output = open(test_file + '.ref').read()
            self.assertEquals(''.join(metapy_output), ref_output)

if __name__ == '__main__':
    unittest.main()

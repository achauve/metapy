# -*- coding: utf-8 -*-

import unittest
from metapy import parse_file

class TestMetaPy(unittest.TestCase):

    def test_parse_file(self):
        test_files = ('test_make_vector.cpp',
                )

        for test_file in test_files:
            metapy_output = parse_file(test_file + '.meta')
            ref_output = open(test_file + '.ref').read()
            self.assertEquals(''.join(metapy_output), ref_output)

if __name__ == '__main__':
    unittest.main()

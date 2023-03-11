#!/usr/bin/env python3
import check_routes as cr
import unittest

class TestRoutes(unittest.TestCase):

    def test_error01(self):
        '''Overlapping and invalid subnets'''
        error_list = cr.check_file("tests/routes_err01.txt")
        self.assertEqual(len(error_list), 2)
        self.assertEqual(error_list[0].type, cr.ErrorType.INVALID)
        self.assertEqual(error_list[0].subnets, {"10.0.10.0/16"})
        self.assertEqual(error_list[1].type, cr.ErrorType.OVERLAP)
        self.assertEqual(error_list[1].subnets, {"10.10.0.0/16", "10.10.0.0/24"})

    def test_error02(self):
        '''Empty routes file'''
        error_list = cr.check_file("tests/routes_err02.txt")
        self.assertEqual(len(error_list), 0)

    def test_error03(self):
        '''Routes file with 1 line'''
        error_list = cr.check_file("tests/routes_err03.txt")
        self.assertEqual(len(error_list), 0)

    def test_error04(self):
        '''Subnets not in CIDR format'''
        error_list = cr.check_file("tests/routes_err04.txt")
        self.assertEqual(len(error_list), 2)

    def test_error05(self):
        '''Routes file with line in unknown format'''
        error_list = cr.check_file("tests/routes_err05.txt")
        self.assertEqual(len(error_list), 1)
        self.assertEqual(error_list[0].type, cr.ErrorType.FORMAT)
        self.assertEqual(error_list[0].subnets, "")

    def test_error06(self):
        '''Routes file with empty lines'''
        error_list = cr.check_file("tests/routes_err06.txt")
        self.assertEqual(len(error_list), 1)

if __name__ == '__main__':
    unittest.main()


#!/usr/bin/env python3
import check_routes as cr
import unittest

class TestRoutes(unittest.TestCase):

    def test_error01(self):
        error_list = cr.check_file("tests/routes_err01.txt")
        self.assertEqual(len(error_list), 2)
        self.assertEqual(error_list[0].type, cr.ErrorType.INVALID)
        self.assertEqual(error_list[0].subnets, {"10.0.10.0/16"})
        self.assertEqual(error_list[1].type, cr.ErrorType.OVERLAP)
        self.assertEqual(error_list[1].subnets, {"10.10.0.0/16", "10.10.0.0/24"})

if __name__ == '__main__':
    unittest.main()


#!/usr/bin/env python3
""" Check file for overlapping network subnets

Requirements
    Python >= 3.6
    Packages: ipaddress

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
import logging
import os
import re
import sys

from enum import Enum
from ipaddress import IPv4Network
from typing import Optional

__license__ = "GPLv3"
__version__ = "0.1"


# Global defaults that can be changed by command line parameters
DEBUG = False


# Global logging object
logger = logging.getLogger(__name__)


# Errors types
class ErrorType(Enum):
    INVALID = 1   # Invalid subnet
    OVERLAP = 2   # Overlapping subnets
    FORMAT = 3    # Invalid format

    @classmethod
    def has_value(this, value):
        return value in [member.value for member in Mode]


class Error:
    def __init__(self, error_subnets: set={}, error_type: ErrorType=None,
                 error_msg: str=""):
        self.subnets = error_subnets
        self.type = error_type
        self.msg = error_msg


def parseargs() -> argparse.Namespace:
    """ Parse command-line arguments """
    parser = argparse.ArgumentParser(description='Check overlapping subnets')
    parser.add_argument(
        '-q', '--quiet', required=False,
        help='quiet mode, do not print anything to stdout', dest='quiet',
        action='store_true')
    parser.add_argument(
        '-d', '--debug', required=False,
        help='enable debug output', dest='debug',
        action='store_true')
    parser.add_argument(
        '-f', '--file', required=True,
        help='file containing list of subnets', dest='subnet_file',
        action='store')

    args = parser.parse_args()
    return args


class LogFilterWarning(logging.Filter):
    """Logging filter >= WARNING"""
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO, logging.WARNING)


def get_logger(debug: bool = False) -> logging.Logger:
    """Retrieve logging object"""
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Log everything >= DEBUG to stdout
    h1 = logging.StreamHandler(sys.stdout)
    h1.setLevel(logging.DEBUG)
    h1.setFormatter(logging.Formatter(fmt='%(asctime)s [%(process)d] %(levelname)s: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S'))
    h1.addFilter(LogFilterWarning())

    # Log errors to stderr
    h2 = logging.StreamHandler(sys.stderr)
    h2.setFormatter(logging.Formatter(fmt='%(asctime)s [%(process)d] %(levelname)s: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S'))
    h2.setLevel(logging.ERROR)

    logger.addHandler(h1)
    logger.addHandler(h2)

    return logger


def check_file(subnet_file :str) -> list:
    """Check file that contains list of subnets"""
    error_list = []
    networks = {}

    with open(subnet_file, "r") as file:
        linenr = 1
        for line in file.readlines():
            m = re.match(r"^push route (.*)$", line)
            if m:
                try:
                    # Checking for invalid subnet definition
                    subnet = IPv4Network(m.group(1))
                except ValueError as e:
                    error_list.append(Error({m.group(1)}, ErrorType.INVALID, f"Invalid subnet {m.group(1)} on line number {linenr}"))
                else:
                    networks[subnet] = linenr
            else:
                # Ignore comment line
                m = re.match(r"^\s*#", line)
                if not m:
                    # Invalid line
                    error_list.append(Error("", ErrorType.FORMAT, f"Invalid line {line} on line number {linenr}"))

            linenr += 1

    networks_list = sorted(networks.keys())

    prev_network = networks_list.pop(0)
    for current_network in networks_list:
        logger.debug(f"Comparing {prev_network} <-> {current_network}")
        if prev_network.overlaps(current_network):
            error_list.append(Error({str(prev_network), str(current_network)}, ErrorType.OVERLAP, f"Network {prev_network} overlaps {current_network}"))
        else:
            logger.debug(f"OK: {current_network}")
        prev_network = current_network
    logger.debug(f"OK: {prev_network}")

    return error_list

def main():
    """Main program flow"""
    global DEBUG
    ret = 0 # Return code of script

    # Set up environment
    args = parseargs()
    mylogger = get_logger(args.debug)

    if args.debug:
        DEBUG = True

    error_list = check_file(args.subnet_file)
    for error in error_list:
        mylogger.error(f"{error.msg}")
        ret = 1


    exit(ret)


if __name__ == '__main__':
    main()

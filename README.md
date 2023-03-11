![last commit](https://img.shields.io/github/last-commit/groland11/check-routes.svg)
![languages](https://img.shields.io/github/languages/top/groland11/check-routes.svg)
![license](https://img.shields.io/github/license/groland11/check-routes.svg)

# check-routes
Check overlapping subnets
- Reads subnets from file (file format can be easily adapted)
- Check if subnet conforms to CIDR format
- Check if subnets overlap
- Useful if subnet file is part of an OpenVPN configuration (push routes to client)

## Prerequisites
- Python >= 3.6
- Python package ipaddress

## Usage
```
> ./check-routes.py -h
usage: check-routes.py [-h] [-q] [-d] -f SUBNET_FILE

Check overlapping subnets

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           quiet mode, do not print anything to stdout
  -d, --debug           enable debug output
  -f SUBNET_FILE, --file SUBNET_FILE
                        file containing list of subnets

```

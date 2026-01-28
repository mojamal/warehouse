#!/usr/bin/env python3
"""
This script determines how to handle a package dispatch based on dimensions and mass.

A package can be:
- STANDARD  -> normal
- SPECIAL   -> heavy OR bulky
- REJECTED  -> heavy AND bulky

Usage:
    python sort.py <width> <height> <length> <mass>
"""

import sys

# Constants
UPPER_DIMENSION = 150
UPPER_MASS = 20
UPPER_VOLUME = 1_000_000


def sort(width: int, height: int, length: int, mass: int) -> str:
    package_is_bulky = False
    package_is_heavy = False

    # Check dimensions
    for dimension in (width, height, length):
        if dimension > UPPER_DIMENSION:
            package_is_bulky = True

    # Check volume
    volume = width * height * length
    if volume > UPPER_VOLUME:
        package_is_bulky = True

    # Check mass
    if mass > UPPER_MASS:
        package_is_heavy = True

    # Determine shipping method
    if package_is_bulky and package_is_heavy:
        return "REJECTED"
    elif package_is_bulky or package_is_heavy:
        return "SPECIAL"
    else:
        return "STANDARD"


def main():
    if len(sys.argv) != 5:
        print("Usage: python sort.py <width> <height> <length> <mass>")
        sys.exit(1)

    try:
        width, height, length, mass = map(int, sys.argv[1:])
    except ValueError:
        print("All arguments must be integers.")
        sys.exit(1)

    result = sort(width, height, length, mass)
    print(result)


if __name__ == "__main__":
    main()

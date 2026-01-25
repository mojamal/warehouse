#! /usr/bin/env bash

# This script determines how to handle a package dispatch based the dimensions and mass provided as input
# A package can be handled normally (automatically), manually or rejected based on the package weight and dimensions
# Implement the funciton sort(width,height,lenght,mass) and it should return
# STANDARD - normal
# SPECIAL - heavy OR bulky
# REJECTED - heavy AND bulky
#
# Usage: sort(width,height,length,mass)

if [ "$#" -ne 4 ]; then
    echo "Usage: ./sort.sh.sh <width> <heigth> <length> <mass>"
    exit 1
fi

# Constants
UPPER_DIMENSION=150
UPPER_MASS=20
UPPER_VOLUME=1000000

# Function: sort(width, height, length, mass)
sort() {
  local width=$1
  local height=$2
  local length=$3
  local mass=$4

  local PACKAGE_IS_BULKY=0
  local PACKAGE_IS_HEAVY=0

  # Check Dimensions
  for dimension in "$width" "$height" "$length"; do
    if [ "$dimension" -gt "$UPPER_DIMENSION" ]; then
      PACKAGE_IS_BULKY=1
    fi
  done

  # Check Volume
  local VOLUME=$((width * height * length))
  if [ "$VOLUME" -gt "$UPPER_VOLUME" ]; then
    PACKAGE_IS_BULKY=1
  fi

  # Check Mass
  if [ "$mass" -gt "$UPPER_MASS" ]; then
    PACKAGE_IS_HEAVY=1
  fi

  # Determine Shipping Method
  if [ "$PACKAGE_IS_BULKY" -eq 1 ] && [ "$PACKAGE_IS_HEAVY" -eq 1 ]; then
    echo "REJECTED"
  elif [ "$PACKAGE_IS_BULKY" -eq 1 ] || [ "$PACKAGE_IS_HEAVY" -eq 1 ]; then
    echo "SPECIAL"
  else
    echo "STANDARD"
  fi
}

sort "$1" "$2" "$3" "$4"

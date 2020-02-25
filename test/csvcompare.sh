#!/bin/sh

./2float.py < $1 > f1.tmp
./2float.py < $2 > f2.tmp

diff f1.tmp f2.tmp

rm f1.tmp f2.tmp

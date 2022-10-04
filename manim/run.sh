#! /bin/zsh
clear
if [[ ("$#" -lt 2) || ("$#" -gt 2) ]]; then
    manim -pql intro.py DifferentRotations
else 
    manim -pql $1 $2
fi

# python wrapper for package gopy-prac within overall package slices
# This is what you import to use the package.
# File is generated by gopy. Do not edit.
# gopy build -output=out -vm=python3 .

# the following is required to enable dlopen to open the _go.so file
import os,sys,inspect,collections
try:
	import collections.abc as _collections_abc
except ImportError:
	_collections_abc = collections

cwd = os.getcwd()
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.chdir(currentdir)
from . import _slices
from . import go

os.chdir(cwd)

# to use this code in your end-user python file, import it as follows:
# from slices import slices
# and then refer to everything using slices. prefix
# packages imported by this package listed below:




# ---- Types ---


#---- Enums from Go (collections of consts with same type) ---


#---- Constants from Go: Python can only ask that you please don't change these! ---


# ---- Global Variables: can only use functions to access ---


# ---- Interfaces ---


# ---- Structs ---


# ---- Slices ---


# ---- Maps ---


# ---- Constructors ---


# ---- Functions ---
def FibParallel(max, numWorkers, numTimes, verbose, goRun=False):
	"""FibParallel(int max, int numWorkers, int numTimes, bool verbose) """
	_slices.slices_FibParallel(max, numWorkers, numTimes, verbose, goRun)
def IntSum(s):
	"""IntSum([]int s) int"""
	return _slices.slices_IntSum(s.handle)
def CreateSlice():
	"""CreateSlice() []int"""
	return go.Slice_int(handle=_slices.slices_CreateSlice())
def Fib(max, verbose):
	"""Fib(int max, bool verbose) []int"""
	return go.Slice_int(handle=_slices.slices_Fib(max, verbose))


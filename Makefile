########################################################################
#
# Makefile for resnet152
#
########################################################################

# List the files to be included in the .mlm package.

MODEL_FILES = 			\
	configure.sh		\
	demo.py 		\
	print.py		\
	display.py		\
	score.py                \
	README.txt		\
	DESCRIPTION.yaml	\
	objreg_utils.py         \

include ../git.mk
include ../pandoc.mk
include ../clean.mk
include ../mlhub.mk

clean::
	rm -rf README.txt output

realclean:: clean
	rm -rf $(MODEL)_*.mlm


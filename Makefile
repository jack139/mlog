PY = python3 -O -m compileall -b -q -f
SRC = src
TARGETS = mlog

all: clean

clean:
	@echo "Clean ..." 
	@find . -name "__pycache__" | xargs rm -rf
	@rm -f logs/rt/* data/rt/*

PY = python3.6 -O -m compileall -b -q -f
SRC = src
TARGETS = mlog
TEMP = logs/rt/* data/rt/*
all: clean $(TARGETS)

$(TARGETS):
	@echo "Compiling ..."
	@cp -r $(SRC) $(TARGETS)
	-$(PY) $(TARGETS)
	@find $(TARGETS) -name '*.py' -delete
	@find $(TARGETS) -name "__pycache__" |xargs rm -rf

clean:
	@echo "Clean ..." 
	@find . -name "__pycache__" | xargs rm -rf
	@rm -rf $(TARGETS) $(TEMP)

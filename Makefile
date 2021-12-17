PYTHON = python3

NAME_FILE = certscan.py

INSTALL_DIR ?= /usr/local/bin

PATH_LOCAL = /opt/scripts

.DEFAULT_GOAL = help

help:
	@echo "----------------HELP------------------"
	@echo "To setup certscan type make setup"
	@echo "To run certscan type make run"
	@echo "To uninstall certscan type make clean"
	@echo "--------------------------------------"

setup:
	@sudo ./install.sh

run:
	$(PYTHON) certscan.py -h

clean:
	rm -rf ${PATH_LOCAL}/${NAME_FILE}
	rm -rf ${INSTALL_DIR}/${NAME_FILE}
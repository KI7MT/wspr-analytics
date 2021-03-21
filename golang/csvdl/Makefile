# Makefile for building WSPR CSV Download CLI App 
#
# Name ..........: csvdl
# Copyright .....: Copyright (C) 2021, Greg Beam (KI7MT)
# License .......: Apache 2.0
# Description ...: WSPRnet CSV Download App
# Execution .....: As a normal user type: csvdl --year=2008 --month=03 --dest=$HOME/Downloads"

# Process variables
APP=csvdl
VERSION=1.0.0
BUILD=devel
DATE=$(shell date)
BINDIR=/usr/local/bin
CP=cp -u
CLEAR=clear
LOGUSER=$(shell $LOGNAME)

# Build rules
.PHONY: build
build: clean
	@$(CLEAR) ||:
	go build -ldflags \
		"-X main.appname=${APP} \
		-X main.version=v$(VERSION) \
		-X 'main.date=$(DATE)'" \
		-o ${APP} main.go
	@echo ''
	@echo 'Finished Build'
	@echo ''
	@echo "Usage: ./csvdl [args]"
	@echo "   -d, --dest string    destination for CSV file (default /home/${LOGNAME}/Downloads)"
	@echo '   -m, --month string   specify month like 03 (default "03")'
	@echo '   -v, --version        prints app version information'
	@echo '   -y, --year string    specify year like 2008 (default "2008")'
	@echo ''
	@echo 'Example:'
	@echo "  ./csvdl --year=2008 --month=03 --dest=/home/${LOGNAME}/Downloads"
	@echo ''

.PHONY: install
install: clean build
	${CP} ${APP} ${BINDIR}/

.PHONY: clean
clean:
	@go clean
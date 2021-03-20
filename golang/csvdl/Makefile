# Makefile for building WSPR CSV Download CLI App 
#
# Name ..........: csvdl
# Copyright .....: Copyright (C) 2021, Greg Beam (KI7MT)
# License .......: Apache 2.0
# Description ...: WSPRnet CSV Download App
# Execution .....: As normal user type: csvdl --year=2008 --month=03

# Process variables
APP=csvdl
VERSION=1.0.0
BUILD=devel
DATE=$(shell date)
BINDIR=/usr/local/bin
CP=cp -u
CLEAR=clear

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
	@echo "To run $(APP), use the following"
	@echo ""
	@echo "OPTIONS"
	@echo '  -y, --year string    specify year like 2009 (default "2008")'
	@echo '  -m, --month string   specify month like 01 (default "03")'
	@echo ''
	@echo 'Example:'
	@echo "  ${APP} --year=2008 -month=03"
	@echo ''

.PHONY: install
install: clean build
	${CP} ${APP} ${BINDIR}/

.PHONY: clean
clean:
	@go clean
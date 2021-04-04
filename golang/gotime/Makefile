# Makefile for building WSPR CSV Download CLI App 
#
# Name ..........: gotime
# Copyright .....: Copyright (C) 2021, Greg Beam (KI7MT)
# License .......: Apache 2.0
# Description ...: Golang Time Examples
# Execution .....: As normal user type: make && ./gotime

# Process variables
APP=gotime
VERSION=1.0.0
BUILD=devel
DATE=$(shell date)
BINDIR=/usr/local/bin
CP=cp -u
CLEAR=clear

build: clean
	@$(CLEAR) ||:
	mkdir ./dist
	go build -ldflags \
		"-X main.appname=${APP} \
		-X main.version=v$(VERSION) \
		-X 'main.date=$(DATE)'" \
		-o ./dist/${APP} ./main.go
	@echo ''
	@echo "To run $(APP), type:"
	@echo ""
	@echo "  ./dist/${APP}"
	@echo ''
	@echo "To install $(APP), type:"
	@echo ''
	@echo '  sudo make install'
	@echo ''
	@echo "To uninstall $(APP), type"
	@echo ''
	@echo '  sudo make uninstall'
	@echo ''

run:
	@clear ||:
	@go run -race main.go

install:
	@${CP} ./dist/${APP} ${BINDIR}/
	@echo ''
	@echo "To run $(APP), type:"
	@echo ""
	@echo "  ${APP}"
	@echo ''

uninstall:
	@rm -f ${BINDIR}/${APP}

clean:
	@go clean
	@rm -rf ./dist

.PHONY: build clean run install uninstall
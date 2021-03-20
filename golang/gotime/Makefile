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
	@echo 'Example:'
	@echo "  ./${APP}"
	@echo ''


.PHONY: run
run:
	@clear ||:
	@go run -race main.go


.PHONY: install
install: clean build
	${CP} ${APP} ${BINDIR}/

.PHONY: clean
clean:
	@go clean
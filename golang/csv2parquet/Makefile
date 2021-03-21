# Makefile for building WSPR CSV Download CLI App 
#
# Name ..........: csv2parquet
# Copyright .....: Copyright (C) 2021, Greg Beam (KI7MT)
# License .......: Apache 2.0
# Description ...: Golang app to cover WSRPnet CSV to Single Parquet format
# Execution .....: make && ./csv2parquet --src=<source> --desc=<location> --compression<type>

# Process variables
APP=csv2parquet
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
	@echo "  ./${APP} -s=${HOME}/Downloads/wsprnet/csv" -d=${HOME}/Downloads/wsprnet/parquet -f=wsprnet-2021-01.csv
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
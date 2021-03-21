# WSPR CSV Archive Download Applicaiton

`CSVDL` is a simple [Golang][] app that downloads CSV archive files from
the [WSPRnet][] download repository. Yes, you could use `curl`, `wget`, or any number of GNU tools, to perform the same task, and with many more options. However, this was just to show the simplicity of using [Golang][] to perform a similar task.

## Features

- Works on Linux, MacOS, and Windows
- Compiles and runs as expected on MSYS2 via `mingw-w64-x86_64-go` package
- Auto-Selects file extension: Windows = `.csv.zip`, Linux/MacOS = `.csv.gz`
- Default destination is $HOME/Downloads or %USERPROFILE%\Downloads if `--dest` flag is not set
- Uses posix flags for --year, --month, --version, --help and download --destination
- Auto-Creates `--dest` location if the user has write permissions

## Compiling

[Golang][] apps do not need to be compiled to run. However, you do need the [Golang][] framework installed for your operating system if not using a pre-compiled binary. Likewise, to compile the binaries, you also need the framwork installed.

See the following link for informaiton about setting up [Golang][] on your operating system (Windows, Linux, MacOS):

- [Golang Installation](https://golang.org/doc/install)
- Installing Golang in MSYS2


## Cloning The Repository

If you have [Git][] installed, you can simply clone the repository. If not, see [download from zip file](#downloading-from-zip-file) below.

```bash
# Clone the wspr-analytics repository
# Open a terminal, then type:

# Adjust location to your preference

cd ~/Downloads

# Clone the repository

git clone https://github.com/KI7MT/wspr-analytics.git

```

## Downloading From Zip File

If you dont want to install [Git][], you can simply download the Zip File from the following link:

- [Download WSPR Analytics][]

Extract the Zip File to a location of your choosing. Then open a terminal in the extracted location.

## Compiling The App

To compile and run the application, change directories to the the cloned or downloaded folder.

```bash
# In this example, I am using $HOME/Downloads
# Type the folloing commands to build and run

# Change direcories
cd $HOME/Downloads/wspr-analytics/golang/csvdl

# To compile the app, type:

make build

# command output
go build -ldflags \
        "-X main.appname=csvdl \
        -X main.version=v1.0.0 \
        -X 'main.date=Sat 20 Mar 2021 06:27:26 PM MDT'" \
        -o csvdl main.go

Finished Build

Usage: ./csvdl [args]
   -d, --dest string    destination for CSV file (default /home/ki7mt/Downloads)
   -m, --month string   specify month like 03 (default "03")
   -v, --version        prints app version information
   -y, --year string    specify year like 2008 (default "2008")

Example:
  ./csvdl --year=2008 --month=03 --dest=/home/ki7mt/Downloads
```

## Example Usage

Using the example invocation above will download the **smallest** [WSPRnet][] archive file once you run it.

You can substitute the following year / month combinations

>NOTE: in year 2008, the months start at 03, whereas the remaining years start at 01.

- Available Years: `2008 thu 2021`
- Available months: `01 02 03 04 05 06 07 08 09 10 11 12`

These values are not error-checked per say, so be carful when entering them manually.

```bash
# run the default example

./csvdl --year=2008 --month=03 --dest=/home/ki7mt/Downloads

# command output
Location ...: /home/ki7mt/Downloads
File .......: wsprspots-2008-03.csv.gz
Progress ...: 993 kB                              
Finished
```

## Version Information

To print the application version information, use the following:

> NOTE: the build date should be the time you compiled the application.

```bash
# To print the version info, type:

./csvdl --version

# command ouput
App Name .....:  csvdl
Version ......:  v1.0.0
Build Date ...:  Sat 20 Mar 2021 06:27:26 PM MDT
Description ..:  Golang app to download WSPRnet CSV Files.
```

## Output Destinations

You can specify the output destination for downloaded archive file using the (`-d=`) or (`--dest=`) flags. `csvdl` will attempt to create the directory if it does not exist. If you use a root owned folder, you will need to preface the command with `sudo` or similar for your operating system.

For Example:

```bash
# To use a custom destination, type:

./csvdl --year=2008 --month=03 --dest=$HOME/Downloads/wsprnet

# command output
Location ...: /home/ki7mt/Downloads/wsprnet
File .......: wsprspots-2008-03.csv.gz
Progress ...: 993 kB                              
Finished

# list the directory contents, type:

ls -al $HOME/Downloads/wsprnet

# output from command
total 980
drwxrwxr-x  2 ki7mt ki7mt   4096 Mar 20 18:38 .
drwxr-xr-x 18 ki7mt ki7mt   4096 Mar 20 18:38 ..
-rw-rw-r--  1 ki7mt ki7mt 993217 Mar 20 18:38 wsprspots-2008-03.csv.gz
```

## Multi-File Bash Shell Wrapper

If you want to download multiple files, you can eaily wrap `csvdl` in a shell script and loop
through the year month combintions of interest.

A small shell script would resemble the following:

```bash
#/usr/bin/env bash

# Description: Small shell wrapper for downloading WSPRnet CSV Files

# Save this script as: ..: test-csvdl.sh
# Update Permissions ....: chmod +x ./test-csvdl.sh
# Run the script with  ..: ./test-csvdl.sh

set -e

# Destination path
DOWNLOAD_DIR="$HOME/Downloads/wsprnet"

# this will download the months 03,04, and 05 for 2008
declare -a year=(2008)
declare -a month=(03 04 05)

# clear the screen
clear ||:

# outer loop for years
for y in "${year[@]}"
do
    # inner loop for months
    for m in "${month[@]}"
    do
        # download invocation
        ./csvdl --year="$y" --month="$m" --dest="$DOWNLOAD_DIR"
    done
done

# list items in the custom output location
ls -al "$DOWNLOAD_DIR"
echo ''

# exit the script
exit 0

# NOTE:
#   You could also add getopts to allow for command-line input for the year / month
#   combnations if desired.
```

### Bash Shell Wrapper Output

Output from the Bash wrapper above would look similar to:

```bash
Location ...: /home/ki7mt/Downloads/wsprnet
File .......: wsprspots-2008-03.csv.gz
Progress ...: 993 kB                              
Finished

Location ...: /home/ki7mt/Downloads/wsprnet
File .......: wsprspots-2008-04.csv.gz
Progress ...: 4.2 MB                              
Finished

Location ...: /home/ki7mt/Downloads/wsprnet
File .......: wsprspots-2008-05.csv.gz
Progress ...: 3.8 MB                              
Finished

total 8800
drwxrwxr-x  2 ki7mt ki7mt    4096 Mar 20 19:21 .
drwxr-xr-x 18 ki7mt ki7mt    4096 Mar 20 18:38 ..
-rw-rw-r--  1 ki7mt ki7mt  993217 Mar 20 19:21 wsprspots-2008-03.csv.gz
-rw-rw-r--  1 ki7mt ki7mt 4193734 Mar 20 19:21 wsprspots-2008-04.csv.gz
-rw-rw-r--  1 ki7mt ki7mt 3811506 Mar 20 19:21 wsprspots-2008-05.csv.gz
```










[Download WSPR Analytics]: https://github.com/KI7MT/wspr-analytics/archive/refs/heads/main.zip
[Git]: https://git-scm.com/
[Golang]: https://golang.org/
[WSPRnet]: https://wsprnet.org/drupal/downloads

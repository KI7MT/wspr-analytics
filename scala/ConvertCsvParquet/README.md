# Build Process

This is a sample Application using [Scala][] that performs the following:

* Reads a WSPRnet CSV from a path (/data/wspr/csv)
* Creates a Parquet file set to an output path (e.g /data/wspr/parquet/2020/02)

>NOTE If you re-run the script, the output Parquet directory will be overwritten.

## Framework Requirements

You must have Java, Scala, Spark and SBT available from the command line.

* Java openjdk version 1.8.0_275 or later
* Scala Version 2.12.12
* Spark 3.0.1
* SBT Tools 1.4.5

An easy way (on Linux / MacOS) to mange Java, Spark, Scala and SBT is
through an management tool called [sdkman][]. This tool allows
one to install virtually any combination of tools you need without
affecting your root file system. All the above requirements
can be installed and managed via [sdkman][].

## Test File Specs

The specs on the test file are:

* Test File : wsprspots-2020-02.csv
* Rows : 47,310,649 spots
* File Size Decompressed : 3.964 GB

## Build and Run The App

Run the following commands in order, and check your results.

```bash
#
# All commands are run from a terminal
#

# change the download location to whatever you prefer
cd ~/Downloads
wget -c http://wsprnet.org/archive/wsprspots-2020-02.csv.gz
gzip -dk wsprspots-2020-02.csv.gz

# set the path of the downloaded and extracted CSV file
csvfile=$PWD/wsprspots-2020-02.csv

# clone the repo
git clone https://github.com/KI7MT/wspr-analytics.git

# change directories and build the assembly
cd ./wspr-analytics/scala/ConvertCsvParquet

# clean and build
sbt clean assembly

# Run the following command
# NOTE : set local[8] to half of your total CPU count. 
spark-submit --master local[8] target/scala-2.12/ConvertCsvParquet-assembly-1.0.jar $csvfile
```

### Results

You should get results similar to the following:

>NOTE The time it takes will depend on your system resources (CPU, RAM, etc)

```bash
Object        : ConvertCsvParquet
Process File  : /data/wspr/raw/csv/wsprspots-2020-02.csv
File Out Path : /data/wspr/raw/parquet/2020/02
Tiimestame    : 2020-12-28 T 04:36:29.941
Description   : Convert CSV to Parquet

Process Steps to Create Parquet File(s)
- Create a Spark Session
- Create the Spot Schema
- Read the CSV file into a DataSet
- Write Parquet File(s), please wait...

Elapsed Time : 20.456 sec

Finished

```

[wpsrspots-2020-02.csv.zip]: http://wsprnet.org/archive/wsprspots-2020-02.csv.zip
[sdkman]: https://sdkman.io/
[Spark SQL]: https://spark.apache.org/docs/latest/sql-programming-guide.html
[Scala]: https://scala-lang.org/
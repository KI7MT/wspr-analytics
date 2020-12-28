# Build Process

This is a sample Application using [Scala][] that performs the following:

* Reads the Original CSV into a Spark DataFrame
* Creates a Parquet file set
* Performas a Query Count on Reporters Ordered Descending
* Reports Top (10) by spot count
* The Parquet compression is set to default => "snappy"

If you re-run the script, you need to remove the previous
directory beforehand as `df.wite.parquet()` will `not` overwrite
existing data.

## Framework Requirements

You must have Java, Scala, Spark and SBT available from the command line.

- Java openjdk version 1.8.0_275 or later
- Scala Version 2.12.12
- Spark 3.0.1
- SBT Tools 1.4.5

An easy way (on Linux / MacOS) to mange Java, Spark, Scala and SBT is
through an management tool called [sdkman][]. This tool allows
one to install virtually any combination of tools you need without
affecting your root file system. All the above requirements
can be installed and managed via [sdkman][].

## Test File Specs

The specs on the test file are:

- Test File : wsprspots-2020-02.csv
- Rows : 47,310,649 spots
- File Size Decompressed : 3.964 GB

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

# Ensure the output directory is free from previous runs
# Change 2020 and 02 to the year and month of CSV file being tested
rm -rf /tmp/wsprspots/2020/02

# Run the following command
# NOTE : set local[8] to half of your total CPU count. 
spark-submit --master local[8] target/scala-2.12/ConvertCsvToParquet-assembly-1.0.jar $csvfile
```

### Results

You should get results similar to the following:

>NOTE The time it takes will depend on your system resources (CPU, RAM, etc)

```bash
Application   : ConvertCsvToParquet
Process File  : wsprspots-2020-02.csv
File Out Path : /tmp/wsprspots/2020/02
Tiimestame    : 2020-12-27 T 02:45:14.346
Description   : Convert CSV to Parquet and Query Reporters

Process Steps to Create Parquet File(s)
- Create a Spark Session
- Add The Spot Schema
- Read The CSV into a DataSet
- Write Parquet File(s), please wait...

Elapsed Time : 30.836 sec

Process Steps to Query Reporters from Parquet Files(s)
- Read Parquet File(s)
- Select Reporters
- GroupBy and Count Reporters
- Sort Reporters Descending
- Execute the Query

+--------+------+
|Reporter| count|
+--------+------+
|   DK6UG|838081|
|  OE9GHV|690104|
|  EA8BFK|648670|
|   KD2OM|589003|
|KA7OEI-1|576788|
|   K4RCG|571445|
|     KPH|551690|
|    K9AN|480759|
|   DF5FH|480352|
|   DJ9PC|474211|
+--------+------+
only showing top 10 rows

Elapsed Time : 1.769 sec
```

[wpsrspots-2020-02.csv.zip]: http://wsprnet.org/archive/wsprspots-2020-02.csv.zip
[sdkman]: https://sdkman.io/
[Spark SQL]: https://spark.apache.org/docs/latest/sql-programming-guide.html
[Scala]: https://scala-lang.org/
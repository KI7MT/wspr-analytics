# Top Ten Reporters

This is a sample application using [Scala][] that performs the following:

* Reads the Original CSV into a Spark DataFrame
* Performas a Query Count on Reporters Ordered Descending
* Reports Top (10) by spot count 

### File Specs

The specs on the test file are:

- Test File : wsprspots-2020-02.csv
- Rows : 47,310,649 spots
- File Size Decompressed : 3.964 GB

If you use a different archive, make sure to you pass
the relative location to the script when running.

## Build and Run

Run the following commands in order, and check your results.

```bash
#
# All commands are run from a terminal
#

cd ~/Downloads
wget -c http://wsprnet.org/archive/wsprspots-2020-02.csv.gz
gzip -dk wsprspots-2020-02.csv.gz

# set the path of the downloaded and extracted CSV file
csvfile=$PWD/wsprspots-2020-02.csv

# clone the repo
git clone https://github.com/KI7MT/wspr-analytics.git

# change directories and build the assembly
cd ./wspr-analytics/scala/TopTenReporters

# clean and build
sbt clean assembly

# Runs the following command
spark-submit --master local[8] target/scala-2.12/TopTenReporter-assembly-1.0.jar $csvfile
```

### Results

You should get results similar to the following:

>NOTE The time it takes will depend on your system resources (CPU, RAM, etc)

```bash
Application  : TopTenReporter
Process File : wsprspots-2020-02.csv
Tiimestame   : 2020-12-27 T 02:36:01.265
Description  : Returns the Top Ten Reporters Grouped by Count

Process Steps for this application
- Creating the Schema
- Reading CSV into DataSet
- Selecting Reporters
- GroupBy and Count Reporters
- Sort Reporters Descending
- Query Execution

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

Query Time : 5.821 sec
```

[wpsrspots-2020-02.csv.zip]: http://wsprnet.org/archive/wsprspots-2020-02.csv.zip
[sdkman]: https://sdkman.io/
[Spark SQL]: https://spark.apache.org/docs/latest/sql-programming-guide.html
[Scala]: https://scala-lang.org/
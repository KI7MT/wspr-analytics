# Build Process

This is a sample Application using [Scala][] via [Spark SQL][]
get the Top Ten Reporters Grouped By Count for the designated
wsprspot year + month csv file. This example uses
[wpsrspots-2020-02.csv.zip][] as the source.

## Framework Requirments

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

If you use a different archive, make sure to update the
Scala script:

```scala
  // Change the csvfile, save and exit.
  // No other edits required.

  // The main entry point
  def main(args: Array[String]) {

    val csvfile: String = "wsprspots-2020-02.csv"
    val appname: String = "TenReporterDataset"
    val timestamp: String = LocalDateTime.now().toString()
    val description: String = "Returns the Top Ten Reporters Grouped by Count"
```

## Build and Run The App

Run the following commands in order, and check your results.

```bash
#
# Download   : http://wsprnet.org/archive/wsprspots-2020-02.csv.zip
# Extract to : data/wsprspots-2020-02.csv
# 

# clean
sbt clean

# build the fat Jar
sbt assembly

# cd data directory and run
cd data/
spark-submit ../target/scala-2.12/TopTenReporter-assembly-1.0.jar
```

### Results

You should get results similar to the following:

>NOTE The time it takes will depend on your system resources (CPU, RAM, etc)

```bash
Application  : TenReporterDataset
Process File : wsprspots-2020-02.csv
Tiimestame   : 2020-12-20 T 20:49:59.324
Description  : Returns the Top Ten Reporters Grouped by Count

- Creating the Schema
- Reading CSV into DataSet
- Selecting Reporters
- GroupBy and Count Reporters
- Sort Reporters Descending
- Executing Query

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

Query Elapsed time: 6971 msec
```

## ToDo

This script could be much more generic, and will be in the future

- Change the name to be more generic
- Add command-line option for FileName and Path
- Add command-line option for which column to count
- Add command-line option to set the number of rows to return

### Example
```scala

// <filename> the full path and file name to process
// <column-name> the column from the csv file to process
// <number> the number of rows to return

spark-submit CountByColumn-assembly-1.0.jar <file-name> <column-name> <number>

```

[wpsrspots-2020-02.csv.zip]: http://wsprnet.org/archive/wsprspots-2020-02.csv.zip
[sdkman]: https://sdkman.io/
[Spark SQL]: https://spark.apache.org/docs/latest/sql-programming-guide.html
[Scala]: https://scala-lang.org/
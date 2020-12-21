# Build Process

This is a sample Application using Scala DataSets to
get the Top Ten Reporters Grouped By Count for the designated
wsprspot year + month csv file. This example uses
[wpsrspots-2020-02.csv.zip][] as the source.

The specs on this file are:
- Rows 47,310,649 spots
- File decompressed 3.964 GB

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

## Framework Requirments

You must have Java, Scala, and Spark available from the command line.

- Java openjdk version 1.8.0_275 or later
- ScalaVersion 2.12.12
- Spark 3.0.1
- SBT Plugin 0.15.0

## Run The App

Run the commands in order, and check your results.

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
spark-submit ../target/scala-2.12/TopTenReporter-1.0.jar 
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

[wpsrspots-2020-02.csv.zip]: http://wsprnet.org/archive/wsprspots-2020-02.csv.zip
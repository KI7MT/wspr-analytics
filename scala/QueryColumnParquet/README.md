# Query Column Using Parquet Files

This is a sample Application using [Scala][] that performs the following:

* Reads a Parquet folder specificed by the user e.g. /data/wspr/raw/parquet/2020/02
* Performs a Query Count on a column specified by the user e.g. Reporter
* Reports GoubyBy Count and returns the Top (10) 

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

# NOTE: You must have previously run ConvertCvsToParquet before
#       useing this app, as it is looking for a Parquet folder,
#       not a CSV file.

# set the path to where you created the Parquet partition
inFolder="/data/wspr/raw/parquet/2020/02"

# set the colum you wish to GroupBy and Count
column="Reporter"

# clone the repo
git clone https://github.com/KI7MT/wspr-analytics.git

# change directories and build the assembly
cd ./wspr-analytics/scala/QueryColumnParquet

# clean and build
sbt clean assembly

# Run the following command
# NOTE : set local[8] to half of your total CPU count. 
spark-submit --master local[8] target/scala-2.12/QueryColumnParquet-assembly-1.0.jar $inFolder $column
```

## Results

You should get results similar to the following:

>NOTE The time it takes will depend on your system resources (CPU, RAM, etc)

```bash
Application   : QueryColumnParquet
Folder        : /data/wspr/raw/parquet/2020/02
Column        : Reporter
Tiimestame    : 2020-12-28T07:36:35.389
Description   : Query Column and Count using Parquet Folders

Process Steps to Query Reporter from Parquet Files(s)
- Create a Spark Session
- Read Parquet File(s)
- Select Reporter
- GroupBy and Count Reporter
- Sort Reporter Descending
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

Elapsed Time : 2.843 sec
```
## Query Reporter for November 2020

For Comparrison, here is the data from `2020-11`. November 2020 had over **70 Million** reports.

```bash
Application   : QueryColumnParquet
Folder        : /data/wspr/raw/parquet/2020/11
Column        : Reporter
Tiimestame    : 2020-12-28 T 07:42:09.275
Description   : Query Column and Count using Parquet Folders

Process Steps to Query Reporter from Parquet Files(s)
- Create a Spark Session
- Read Parquet File(s)
- Select Reporter
- GroupBy and Count Reporter
- Sort Reporter Descending
- Execute the Query

+--------+-------+
|Reporter|  count|
+--------+-------+
|  EA8BFK|1120739|
|  OE9GHV|1103335|
|   WA2TP| 847124|
|   KD2OM| 834896|
|  IW2NKE| 818315|
|   LX1DQ| 803347|
|   DK6UG| 794675|
|KA7OEI-1| 748356|
|   ON5KQ| 744727|
|  OE9HLH| 733580|
+--------+-------+
only showing top 10 rows

Elapsed Time : 2.8 sec

```

## Query CallSign for November 2020

This query is from the `CallSign` column.

```bash
Application   : QueryColumnParquet
Folder        : /data/wspr/raw/parquet/2020/11
Column        : CallSign
Tiimestame    : 2020-12-28 T 07:44:16.711
Description   : Query Column and Count using Parquet Folders

Process Steps to Query CallSign from Parquet Files(s)
- Create a Spark Session
- Read Parquet File(s)
- Select CallSign
- GroupBy and Count CallSign
- Sort CallSign Descending
- Execute the Query

+--------+------+
|CallSign| count|
+--------+------+
|   DK2DB|662784|
|   K4APC|600895|
|   ON7KO|557477|
|   KD6RF|541418|
|  WA4KFZ|531006|
|   W6LVP|466346|
|   DL6NL|438741|
|   N8VIM|438260|
|   DK8JP|403667|
|   G0CCL|386570|
+--------+------+
only showing top 10 rows

Elapsed Time : 2.445 sec

```
## Query Version for November 2020

```bash
Application   : QueryColumnParquet
Folder        : /data/wspr/raw/parquet/2020/11
Column        : Version
Tiimestame    : 2020-12-28 T 07:50:17.725
Description   : Query Column and Count using Parquet Folders

Process Steps to Query Version from Parquet Files(s)
- Create a Spark Session
- Read Parquet File(s)
- Select Version
- GroupBy and Count Version
- Sort Version Descending
- Execute the Query

+---------+--------+
|  Version|   count|
+---------+--------+
|     null|27015499|
| 1.3 Kiwi|13207118|
|    2.2.2|11199415|
|    2.1.2| 5906973|
|2.3.0-rc1| 2952306|
|    2.1.0| 2602903|
|2.3.0-rc2| 2366520|
|0.9_r4178| 2033622|
|    2.2.1| 2027954|
|    2.0.0| 1482597|
+---------+--------+
only showing top 10 rows

Elapsed Time : 2.492 sec

```


[wpsrspots-2020-02.csv.zip]: http://wsprnet.org/archive/wsprspots-2020-02.csv.zip
[sdkman]: https://sdkman.io/
[Spark SQL]: https://spark.apache.org/docs/latest/sql-programming-guide.html
[Scala]: https://scala-lang.org/
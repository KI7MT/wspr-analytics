# WSPR Analytics Using Scala

This apps in the directory are used for exploring the use of
[Apache Spark][] with [Scala](https://docs.scala-lang.org).

1. Converting CSV files to Parquet
1. Query both raw CSV files and Parquet partitions
1. Query Parquet Folders and GroupBy and Count Columns.
1. Example of how to convert Epoch times to humand readable values

## Basic Tool and Build Instructions

In each folder under you'll find instructions for compiling and running each
project or script as appropriate.

You must have Java, Scala, Spark and SBT, and Python available from the command line.

- Java openjdk version 1.8.0_275 or later
- Scala Version 2.12.12
- Spark 3.0.1
- SBT Tools 1.4.9

>IMPORTANT: The Spark / Scala combinations are very version specific. Check the [Spark][]
download page for recommended version combinaitons if you deviate from what is listed here.
As of this writing, Spark 3.0.1 and above was built with Scala 2.12.12. For the least
amount of frustration, stick with what's known to work.

An easy way (on Linux / MacOS) to manage Java, Spark, Scala and SBT is
through an management tool called [sdkman][]. This tool allows
one to install virtually any combination of tools you need without
affecting your root file system. All the above requirements can be
installed and managed via [sdkman][].

## Sample Applications

The following is a list of sample applications that can be performed on the various
[WSPR Spots][] CSV Files. As new script are written, they will appear in the list below.

* [Query Columns using Parquet Folders][]
* [Query Top Ten Reporters][]
* [Convert CSV to Parquet][]
* [Epoch Conversion][]
* [Delta Create Table][]


[Apache Spark]: https://spark.apache.org
[Scala]: https://docs.scala-lang.org
[sdkman]: https://sdkman.io/
[WSPR Spots]: https://wsprnet.org/drupal/downloads
[Spark]: https://spark.apache.org/downloads.html

[Query Columns using Parquet Folders]: https://github.com/KI7MT/wspr-analytics/tree/main/scala/QueryColumnParquet
[Query Top Ten Reporters]: https://github.com/KI7MT/wsprana-spark-scala/tree/main/scala/TopTenReporters
[Convert CSV to Parquet]: https://github.com/KI7MT/wspr-analytics/tree/main/scala/ConvertCsvParquet
[Delta Create Table]: https://github.com/KI7MT/wspr-analytics/tree/main/spark/DeltaCreateTable
[Epoch Conversion]: https://github.com/KI7MT/wspr-analytics/tree/main/spark/EpochConversion
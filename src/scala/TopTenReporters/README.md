# Build Process

This is a sample Application using Scala DataSets to
get the TopTenReporter by Couny for the designated
wsprspot year + month

## Framework Requirments

You must have Java, Scala, and Spark available from the command line.

- Java openjdk version 1.8.0_275 or later
- ScalaVersion 2.12.12
- Spark 3.0.1
- SBT Plugin 0.15.0

## Run The App

Make sure all the SBT commands work, just for completness.

```bash

# Copy the November 2020-11 CSV to the data directory
# If you use a different year / moth combination, adjust the script
#
# data/wsprspots-2020-11.csv

# clean
sbt clean

# compile the project
sbt compile

# build a thin Jar
sbt package

# clean again
sbt clean

# build the fat Jar
sbt assembly

# cd data directory and run
cd data
spark-submit ../target/scala-2.12/TopTenReporter-1.0.jar 
```
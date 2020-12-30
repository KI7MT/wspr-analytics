package com.ki7mt.spark

import org.apache.log4j.PropertyConfigurator
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import java.time.ZoneId


object EpocConversion {

  def main(args: Array[String]): Unit = {
    PropertyConfigurator.configure("log4j/log4j.properties")

    // IMPORTANT: When converting EPOCH times, you must do so with the
    // to_utc_timestamp method. This requires telling the system what Zone
    // your computer is in (the one doing the conversion) in order to get
    // the correct unix time.
    val z = ZoneId.systemDefault()
    val zoneId = z.getId

    println("Process Steps For Processing A CSV File")
    println("- Create a Spark Session")

    val spark: SparkSession = SparkSession.builder()
      .appName("Read CSV and Show Schema")
      .master("local[*]")
      .getOrCreate()

    println("- Create the Spot Schema")
    val spotSchema = new StructType()
      .add("SpotID", LongType, nullable = false)
      .add("Timestamp", IntegerType, nullable = false)
      .add("Reporter", StringType, nullable = false)
      .add("RxGrid", StringType, nullable = false)
      .add("SNR", ByteType, nullable = false)
      .add("Frequency", DoubleType, nullable = false)
      .add("CallSign", StringType, nullable = false)
      .add("Grid", StringType, nullable = false)
      .add("Power", ByteType, nullable = false)
      .add("Drift", ByteType, nullable = false)
      .add("Distance", ShortType, nullable = false)
      .add("Azimuth", ByteType, nullable = false)
      .add("Band", ByteType, nullable = false)
      .add("Version", StringType, nullable = true)
      .add("Code", ByteType, nullable = true)

    println("- Read the CSV file into a DataSet")
    val df = spark.sqlContext
      .read.format("csv")
      .option("delimiter", ",")
      .option("header", "false")
      .schema(spotSchema)
      .load("/home/ki7mt/Dev/Data/wspr/wsprspots-2020-11.csv")

    println("- Select the column we want to process")
    val res = df.select("*")
      .withColumn("x_TimeStamp", date_format(col("TimeStamp")
        .cast(DataTypes.TimestampType), "yyyy-MM-dd HH:mm:ss"))

    //res.printSchema()

    // See not above about ZoneId, it's important.
    println("- Setup Epoh Conversion")
    val res1 = res.select("*")
      .withColumn("x_timestamp", to_utc_timestamp(col("x_TimeStamp"), zoneId))
      .withColumn("x_date", to_date(col("x_TimeStamp")))
      .withColumn("x_year", year(col("x_TimeStamp")))
      .withColumn("x_month", month(col("x_TimeStamp")))
      .withColumn("x_day", dayofmonth(col("x_TimeStamp")))
      .withColumn("x_hour", hour(col("x_TimeStamp")))
      .withColumn("x_minute", minute(col("x_TimeStamp")))

    //res1.printSchema()

    //println("- Print Res1 Schema")
    //res1.printSchema()
    println("- Execute the Query")
    time {
      res1.show(5)
    }

    println("\nGetting final row count, please wait...")
    val rowcount = res1.count()
    println(f"Epoch Conversion Processed : ($rowcount%,d) Spots ")

  } // END - Main CLass

  // timer function
  def time[R](block: => R): R = {
    val t0 = System.currentTimeMillis()
    val result = block // call the block
    val t1 = System.currentTimeMillis()
    val elapsedTimeMsec: Float = t1 - t0
    val elapsedTime: Float = elapsedTimeMsec / 1000
    println(f"Elapsed Time : $elapsedTime sec")
    result
  }

} // END - BasicExample

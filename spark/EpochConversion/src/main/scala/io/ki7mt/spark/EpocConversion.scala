package com.ki7mt.spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import java.time.ZoneId

object EpocConversion {

  case class RawSpot(
                      SpotId: Long,
                      TimeStamp: Integer,
                      Reporter: String,
                      RxGrid: String,
                      SNR: Byte,
                      Frequency: Double,
                      CallSign: String,
                      Grid: String,
                      Power: Byte,
                      Drift: Byte,
                      Distance: Short,
                      Azimuth: Byte,
                      Band: Byte,
                      Version: String,
                      Code: Byte
                    )

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

  def main(args: Array[String]): Unit = {

    val debug: Boolean = false
    val z = ZoneId.systemDefault()
    val zoneId = z.getId

    println("Process Steps For Processing A CSV File")
    println("- Create a Spark Session")

    val spark: SparkSession = SparkSession.builder()
      .appName("Read CSV and Show Schema")
      .master("local[16]")
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
    import spark.implicits._
    val ds = spark.read
      .option("delimiter", ",")
      .option("header", "false")
      .schema(spotSchema)
      .csv(path = "data/spots-2020-02-100K.csv")
      .as[RawSpot]

    println("- Select the column we want to process")
    val res = ds.select("*")
      .withColumn("x_TimeStamp", date_format(col("TimeStamp")
      .cast(DataTypes.TimestampType), "yyyy-MM-dd HH:mm:ss"))

    // only print the schema in Debug Mode
    if (debug) {
      res.printSchema()
    }

    // See not above about ZoneId, it's important.
    println("- Setup Epoh Conversion")
    val res1 = res.select("*")
      .withColumn("x_timestamp", to_utc_timestamp(col("x_TimeStamp"), zoneId))
      .withColumn("x_date", to_date(col("x_TimeStamp")))
      .withColumn("x_year", year(col("x_TimeStamp")).cast(ShortType))
      .withColumn("x_month", month(col("x_TimeStamp")).cast(ByteType))
      .withColumn("x_day", dayofmonth(col("x_TimeStamp")).cast(ByteType))
      .withColumn("x_hour", hour(col("x_TimeStamp")).cast(ByteType))
      .withColumn("x_minute", minute(col("x_TimeStamp")).cast(ByteType))

    if (debug) {
      println("- Print Res1 Schema")
      res1.printSchema()
    }

    println("- Execute the Query")
    time {
      res1.show(5)
    }

    println("\nGetting final row count, please wait...")
    time {
      val rowcount = res1.count()
      println(f"Epoch Conversion Processed : ($rowcount%,d) Spots ")
    }

  } // END - Main CLass

  // TODO: Move `case class RawSpot` to a beans package
  // TODO: Add column for calculating km to statue miles
  // TODO: Add column for standardized Band field
  // TODO: Add default value (nr) for applications 'not reporting" their app version
  /**
   * This represents the WSPR Spot as it arrives from
   * the CSV File of of WSPRnet. Additional
   *
   * @param SpotId    Integer representing the spot id from wspr net
   * @param TimeStamp Integer EPOCH time representing the time of the spot
   * @param Reporter  String The station reporting the spot
   * @param RxGrid    String representing the reporters Maiden Head ggrid square
   * @param SNR       Byte Signal to noise ratio in dB as reported by the receiving software.
   * @param Frequency Double Frequency of the received signal in MHz
   * @param CallSign  String Call sign of the transmitting station
   * @param Grid      String Maidenhead grid locator of transmitting station, in 4 or 6 character format.
   * @param Power     Byte Power, as reported by transmitting station in the transmission. Units are dBm
   * @param Drift     Byte The measured drift of the transmitted signal as seen by the receiver, in Hz/minute.
   * @param Distance  Integer Approximate distance between tx and rx along the great circle (short) path, in kilometers.
   * @param Azimuth   Integer Approximate direction, in degrees, from tx and rx station along the great circle (short) path.
   * @param Band      Integer Band of operation, computed from frequency as an index for faster retrieval.
   * @param Version   String Version string of the WSPR software in use by the receiving station.
   * @param Code      Integer Archives generated after 22 Dec 2010 have an additional integer Code field.
   *                  Non-zero values will indicate that the spot is likely to be erroneous.
   */

} // END - EpocConversion

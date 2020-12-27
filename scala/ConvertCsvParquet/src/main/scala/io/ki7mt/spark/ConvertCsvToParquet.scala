package io.ki7mt.spark

import java.time.LocalDateTime

import org.apache.log4j._

import org.apache.spark.sql.types.{IntegerType, StringType, StructType, DoubleType}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Get The Top Ten Reporters by Count
object ConvertCsvToParquet {

  case class Spot(SpotId: Integer, 
                  TimeStamp: Integer,
                  Reporter: String,
                  RxGrid: String,
                  SNR: Integer,
                  Frequency: Double,
                  CallSign: String,
                  Grid: String,
                  Power: Integer,
                  Drift: Integer,
                  Distance: Integer,
                  Azimuth: Integer,
                  Band: Integer,
                  Version: String,
                  Code: Integer
                  )

  // Changed ro Milliseconds as Nanoseconds is a bit to high in percision
  // Also added the Long $et for better readability
  // https://biercoff.com/easily-measuring-code-execution-time-in-scala/
  def time[R](block: => R): R = {
      val t0 = System.currentTimeMillis()
      val result = block  // call the block
      val t1 = System.currentTimeMillis()
      val elapsedTimeMsec: Float = (t1 - t0)
      val elapsedTime: Float = (elapsedTimeMsec / 1000)

      println(f"Elapsed Time : $elapsedTime sec\n")
      result
  }

  // The main entry point
  def main(args: Array[String]) {

    if (args.length <= 0) {
      println("\nInput File Error")
      println("Usage: ConvertCsvToParquet-assembly-1.0.jar $csvfile")
      println("Example: wsprspots-2020-02.csv")
      System.exit(1)
    }

    val csvfile: String = args(0)
    val appname: String = "ConvertCsvToParquet"
    val timestamp: String = LocalDateTime.now().toString()
    val description: String = "Convert CSV to Parquet and Query Reporters"
  
    // Setup the output path
    val pathSplit : Array[String] = csvfile.split("/")
    val fileName : String = pathSplit.last
    val shortName: String = fileName.substring(0, fileName.lastIndexOf('.'))
    val nameArray : Array[String] = shortName.split("-")

    // set the output directory
    // example: /tmp/wsprspots/2020/02
    val outputDir : String = "/tmp/" + nameArray(0) + "/" + nameArray(1) + "/" + nameArray(2).replace(".csv", "")

    println(s"\nApplication   : $appname")
    println(s"Process File  : $csvfile" )
    println(s"File Out Path : $outputDir")
    println(s"Tiimestame    : $timestamp")
    println(s"Description   : $description\n" )

    // Set the Java Log Level
    Logger.getLogger("org").setLevel(Level.ERROR)

    // Spark Session: local[*] uses all cores on the local machine
    println("Process Steps to Create Parquet File(s)")
    println("- Create a Spark Session")
    val spark = SparkSession
      .builder
      .appName("ConvertCsvToParquet")
      //.master("local[16]")
      .getOrCreate()

    // create the schema
    println("- Add The Spot Schema")
    val spotSchema = new StructType()
      .add("SpotID", IntegerType, nullable = false)
      .add("Timestamp", IntegerType, nullable = false)
      .add("Reporter", StringType, nullable = false)
      .add("RxGrid", StringType, nullable = false)
      .add("SNR", IntegerType, nullable = false)
      .add("Frequency", DoubleType, nullable = false)
      .add("CallSign", StringType, nullable = false)
      .add("Grid", StringType, nullable = false)
      .add("Power", IntegerType, nullable = false)
      .add("Drift", IntegerType, nullable = false)
      .add("Distance", IntegerType, nullable = false)
      .add("Azimuth", IntegerType, nullable = false)
      .add("Band", IntegerType, nullable = false)
      .add("Version", StringType, nullable = false)
      .add("Code", IntegerType, nullable = true)

    // Read the CSV into the DataSet
    println("- Read The CSV into a DataSet")
    import spark.implicits._
    val ds = spark.read
      .schema(spotSchema)
      .csv(csvfile)
      .as[Spot]

    //println("\nPrint the Spot Schema")
    //ds.printSchema()

    println("- Write Parquet File(s), please wait...\n")
    val df = ds.toDF()
    time { df.write.parquet(outputDir) }

    println("Process Steps to Query Reporters from Parquet Files(s)")
    println("- Read Parquet File(s)")
    val ds1 = spark.read.parquet(outputDir)
    
    // Select only the reporter column as that's all we need
    println("- Select Reporters")
    val reporter = ds1.select("Reporter")

    // Group and count
    println("- GroupBy and Count Reporters")
    val rank = reporter.groupBy("Reporter").count()

    // Sort the resulting dataset by count column descending (default is assending)
    println("- Sort Reporters Descending")
    val sortedResults = rank.sort(desc("Count"))

    // Print results from the dataset
    println("- Execute the Query\n")
    time {sortedResults.show(10)}

    // shutdown spark engine
    spark.stop()

  } // END - main method

} // END - CnvertCsvToParquet
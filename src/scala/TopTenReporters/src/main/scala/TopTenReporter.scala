package com.ki7mt.spark

import org.apache.spark.sql.types.{IntegerType, StringType, StructType}
import org.apache.log4j._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

import java.time.LocalDateTime

// Get The Top Ten Reporters by Count
object TopTenReporterDataset {

  case class Reporter(SpotID: Integer, Timestamp: Integer, Reporter: String)

  // I changed it to Milliseconds as Nanoseconds is a bit to high in percision
  // Also added the Long $et for better readability
  // https://biercoff.com/easily-measuring-code-execution-time-in-scala/
  def time[R](block: => R): R = {
      val t0 = System.currentTimeMillis()
      val result = block  // call the block
      val t1 = System.currentTimeMillis()
      val elapsedTime: Long = (t1 - t0)
      println(f"Query Time : $elapsedTime msec\n")
      result
  }

  // The main entry point
  def main(args: Array[String]) {

    val csvfile: String = "wsprspots-2020-02.csv"
    val appname: String = "TenReporterDataset"
    val timestamp: String = LocalDateTime.now().toString()
    val description: String = "Returns the Top Ten Reporters Grouped by Count"

    println(s"\nApplication  : $appname")
    println(s"Process File : $csvfile" )
    println(s"Tiimestame   : $timestamp")
    println(s"Description  : $description\n" )

    // Set the Java Log Leve
    Logger.getLogger("org").setLevel(Level.ERROR)

    // Spark Session: local[*] uses all cores on the local machine
    val spark = SparkSession
      .builder
      .appName("TopTenReporters")
      .master("local[*]")
      .getOrCreate()

    // create the schema
    println("- Creating the Schema")
    val reporterSchema = new StructType()
      .add("SpotID", IntegerType, nullable = false)
      .add("Timestamp", IntegerType, nullable = false)
      .add("Reporter", StringType, nullable = false)
      
    // Read the CSV into the DataSet
    println("- Reading CSV into DataSet")
    import spark.implicits._
    val reporterDS = spark.read
      .schema(reporterSchema)
      .csv(csvfile)
      .as[Reporter]
    
    // Select only the reporter column as that's all we need
      println("- Selecting Reporters")
    val reporter = reporterDS.select("Reporter")

    // Group and count
    println("- GroupBy and Count Reporters")
    val rank = reporter.groupBy("Reporter").count().alias("Count")

    // Sort the resulting dataset by count column descending (default is assending)
    println("- Sort Reporters Descending")
    val sortedResults = rank.sort(desc("Count"))

    // Print results from the dataset
    println("- Executing Query\n")
    time {sortedResults.show(10)}

  } // END - main method

} // END - TopTenReporterDataset
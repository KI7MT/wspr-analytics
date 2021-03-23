package io.ki7mt.spark

import java.time.LocalDateTime

import org.apache.log4j._

import org.apache.spark.sql.types.{IntegerType, StringType, StructType, DoubleType}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Get The Top Ten Reporters by Count
object QueryColumnParquet {

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

    // Set the Java Log Level
    Logger.getLogger("org").setLevel(Level.ERROR)

    // TODO: convert to scopt
    if (args.length <= 1) {
      println("\nInput Processing Error\n")
      println("The conversion script rerquires atwo parameters\n")
      println("Input Folder     : /data/wspr/raw/parquet/2020/02")
      println("Column           : Reporter")
      println("\nExample\n")
      println("spark-submit --master local[8] target/scala-2.12/QueryColumnParquet-assembly-1.0.jar $inFolder $column\n")
      System.exit(1)
    }

    val inFolder: String = args(0)
    val column: String = args(1)
    val appname: String = "QueryColumnParquet"
    val timestamp: String = LocalDateTime.now().toString()
    val description: String = "Query Column and Count using Parquet Folders"

    println(s"\nApplication   : $appname")
    println(s"Folder        : $inFolder" )
    println(s"Column        : $column")
    println(s"Tiimestame    : $timestamp")
    println(s"Description   : $description\n" )

    // Spark Session: local[*] uses all cores on the local machine
    println(s"Process Steps to Query $column from Parquet Files(s)")
    println("- Create a Spark Session")
    val spark = SparkSession
      .builder
      .appName(s"Query $column with Parquet")
      .getOrCreate()

    println("- Read Parquet File(s)")
    val ds = spark.read.parquet(inFolder)
    
    // Select only the column providerd by the user
    println(s"- Select $column")
    val selection = ds.select(column)

    // Group and count
    println(s"- GroupBy and Count $column")
    val rank = selection.groupBy(column).count().alias("Count")

    // Sort the resulting dataset by count column descending (default is assending)
    println(s"- Sort $column Descending")
    val sortedResults = rank.sort(desc("Count"))

    // Print results from the dataset
    println("- Execute the Query\n")
    time {sortedResults.show(10)}

    // shutdown spark engine
    spark.stop()

  } // END - main method

} // END - CnvertCsvToParquet
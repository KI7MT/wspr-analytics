package com.ki7mt.spark

import org.apache.spark.sql.types.{IntegerType, StringType, StructType}
import org.apache.log4j._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Get The Top Ten Reporters by Count
object TopTenReporterDataset {

  case class Reporter(SpotID: Integer, Timestamp: Integer, Reporter: String)

  // Our main function where the action happens 
  def main(args: Array[String]) {
   
    // Change this to the file located in /data/
    val csvfile = "wsprspots-2020-02.csv"
    println(f" - Processing File : $csvfile" )

    // Set the Java Log Leve
    Logger.getLogger("org").setLevel(Level.ERROR)

    // Spark Session: local[*] uses all cores on the local machine
    val spark = SparkSession
      .builder
      .appName("TopTenReporters")
      .master("local[*]")
      .getOrCreate()

    // Add the schema struct
    println(" - Creating the Schema")
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
    val rank = reporter.groupBy("Reporter").count()

    // Sort the resulting dataset by count column descending (default is assending)
    println("- Sort Reporters Descending")
    val sortedResults = rank.sort(desc("count"))

    // Print results from the dataset
    println(" - Executing Query")
    sortedResults.show(10)

  }

}
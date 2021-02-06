package io.ki7mt.spark

import java.time.LocalDateTime
import org.apache.commons.io.FileUtils
import java.io.File

import org.apache.log4j._

import org.apache.spark.sql.types.{IntegerType, StringType, StructType, DoubleType, LongType, ByteType, ShortType}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Get The Top Ten Reporters by Count
object DeltaCreateTable {

  // DataSet case class
  case class Spot(SpotId: Long, 
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

  // timimg function
  def time[R](block: => R): R = {
      
      val t0 = System.currentTimeMillis()
      val result = block  // call the block
      val t1 = System.currentTimeMillis()
      val elapsedTimeMsec: Float = (t1 - t0)
      val elapsedTime: Float = (elapsedTimeMsec / 1000)

      println(f"Elapsed Time : $elapsedTime sec\n")
      result
  }

  // main entry point
  def main(args: Array[String]) {

    // Set the Java Log Level
    Logger.getLogger("org").setLevel(Level.ERROR)

    if (args.length <= 1) {
      println("\nInput Processing Error\n")
      println("The conversion script rerquires two parameters\n")
      println("Input File       : /path/to/some/wsprspots-2020-12.csv")
      println("Output Directory : /tmp/delta/wspr/2020/11")
      println("\nExample\n")
      println("spark-sumbit --master local[8] DeltaCreateTable-assembly-1.0.jar $inFile $outDir\n")
      System.exit(1)
    }
 
    val inFile: String = args(0)
    val outDir: String = args(1)
    val appname: String = "DeltaCreateTable"
    val timestamp: String = LocalDateTime.now().toString()
    val description: String = "Convert CSV to Delta Table"

    val file = new File(args(1))
    if (file.exists()) FileUtils.deleteDirectory(file)

    if (scala.reflect.io.File(inFile).exists) {
      println(s"\nObject         : $appname")
      println(s"Process File    : $inFile" )
      println(s"Folder Out Path : $outDir")
      println(s"Tiimestame      : $timestamp")
      println(s"Description     : $description\n" )

      println("Process Steps to Create Delta Lake Table")
      println("- Create a Spark Session")
      val spark = SparkSession
        .builder
        .appName("Convert CSV To Delta Lake Table")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()

        println("- Create the Spot Schema")
        val spotSchema = new StructType()
          .add("SpotID", LongType, nullable=false)
          .add("Timestamp", IntegerType,nullable=false)
          .add("Reporter", StringType,nullable=false)
          .add("RxGrid", StringType,nullable=false)
          .add("SNR", ByteType,nullable=false)
          .add("Frequency", DoubleType,nullable=false)
          .add("CallSign", StringType,nullable=false)
          .add("Grid", StringType,nullable=false)
          .add("Power", ByteType,nullable=false)
          .add("Drift", ByteType,nullable=false)
          .add("Distance", ShortType,nullable=false)
          .add("Azimuth", ByteType,nullable=false)
          .add("Band", ByteType,nullable=false)
          .add("Version", StringType,nullable=true)
          .add("Code", ByteType,nullable=true)

        println("- Read the CSV file into a DataSet")
        import spark.implicits._
        val ds = spark.read
          .schema(spotSchema)
          .csv(inFile)
          .as[Spot]

        println("- Write Delta Table, please wait...\n")
        val df = ds.toDF()
        time { df.write.format("delta").save(outDir) }
        
        // shutdown spark engine
        spark.stop()

        println("Finished\n")

    } else { // if the script could not find input file

      println(f"\nCould not find : $inFile")
      println("Please check the file path and name, then try again.\n")
    
    }

  } // END - main method

} // END - CnvertCsvParquet Object
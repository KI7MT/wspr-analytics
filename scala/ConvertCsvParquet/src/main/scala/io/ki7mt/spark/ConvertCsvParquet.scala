package io.ki7mt.spark

import java.time.LocalDateTime

import org.apache.log4j._

import org.apache.spark.sql.types.{IntegerType, StringType, StructType, DoubleType}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Get The Top Ten Reporters by Count
object ConvertCsvParquet {

  // DataSet case class
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

    // TODO: convert to scopt
    if (args.length <= 1) {
      println("\nInput Processing Error\n")
      println("The conversion script rerquires two parameters\n")
      println("Input File       : /path/to/some/wsprspots-2020-12.csv")
      println("Output Directory : /tmp/wspr/raw/parquet/2020/11")
      println("\nExample\n")
      println("spark-sumbit --master local[8] ConvertCsvParquet-assembly-1.0.jar $inFile $outDir\n")
      System.exit(1)
    }

    val inFile: String = args(0)
    val outDir: String = args(1)
    val appname: String = "ConvertCsvParquet"
    val timestamp: String = LocalDateTime.now().toString()
    val description: String = "Convert CSV to Parquet"

    if (scala.reflect.io.File(inFile).exists) {
      println(s"\nObject        : $appname")
      println(s"Process File  : $inFile" )
      println(s"File Out Path : $outDir")
      println(s"Tiimestame    : $timestamp")
      println(s"Description   : $description\n" )

      println("Process Steps to Create Parquet File(s)")
      println("- Create a Spark Session")
      val spark = SparkSession
        .builder
        .appName("Convert CSV To Parquet")
        .getOrCreate()

      println("- Create the Spot Schema")
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
        .add("Version", StringType, nullable = true)
        .add("Code", IntegerType, nullable = true)


        println("- Read the CSV file into a DataSet")
        import spark.implicits._
        val ds = spark.read
          .schema(spotSchema)
          .csv(inFile)
          .as[Spot]

        println("- Write Parquet File(s), please wait...\n")
        val df = ds.toDF()
        time { df.write.mode("overwrite").parquet(outDir) } // set to overwrite mode

      // shutdown spark engine
      spark.stop()

    } else { // if the script could not find input file

      println(f"\nCould not find : $inFile")
      println("Please check the file path and name, then try again.\n")
    
    }

  } // END - main method

} // END - CnvertCsvParquet Object
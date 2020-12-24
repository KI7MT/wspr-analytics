package com.ki7mt.spark

import org.apache.log4j._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

/** Count up how many of each word occurs in the gplv3.txt license */
object WordCountDataset {

  case class License(value: String)

  def main(args: Array[String]) {

    // set logger warnings ( this can be better adjusted  in spark-conf.sh )
    Logger.getLogger("org").setLevel(Level.ERROR)

    // Spark session
    val spark = SparkSession
      .builder
      .appName("WordCount")
      .master("local[*]")
      .getOrCreate()

    // Read lines into Dataset
    import spark.implicits._

    // ANOTHER WAY TO DO IT (Blending RDD's and Datasets)
    val licenseRDD = spark.sparkContext.textFile("data/gpl3.txt")
    val wordsRDD = licenseRDD.flatMap(x => x.split("\\W+"))
    val wordsDS = wordsRDD.toDS()

    val lowercaseWordsDS = wordsDS.select(lower($"value").alias("word"))
    val wordCountsDS = lowercaseWordsDS.groupBy("word").count()
    val wordCountsSortedDS = wordCountsDS.sort("count")
    wordCountsSortedDS.show(wordCountsSortedDS.count.toInt)
  }
}

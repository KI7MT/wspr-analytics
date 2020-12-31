
>Apache Spark™ is a unified analytics engine for large-scale data processing. 
>
><cite>[Apache Spark Project][]</cite>

## Framework Requirements

You must have Java, Scala, Spark and SBT available from the command line for all
[Scala Projects][] listed in this section.

- Java openjdk version 1.8.0_275 or later
- Scala Version 2.12.12
- Spark 3.0.1
- SBT Tools 1.4.5

An easy way (on Linux / MacOS) to mange Java, Spark, Scala and SBT is
through an management tool called [sdkman][]. This tool allows
one to install virtually any combination of tools you need without
affecting your root file system. All the above requirements
can be installed and managed via [sdkman][].

If you can't run : `spark-shell` and have it present the REPL,
see [Installing Spark](../setup/install-spark.md)

>NOTE: Your version of Java and Scala may be different.

```scala

(wsprana) ki7mt@3950X:~ $ spark-shell 
Spark context Web UI available at http://localhost:4040
Spark context available as 'sc' (master = local[*], app id = local-1609375750950).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.0.1
      /_/
         
Using Scala version 2.12.10 (OpenJDK 64-Bit Server VM, Java 1.8.0_275)
Type in expressions to have them evaluated.
Type :help for more information.

scala> 
```

### Read and Query DataSet

```scala
   // Read the CSV into the DataSet
    println("- Reading CSV into DataSet")
    import spark.implicits._
    val reporterDS = spark.read
      .schema(reporterSchema)
      .csv(csvfile)
      .as[Reporter]

    // Print results from the dataset
    println("- Query Execution\n")
    time {sortedResults.show(10)}
```

[Apache Spark Project]: https://spark.apache.org/
[Scala Projects]: https://scala-lang.org/
[sdkman]: https://sdkman.io/
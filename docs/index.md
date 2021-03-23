# WSPR Analytics

In the early days (March 2008), [WSPR Spots][] measured in the hundreds of thousands per month. Today,
that number has increased to over 75+ Million per month and shows no sign of abatement.
By any reasonable definition, it is safe to say that [WSPR][] has entered the realm of [Big Data][].

## Features

- Full Tool Chain Installation and Environment Setup Guide(s)
- Tutorials, experiments, and tests on large data sets
- Exposure to leading-edge technologies in the realm of Big Data Processing
- Hints, tips and tricks for keeping your Linux distro running smooth
- And eventually, produce useful datasets for the greater Amateur Radio Community to consume

## Primary Focus

The focus of this project is to provide a set of tools to download, manage, transform and query
WSPR DataSets using modern [Big Data][] frameworks.

## Folder Descriptions

Several frameworks are used in this repository. The following matrix provides a short description
of each, and their intended purpose.

* `docs` - Python, MkDocs for repository documentation
* `golang` - General purpose command line apps and utilities
* `java` - Java, Maven, and SBT apps for RDD and Avro examples
* `notebooks` - Jupyter Notebooks  for basic test and visualization
* `pyspark` - Python, PyArrow scripts that interact with CSV and Parquet files
* `spark` -Scala programs to perform tasks
* `wsprdaemon` - Python, Scala, Psql utilities related to the WSPR Daemon project
* `wsprana` - Python, (soon to be retired)


Pay close attention to the `README` files as they lay out how to setup the
tools needed to run their respective scripts or application.

## Base Tool Requirements

You must have Python, Java, PySpark / Spark (Scala) and SBT available from the command line.

- Java OpenJDK version 1.8.0_275 or later
- Python 3.7 or 3.8, PyArrow has issues with 3.9 at present
- PySpark from PyPi
- Apache Arrow 2.0+
- Scala 2.12.12 - patch version 10,11,12,13 also work with Spark 3.0.1 / 3.1.1
- Spark 3.0.1
- PostgreSQL Database (local, remote, Docker, Vagrant, etc)
- Optional ClickHouse High Performance Database

>IMPORTANT: The Spark / Scala combinations are version sensitive. Check the [Spark][]
download page for recommended version combinations if you deviate from what is listed here.
As of this writing, Spark 3.0.1 and above was built with Scala 2.12.10. For the least
amount of frustration, stick with what's known to work (any of the 2.12.xx series)

## Data Sources and Processing

The main data source will be the monthly [WSPRNet Archives][]. At present, there is no plan to pull
nightly updates. That could change if a reasonable API is identified. [WSPR Daemon][]

The tools (apps/scripts) will be used to convert the raw CSV files into a format better suited for parallel processing,
namely, [Parquet][]. Read speeds, storage footprints, and ingestion improve dramatically with this storage format.
However, there is a drawback, one cannot simply view a binary file as they can with raw text files. The
original CSV will remain in place, but all bulk processing will be pulled from [Parquet][] or a high performance database
such as [ClickHouse][]. During these transformations is where [PyArrow][], [PySpark][] or [Spark][] will earn it's keep.

## Persistent Storage

A [PostgreSQL][] database server will be needed. There are many ways to perform this installation (local, remote,
[Dockerize PostgreSQL][], [PostgreSQL with Vagrant][], etc).

## High Performance Database

While [PostgreSQL][] is a highly-capabale RDMS, another database that is better suited to big data and extremely
fast queries called [ClickHouse][] will be used.

>It is column-oriented and allows to generate analytical reports using SQL queries in real-time. Blazingly fast,
> Linearly scalable, Feature rich, Hardware efficient, Fault-tolerant, Highly reliable
>
><cite>[ClickHouse Organization][]</cite>

## Distribution Tabs

In many of the installation sections, you will see Tabs for a particular distribution. Clicking on the 
desired tab will render the command or content relevant to that distribution.

>NOTE: These are just examples, and not intended for actual use.

=== "Alpine"
    - Update the package list
    ```bash
    apk update
    ```
    - Add a package
    ```bash
    apk add openssh
    apk add openssh opentp vim
    ```

=== "Arch"
    Example to install a prerequisite package for Kernel compiling.

    ```shell
    # Update the repositories
    pacman -Syu 

    # Install a package
    pacman -S dkms
    ```

=== "Ubuntu"
    Upgrade the host System Packages.

    ```shell
    # Run the following command
    sudo apt-get update && sudo apt-get upgrade
    ```

=== "Windows"
    Lets not and say we did!

    ```batch
    REM Run the following command
    echo Spark runs better on Linux.
    echo Please consider running Spark apps in
    echo VirtualBox if your host os is Windows!!
    ```

## Super Fencing

In many examples you may see multiple tabs relating to a particular code-block. Clicking on each
tab shows the syntax for the stated language. This is the same behaviour as with
[Distribution Tabs](#distribution-tabs)

=== "Golang"

    ``` go
    package main

    import (
        "fmt"
        "os"
        "os/exec"
        "strings"
        "time"

        flag "github.com/spf13/pflag"

        . "github.com/logrusorgru/aurora"
    )

    // version flags for main funciton
    var (
        appname     string
        version     string
        date        string
        description string = "Golang App to display time zone informaiton."
    )

    // CheckError is a function to print out errors
    func CheckError(e error) {
        if e != nil {
            fmt.Println(e)
        }
    }

    // clearScreen simple clears the terminal screen of any existing text
    func clearScreen() {
        c := exec.Command("clear")
        c.Stdout = os.Stdout
        c.Run()
    }

    // main is the primary entry point for the app
    func main() {

        //clearScreen()

        // set the option flagsd
        var ver = flag.BoolP("version", "v", false, "prints app version information")
        flag.Parse()

        // only print the version informaiton if the user asks for it.
        if *ver {
            fmt.Println("\nApp Name .....: ", Cyan(appname))
            fmt.Println("Version ......: ", Cyan(version))
            fmt.Println("Build Date ...: ", Cyan(date))
            fmt.Println("Description ..: ", Cyan(description))
            fmt.Println()
            os.Exit(0)
        }

        tNow := time.Now()

        fmt.Println(Cyan("\nCurrent Time Data In Local Time Zone"))
        fmt.Println(strings.Repeat("-", 55))

        // Local Time Now in Unix Timestamp format
        tUnix := tNow.Unix()
        fmt.Printf("Unix.Time:\t%d\n", tUnix)

        // Local Time Now serived from unix timestamp
        tLocal := time.Unix(tUnix, 0)
        fmt.Printf("Time.Local:\t%s\n", tLocal)

        // UTC Time serived from unix timestamp
        tUtc := time.Unix(tUnix, 0).UTC()
        fmt.Printf("Time.UTC:\t%s\n", tUtc)

        // Location Source: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        fmt.Println(Cyan("\nLocal Time For A Specific Zone"))
        fmt.Println(strings.Repeat("-", 58))

        eastern, e := time.LoadLocation("US/Eastern")
        CheckError(e)

        central, e := time.LoadLocation("US/Central")
        CheckError(e)

        mountain, e := time.LoadLocation("US/Mountain")
        CheckError(e)

        pacific, e := time.LoadLocation("US/Pacific")
        CheckError(e)

        alaska, e := time.LoadLocation("US/Alaska")
        CheckError(e)

        hawaii, e := time.LoadLocation("US/Hawaii")
        CheckError(e)

        fmt.Println("US/Eastern:\t", tNow.In(eastern))
        fmt.Println("US/Central:\t", tNow.In(central))
        fmt.Println("US/Mountain:\t", tNow.In(mountain))
        fmt.Println("US/Pacific:\t", tNow.In(pacific))
        fmt.Println("US/Alaska:\t", tNow.In(alaska))
        fmt.Println("US/Hawaii:\t", tNow.In(hawaii))
        /*
        Goloang Time Format Examples
        */
        fmt.Println(Cyan("\nGloang Time Package Format Examples"))
        fmt.Println(strings.Repeat("-", 55))
        fmt.Println("ANSIC:  \t", tNow.Format(time.ANSIC))
        fmt.Println("UnixDate:\t", tNow.Format(time.UnixDate))
        fmt.Println("RubyDate:\t", tNow.Format(time.RubyDate))
        fmt.Println("RFC822:  \t", tNow.Format(time.RFC822))
        fmt.Println("RFC822Z:  \t", tNow.Format(time.RFC822Z))
        fmt.Println("RFC850:  \t", tNow.Format(time.RFC850))
        fmt.Println("RFC1123:  \t", tNow.Format(time.RFC1123))
        fmt.Println("RFC1123Z:  \t", tNow.Format(time.RFC1123Z))
        fmt.Println("RFC3339:  \t", tNow.Format(time.RFC3339))
        fmt.Println("Kitchen:    \t", tNow.Format(time.Kitchen))
        fmt.Println("StampMicro:\t", tNow.Format(time.StampMicro))
        fmt.Println("StampMilli:\t", tNow.Format(time.StampMilli))
        fmt.Println("StampNano:\t", tNow.Format(time.StampNano))
        fmt.Println()
    }
    ```

=== "Java"

    ``` java
    /**
    *
    * Static Method: Unzip a file to a path location
    *
    */
    private static void UnzipFile(String zipFilePath, String destDir) {

        File dir = new File(destDir);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        FileInputStream fis;

        byte[] buffer = new byte[1024];
        try {
            
            fis = new FileInputStream(zipFilePath);
            ZipInputStream zis = new ZipInputStream(fis);
            ZipEntry ze = zis.getNextEntry();

            // outer-loop
            while (ze != null) {
                String fileName = ze.getName();
                File newFile = new File(destDir + File.separator + fileName);
                System.out.println("* Unzipping to " + newFile.getAbsolutePath());

                new File(newFile.getParent()).mkdirs();
                FileOutputStream fos = new FileOutputStream(newFile);
                int len;

                // inner-loop
                while ((len = zis.read(buffer)) > 0) {
                    fos.write(buffer, 0, len);
                }
                fos.close();

                //close this ZipEntry
                zis.closeEntry();
                ze = zis.getNextEntry();
            }

            // close the ZipEntry
            zis.closeEntry();
            zis.close();
            fis.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(2);
        }
    } // END - UnzipFile method
    ```

=== "Python"

    ``` python
    def pandas_convert_csv(csvfile):
        """Convert CSV file using parquet_type compression"""

        file_name = os.path.basename(csvfile)

        clear()
        print("\nPandas CSV Conversion Method")
        print(f"Parquet Compression Types : {parquet_types}")
        print("Sit back and relax, this takes a while!!\n")
        print(f'* Reading file  : {file_name}')
    
        start = time.time()
        df = pd.read_csv(csvfile, dtype=spot_dtype, names=column_names, header=None)
        rc = df.shape[0]
        print(f"* Spot Count    : {rc:,}")
        end = time.time()
        
        print(f"* File Size     : {round(get_file_size(csvfile, 'csv'), 2)} MB")
        print(f"* Elapsed Time  : {round((end - start), 3)} sec")

        for f in parquet_types:
            compression_type = str(f.upper())
            file_name = csvfile.replace('csv', f.lower())
            if compression_type == "PARQUET":
                comp_type = "NONE"
            else:
                comp_type = compression_type.upper()
            print(f'\n* Converting CSV to -> {f.lower()}')
            start = time.time()
            df.to_parquet(file_name, compression=str(comp_type.upper()))
            end = time.time()
            time.sleep(sleep_time) # prevent seg-fault on reads that are too quick

            print(f"* File Size     : {round(get_file_size(csvfile, comp_type), 2)} MB")
            print(f"* Elapsed Time  : {round((end - start), 3)} sec")
    ```

=== "Scala"

    ``` scala
    // Convert Epoch Times in from WSPRnet CSV files

    def main(args: Array[String]): Unit = {
        
        val debug: Boolean = false

        // make Java's log4j warnings be quiet
        PropertyConfigurator.configure("log4j/log4j.properties")

        // IMPORTANT: When converting EPOCH times, you must do so with the
        // to_utc_timestamp method. This requires telling the system what Zone
        // your computer is in (the one doing the conversion) in order to get
        // the correct unix time.
        val z = ZoneId.systemDefault()
        val zoneId = z.getId

        println("Process Steps For Processing A CSV File")
        println("- Create a Spark Session")

        // Create the SPark Session
        val spark: SparkSession = SparkSession.builder()
          .appName("Read CSV and Show Schema")
          .master("local[16]")
          .getOrCreate()

        // Add Type-Safe Schema
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

        // Create the Spark DataSet ( using small 100K csv )
        println("- Read the CSV file into a DataSet")
        import spark.implicits._
        val ds = spark.read
          .option("delimiter", ",")
          .option("header", "false")
          .schema(spotSchema)
          .csv(path = "data/spots-2020-02-100K.csv")
          .as[RawSpot]
        
        println("- Select the column we want to process")

        // Filter the data set 
        val res = ds.select("*")
          .withColumn("x_TimeStamp", date_format(col("TimeStamp")
          .cast(DataTypes.TimestampType), "yyyy-MM-dd HH:mm:ss"))

        // only print the schema in Debug Mode
        if (debug) {
            res.printSchema()
        }

        // See note above about ZoneId, it's important!
        println("- Setup Epoh Conversion")
        val res1 = res.select("*")
          .withColumn("x_timestamp", to_utc_timestamp(col("x_TimeStamp"), zoneId))
          .withColumn("x_date", to_date(col("x_TimeStamp")))
          .withColumn("x_year", year(col("x_TimeStamp")).cast(ShortType))
          .withColumn("x_month", month(col("x_TimeStamp")).cast(ByteType))
          .withColumn("x_day", dayofmonth(col("x_TimeStamp")).cast(ByteType))
          .withColumn("x_hour", hour(col("x_TimeStamp")).cast(ByteType))
          .withColumn("x_minute", minute(col("x_TimeStamp")).cast(ByteType))

        // only print the schema in Debug Mode
        if (debug) {
            println("- Print Res1 Schema")
            res1.printSchema()
        }

        // When we call show(x), this is what triggers the run
        println("- Execute the Query")
        time {
            res1.show(5)
        }

        // Print the final row count
        println("\nGetting final row count, please wait...")
        time {
            val rowcount = res1.count()
            println(f"Epoch Conversion Processed : ($rowcount%,d) Spots ")
        }
    } // END - Main CLass
    ```

<div>
    <p align="center"><i>WSPR Analytics is <a href="https://github.com/KI7MT/wspr-analytics/blob/master/LICENSE.md">Apache 2.0 licensed</a> code.</i></p>
</div>

[Arch Linux]: https://archlinux.org/
[Alpine]: https://www.alpinelinux.org/
[ClickHouse]: https://clickhouse.tech/
[ClickHouse Organization]: https://clickhouse.tech/

[WSPR Spots]: http://www.wsprnet.org/drupal/wsprnet/activity
[WSPRnet]: http://www.wsprnet.org
[WSPR]: https://www.physics.princeton.edu/pulsar/k1jt/wspr.html
[Big Data]: https://www.oracle.com/big-data/what-is-big-data.html
[Amazon AWS EBR]: https://aws.amazon.com/emr/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc
[Microsoft Cloud Analytics]: https://azure.microsoft.com/en-us/solutions/big-data/#products
[Google Smart Analytics]: https://cloud.google.com/solutions/smart-analytics/
[Apache Spark]: https://spark.apache.org/PySpark
[PySpark]: https://databricks.com/glossary/pyspark
[Anaconda Python]: https://www.anaconda.com/
[Scala]: https://docs.scala-lang.org
[Open Source Tools]: https://apache.org/index.html#projects-list
[AWS]: https://aws.amazon.com/
[Azure]: https://azure.microsoft.com/en-us/
[GCP]: https://cloud.google.com/
[Apache Hadoop]: http://hadoop.apache.org/
[Jupyter Notebooks]: https://jupyter.org/
[IntelliJ IDEA]: https://www.jetbrains.com/idea/
[Dockerize PostgreSQL]: https://docs.docker.com/engine/examples/postgresql_service/
[PostgreSQL]: https://www.postgresql.org/
[PostgreSQL with Vagrant]: https://wiki.postgresql.org/wiki/PostgreSQL_For_Development_With_Vagrant
[Parquet]: https://parquet.apache.org/
[Flask-Pandas-App]: https://github.com/the-akira/Flask-Pandas-App
[Full Stack Flask]: https://www.fullstackpython.com
[WSPRNet Archives]: http://www.wsprnet.org/drupal/downloads
[Anaconda Python]: https://www.anaconda.com/
[sdkman]: https://sdkman.io/
[PyArrow]: https://towardsdatascience.com/distributed-processing-with-pyarrow-powered-new-pandas-udfs-in-pyspark-3-0-8f1fe4c15208
[Apache Foundation Project List]: https://apache.org/index.html#projects-list
[WSPR Analytics Docs]: https://ki7mt.github.io/wspr-analytics/
[Ubuntu-20.04]: http://www.releases.ubuntu.com/20.04/
[WSPR Daemon]: http://wsprdaemon.org/
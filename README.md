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

# Setup and Installation

The setup section in the [documentation below](#documentation) below will walk users through everything
they need to setup their system for big data processing. The guide has been well tested on three
different Linux distributions, namely: [Ubuntu-20.04][], [Arch Linux][], and [Alpine][].

For newer Linux users, I'd highly recommend [Ubuntu-20.04][], as Arch and Alpine can be difficult
if you are not accustom to their installation methiods.

## Documentation

Each folder will contain a series of `README` files that explain the content, and where warrented,
usage. Additionally, project documentation website can be used for more extensive and exhaustinve 
explination of the project and its contence.

* [WSPR Analytics Docs][] - bookmark this location for future reference

## Folder Descriptions

Several frameworks are used in this repository. The following matrix provides a short description
of each, and their intended purpose.

Folder       | Frameworks          | Description
|:---        |:---                 |:---
|docs        | Python, MkDocs      | General repository documentation
|golang      | Golang              | General purpose command line apps and utilities
|java        | Java, Maven, SBT    | Java apps for RDD and Avro examples
|notebooks   | Jupyter Notebooks   | Notebooks for basic test and visualization
|pyspark     | Python, PyArrow     | Scripts that interact with CSV and Parquet files
|spark       | Scala               | Scala programs to perform ETL tasks
|wsprdaemon  | Python, Scala, Psql | Utilities related to the WSPR Daemon project
|wsprana     | Python              | (soon to be retired)

## Base Tool Requirements

You must have Python, Java, PySpark/Spark available from the command line.

- Java openjdk version 1.8.0_275 or later
- Python 3.7 oir 3.8, PyArrow hsa some issues with 3.9
- PySpark from PyPi
- Apache Arrow 2.0+
- Scala 2.12.12
- Spark 3.0.1
- PostgreSQL Database (local, remote, Docker, etc)

>IMPORTANT: The Spark / Scala combinations are version sensitive. Check the [Spark][]
download page for recommended version combinaitons if you deviate from what is listed here.
As of this writing, Spark 3.0.1 and above was built with Scala 2.12.10. For the least
amount of frustration, stick with what's known to work (any of the 2.12.xx series)

## Data Sources and Processing

The main data source will be the monthly [WSPRNet Archives][]. At present, there is no plan to pull
nightly updates. That could change if a reasonble API is identified.

The tools (apps/scripts) will be used to convert the raw CSV files into a format better suited for parallel processing,
namely, [Parquet][]. Read speeds, storage footprints, and ingestion improve dramativaly with this storage format.
However, there is a drawback, one cannot simply view a binary file as they can with raw text files. The
original CSV will remain in place, but all bulk processing will be pulled from [Parquet][] or a high performance dataabase
such as [ClickHouse][]. During these transformations is where [PyArrow][], [PySpark][] or [Spark][] will earn it's keep.

## Persistant Storage

A [PostgreSQL][] database server will be needed. There are many ways to perform this installation (local, remote,
[Dockerize PostgreSQL][], [PostgreSQL with Vagrant][], etc).

## High Performance Database

While [PostgreSQL][] is a highly-capabale RDMS, another database that is better suited to big data and extremely
fast queries called [ClickHouse][] will be used.

>It is column-oriented and allows to generate analytical reports using SQL queries in real-time.
> - Blazingly fast
> - Linearly scalable
> - Feature rich
> - Hardware efficient
> - Fault-tolerant
> - Highly reliable
>
> <cite>[ClickHouse Orginization][]</cite>
>

[Arch Linux]: https://archlinux.org/
[Alpine]: https://www.alpinelinux.org/
[ClickHouse]: https://clickhouse.tech/
[ClickHouse Orginization]: https://clickhouse.tech/
[WSPR Spots]: http://www.wsprnet.org/drupal/wsprnet/activity
[WSPRnet]: http://www.wsprnet.org
[WSPR]: https://www.physics.princeton.edu/pulsar/k1jt/wspr.html
[Big Data]: https://www.oracle.com/big-data/what-is-big-data.html
[Amazon AWS EBR]: https://aws.amazon.com/emr/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc
[Microsoft Cloud Analytics]: https://azure.microsoft.com/en-us/solutions/big-data/#products
[Google Smart Analytics]: https://cloud.google.com/solutions/smart-analytics/
[Apache Spark]: https://spark.apache.org/PySpark
[Spark]: https://spark.apache.org/downloads.html
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
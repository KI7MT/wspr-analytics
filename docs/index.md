# WSPR Analytics

In the early days (March 2008), [WSPR Spots][] measured in the hundreds of thousands per month. Today,
that number has increased to over 75+ Million per month and shows no sign of abatement.
By any reasonable definition, it is safe to say that [WSPR][] has entered the realm of [Big Data][].

## Project Goal

The goal of this project is to provide a set of tools to download, manage, transform and query
WSPR DataSets using modern [Big Data][] frameworks.

## Folder Descriptions

Several frameworks are used in this repository. The following matrix provides a short description
of each, and their intended purpose.

* `docs` - Python, MkDocs for repository documentation
* `java` - Java, Maven, and SBT apps for RDD and Avro examples
* `notebooks` - Jupyter Notebooks  for basic test and visualization
* `pyspark` - Python, PyArrow scripts that interact with CSV and Parquet files
* `spark` -Scala programs to perform tasks
* `wsprdaemon` - Python, Scala, Psql utilities related to the WSPR Daemon project
* `wsprana` - Python, (soon to be retired)


Pay close attention to the `README` files as they lay out how to setup the
tools needed to run their respective scripts or application.

## Basic Tool Requirements

>NOTE: During development, the wsprana package **is not** intended for pip installaiton
>yet, but will be.It should be checked out and run from source at present.

You must have Python, Java, PySpark/Spark available from the command line.

- Java openjdk version 1.8.0_275 or later
- Python 3.7+
- PySpark from PyPi
- Apache Arrow 2.0+
- Scala 2.12+
- Spark 3.0.1
- PostgreSQL Database (local, remote, Docker, etc)

An easy way (on Linux / MacOS) to manage Java, Spark, Scala and SBT is
through an management tool called [sdkman][]. This tool allows
one to install virtually any combination of tools you need without
affecting your root file system. With the exception of Python,
All the above requirements can be installed and managed via [sdkman][].

For Python, the recomendation is to use [Anaconda Python][], the full version,
as it provides all the analytics tooling you'll need for this project and more.

## Data Sources and Processing

The primary data source will be the monthly [WSPRNet Archives][]. At present, there is no plan to pull
nightly updates. That could change if a reasonble API is identified.

The WSPR CSV tools will be used to convert the raw CSV files into a format better suited for parallel processing,
namely, [Parquet][]. Read speeds, storage footprints, and ingestion improve dramativaly with this storage format.
However, there is a drawback, one cannot simply view a binary file as they can with raw text files. The
original CSV will remain in place, but all bulk processing will be pulled from [Parquet][].
During these transformations is where [PyArrow][] + [PySpark][] will earn it's keep.

## Persistant Storage

A [PostgreSQL][] database server will be needed. There are many ways to perform this installation (local, remote,
[Dockerize PostgreSQL][], [PostgreSQL with Vagrant][], etc). Whichever method you chose, it will be used extensively
by many of the apps and scripts.

<p align="center"><i>WSPR Analytics is <a href="https://github.com/KI7MT/wspr-analytics/blob/master/LICENSE.md">Apache 2.0 licensed</a> code.</i></p>

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
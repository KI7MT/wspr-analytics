# WSPR Analytics Using Scala

In the early days (March 2008), [WSPR Spots][] measured in the hundreds of thousands per month. Today,
that number has increased to over 46 Million per month at last count, and shows no sign of abatment.
By any reasonable definition, it is safe to say, [WSPR] has entered the realm of [Big Data][].

With this entry comes a unique set of challanges to draw meaningful results in a timely manner.
The `WSPR Analytics` project will contain a seris of documents, small modules, example
applications, code snippets and various utilities centerd around [Apache Spark][], [Apache Hadoop][],
[Jupyter Notebooks][], [Scala][] and other [Big Data][] tooling to help with this challange.

## Basic Tool and Build Instructions

In each folder under `src`, you'll find instructions for compiling and running each
project or script as appropriate.

You must have Python, Java, Scala, Spark and SBT available from the command line.

- Java openjdk version 1.8.0_275 or later
- Scala Version 2.12.12
- Spark 3.0.1
- SBT Tools 1.4.5
- Python 3.7+

An easy way (on Linux / MacOS) to mange Java, Spark, Scala and SBT is
through an management tool called [sdkman][]. This tool allows
one to install virtually any combination of tools you need without
affecting your root file system. With the exception of Python,
All the above requirements can be installed and managed via [sdkman][].

For Python, the recomendation is to use [Anaconda Python][], the full version,
as it provides all the analytics tooling you'll need for this project and more.

## Visualization

The presentation layer very much depends on the users needs. One may be writing a paper and only needs specific
data blocks presented in [Jupyter Notebooks][] while others are generating data for use with a [Full Stack Flask][] app.
No matter the case, examples will be provided to show how this can eaily be achived with the language framework
we've chosen to use. See this example ([Flask-Pandas-App][]) to illistrate the point resepctive to Data Science.

## Sample Applications

The following is a list of sample applications that can be performed on the various
[WSPR Spots][] CSV Files. As new script are written, then will appear in the list below.

- [Top Ten Reporters][]

[WSPR Spots]: http://www.wsprnet.org/drupal/wsprnet/activity
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


[Top Ten Reporters]: https://github.com/KI7MT/wsprana-spark-scala/tree/main/scala/TopTenReporters

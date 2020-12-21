# WSPR Analytics

`Big Data Analytics on a small budget is the focus of this project.` 


In the early days (March 2008), [WSPR Spots][] measured in the hundreds of thousands per month. Today,
that number has increased to nearly 46 Million, and shows no sign of abatment.
By any reasonable definition, it is safe to say, [WSPR] has entered the realm of [Big Data][].

With this entry comes a unique set of challanges to draw meaningful results in a timely manner.
The `WSPR Analytics` project will contain a seris of documents, small modules, example
applications, code snippets and various utilities centerd around [Apache Spark][], [Apache Hadoop][],
[PySpark][], [PyArrow][], [Anaconda Python][], [Jupyter Notebooks][], [Scala][] and other [Big Data][] tooling to
help with this challange.

## Abstract Implementation

This peoject will focus on `Scaling Up`, not so much `Scaling Out`, using comodity based
hardware. [Big Data][] tooling from vendors such as [Amazon AWS EBR][], [Microsoft Cloud Analytics][],
[Google Smart Analytics][] provide a litany of options for processing [Big Data][]. However, for most of us, the
return on invenst just isn't there.

The same [Open Source Tools][] used in the pay-to-play areana can be employed on a much smaller scale
(home server, work station, laptop, VMWare / VirtualBox Nodes, or SBC's like the Raspbery Pi) and used to process
datasets in a much more effecient manner than mere parsing of CSV files. The trade off is a bit more 
processing time compared to the thousands of dollars one could spend spining up compute clusters with 
cloud based providers.

Commodity based hardware, for the most part, will be the focus of this project. That is not to say, [AWS],
[Azure], [GCP] examples won't be provided in time, they just won't be the main focus initially.

## Scope of Work

While there may be some `installable` packages, where warrented, the majority of activity will take place
in [Jupyter Notebooks][], [IntelliJ IDEA][], running scripts or compiled applications from the command line.
There will be no overarching application that performs all tasks, rather, a colletion of scripts and smaller
apps one can choose to use if desired.

## Cross Platform Compatability

The majority of the tools that will be used can run on Windows, Linux, or MacOS. Windows, as always,
presents a unique set of challanges, but will not left out of the mix.


## Data Sources and Processing

The primary data source will be the monthly [WSPRNet Archives][]. At present, there is no plan to pull
nightly updates but that could change of a reasonble implementation can be identified.

The WSPR CSV tools will be used to convert the raw CSV files into a format better suited for parallel processing,
namely, [Parquet][]. Read speeds, storage footprints, and ingestion improve dramativaly with this storage formate.
However, there is a drawback, one cannot simply view a binary file format as they can with raw text files. The
original CSV will remain in place, but all processing that's done on a large scale will be pulled from [Parquet][].
During these transformations is where [PyArrow][] will earn it's keep.

A [PostgreSQL] data base server will be beeded. There are many ways to perform this installation (local, remote,
[Dockerize PostgreSQL][], [PostgreSQL with Vagrant][], etc). Whichever method you chose, it will be used extensively through many of the apps and scripts.

## Presentation

The presentation layer very much depends on the users needs. One may be writing a paper and only need specific
data blocks presented in [Jupyter Notebooks][] while others are generating data for use with a [Full Stack Flask][] app. No matter the case, examples will be provided to show how this can eaily be achived with the language framework we've chosen to use. See this example ([Flask-Pandas-App][]) to illistrate the point resepctive to Data Science.

## Documentation

Documentation will be provided for basic environment and tooling setup, but there will not be a fully automated
install process. Users will need to invest some time in learing the basics of the tools used in order to make the
most of what they can do.

At this time, the documentation sight is under development. When the basic framweork is complete, including tool setup, it will be published to Github Pages as a static website.

Each section in the `src` folder will have a `README` that convers basic usage, and if needed, compling instructions. User are encouraged to read these files before attemmpting to run the app/script. In most cases, some level of configuration will be needed, if for no other reason that to identify the data-source location.

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
[PostgreSQL with Vagrant]: https://wiki.postgresql.org/wiki/PostgreSQL_For_Development_With_Vagrant
[Parquet]: https://parquet.apache.org/
[Flask-Pandas-App]: https://github.com/the-akira/Flask-Pandas-App
[Full Stack Flask]: https://www.fullstackpython.com
[PyArrow]: https://towardsdatascience.com/distributed-processing-with-pyarrow-powered-new-pandas-udfs-in-pyspark-3-0-8f1fe4c15208
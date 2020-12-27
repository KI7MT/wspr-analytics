# Performance Experiments

The scripts in this directory are used for exploring the use of [Spark][], [Apache Arrow][],
[Scala][] and other Big Data frameworks to: 

1. Reduce WSPR CSV on-disk storage space
1. Improve CSV read times and portability
1. Improve query performance
1. Produce a cost effective, yet scalable, analytics solution for WSPR data

An additional dimension that could be explored is streaming. For those with
suffecient energy, there are many frameworks that can be employed in this
area:

* [Apache Storm][]
* [Spark Streaming][]
* [Apache Flink][]

...and many others.

All of the example scripts will be incorporated into a main application at some point,
however, some will just be for testing.

Additional tests will be done using [Scala][] and / or [Java][] for performance
cvomparison. Initial tests will be run using Python, or more sustinct, [PySpark][],
as it lends itself to rapid-deployment scenarios.

>NOTE: This exercise is not a full-blown scientific experiment. Rather, its more
>of a feasability or proof of concept exercise.

## Compute Constraints

While there is no shortage of cloud-based Big Data solutions these days ( 
[AWS EMR][], [Azure Synapse][], [Databricks][], [GCP][], [Google Big Query][], etc),
these tests will look at commonidty based on-prem resources in order to keep
the overall cost to an acceptable level. In other words: a hefty workstation,
a stack of Raspberry PI's, or an over-powered laptop should be capable of
performing the tasks for the use case at hand.

## Compute Environment

If you are on `Windows 10`, I would highly recommended using `Windows Subsystem Linux v2`.
Doing so will make setting up [Apache Spark][] much easier, and you can follow
the directions below with mininal frustration.

### Java

No matter which method of compute is employed, [Java][] forms the foundation.
I chose to use `openjdk version 1.8.0_275`, however, [Spark][] now fully
supports `Java-11`. I've also ran `Java-14`, but prefer to stick with LTS
versions becasue not all frameworks support the `"latest and greatest"` JVM.

### Python

You need a `Python` environment, either from [Anaconda Python][] or the standard
[Python][] installer and `venv`. Either way, you should run the tests in a virtual
Python environment to keep these packages from interfering with your core
operating system.

### SDK Manager

While running tests, it can be frustraighting to manage the large matrix of
frameworks. The use of [sdkman][] can make quick work of this chore; it's up to
you though.

## Running The Tests

The first two tests will illustrate the speed increase by using [Apache Arrow][]
to process both CSV and [Apache Parquet][] compressed binaries. The major difference
between the native CSV file, and those compressed by the `pandas_convert_csv.py`
script is, the CSV file has no schema header information accompanying the file
whereas the [Apache Parquet][] binaries have full headers and data-type structures
defined. Using inferred-schema does work, but it is not without error.
This is the primary reason to fully define the schemas beforehand.

[Pandas][], buy default, is a single thread reader/writer. It can be made to
pool, but it's not configured to do so out of the box. You will see the
difference in reading raw CSV files during the compression
run and that of [Apache Arrow][] (e.g. PyArrow with Python) running in parallel
doing the same task.

To run the test scripts, perform the following:

- Download and extract a WSPR Archive
- Clone the [wspr-analytics][] repository
- Set a path variable
- Install Python package requirments
- Runs the test scripts

Here are the `Bash` commands I used to run the tests.

```bash
# change the download location to whatever you prefer
cd ~/Downloads
wget -c http://wsprnet.org/archive/wsprspots-2020-02.csv.gz
gzip -dk wsprspots-2020-02.csv.gz

# set the path of the downloaded and extracted CSV file
csvfile=$PWD/wsprspots-2020-02.csv

# clone the repo
git clone https://github.com/KI7MT/wspr-analytics.git

# change directories and install dependencies
cd ~/Downloads/wspr-analytics/experiments

# NOTE: Be sure you are in a virtual environment "before"
# installing Python packages
python -m pip install -r requirement.txt

# run the conversion script
python pandas_convert_csv.py -f $csvfile
```

### Pandas Parquet Compression Test

* `CSV Reader` - Python Pandas
* `Parquet Writer` - Python Pandas To Parquet

>NOTE: Additional tests will be added to check the read/write
>speeds using [Apache Arrow][] only while leaving [Pandas][]
>out of the mix completely.

The following data shows the results of converting a CSV file to 
several [Apache Parquet][] formats. Substantial disk-space
savings can be achived using these methods.

Generally speaking, as the compression increases so does the length
of time it takes to create the file. However, the disk-space savings
are impressive.

>NOTE : Make note of the CSV Read Time while using [Pandas] in a `Single Thead` 

Disk space savings range from `>= 5 : 1` to `8 : 1` depending on the compression
you'd like to use. It's a `substantial` savings no matter which you chose.

```bash
Pandas CSV Conversion Method
Parquet Compression Types : ['SNAPPY', 'LZ4', 'ZSTD', 'GZIP', 'BROTLI']
Sit back and relax, this takes a while!!

* Reading file  : wsprspots-2020-02.csv
* Spot Count    : 47,310,649
* File Size     : 3780.94 MB
* Elapsed Time  : 79.448 sec

* Converting CSV to -> snappy
* File Size     : 667.07 MB
* Elapsed Time  : 29.579 sec

* Converting CSV to -> lz4
* File Size     : 627.88 MB
* Elapsed Time  : 29.702 sec

* Converting CSV to -> zstd
* File Size     : 520.19 MB
* Elapsed Time  : 30.778 sec

* Converting CSV to -> gzip
* File Size     : 467.55 MB
* Elapsed Time  : 107.244 sec

* Converting CSV to -> brotli
* File Size     : 446.58 MB
* Elapsed Time  : 89.529 sec

NOTE : The File Sizes Are Approximated = (file bytes / 1048576)

Finished !!
```

### PyArrow Read Test

* `Reader` - PyArrow

The results below are from using [Apache Arrow][] to read each of the
compressed-file formats created above.

No Spark nodes are deployed, only a single master with no special
optimizations applied. [Apache Arrow][] uses threads by default which
is the main difference in using [Pandas][] to read original CSV read.

To say it's fast is an understatement.

> NOTE : Check the CSV Read Time below and compare it to the [Pandas][]
> CSV read time from above; it's an `36 : 1` read-speed improvement or
> ( `80.32 sec` v.s. `2.213 sec` )

```bash
# You run the read script the same way
python pyarrow_read.py -f $csvfile

# Results:

Running Read Tests Using Apache Arrow
Compression Types : ['CSV', 'SNAPPY', 'ZSTD', 'GZIP', 'BROTLI']

* Reading file  : wsprspots-2020-02.csv
* File Size     : 3780.94 MB
* Elapsed Time  : 2.185

* Reading file  : wsprspots-2020-02.snappy
* File Size     : 667.07 MB
* Elapsed Time  : 2.011

* Reading file  : wsprspots-2020-02.zstd
* File Size     : 520.19 MB
* Elapsed Time  : 1.769

* Reading file  : wsprspots-2020-02.gzip
* File Size     : 467.55 MB
* Elapsed Time  : 3.654

* Reading file  : wsprspots-2020-02.brotli
* File Size     : 446.58 MB
* Elapsed Time  : 2.102

 Finished !!
```

# Query Parquet File Using PySpark

The next phase is to run a simple query using [PySpark][] in  
in a distributed manner.

As this is all happening on a single msater host node, it is more
of a parralized action rather than distributed, but the results are
far superior to what any single threaded implementation could achieve.

See [WSPR Query Notebook][] for details.

The read speed is impressive. It takes `~1.5` seccond to read
`47+ Million` rows, and `~4.8` seconds to do a group by query.

Row count speeds (  `0.87 sec` ) are on par with using ( `wc -l` )
from a Linux shell.

Now matter how one looks at this approach, it's a viable alternative
to a raw csv read and process action.

```bash
* Reading file ..: wsprspots-2020-02.parquet
* File Size .....: 490,259,730 bytes compressed
* Read Time .....: 1.51834 sec

* Counting Records
* Record Count ..: 47,310,649
* Count Time ....: 0.90268 sec

* Running Group by Count Query and return the dataframe
+--------+------+
|Reporter| count|
+--------+------+
|   DK6UG|838081|
|  OE9GHV|690104|
|  EA8BFK|648670|
|   KD2OM|589003|
|KA7OEI-1|576788|
|   K4RCG|571445|
|     KPH|551690|
|    K9AN|480759|
|   DF5FH|480352|
|   DJ9PC|474211|
+--------+------+
only showing top 10 rows

* Query Time ....: 4.94034 sec
```

[PySpark]: https://databricks.com/glossary/pyspark
[wsprana]: https://github.com/KI7MT/wsprana-spark-python
[Apache Spark]: https://spark.apache.org/PySpark
[Anaconda Python]: https://www.anaconda.com/
[Python]: https://www.python.org
[Pandas]: https://pandas.pydata.org/
[Apache Parquet]: https://parquet.apache.org/
[wsprana repository]: https://github.com/KI7MT/wsprana-spark-python
[Spark and Scala]: https://github.com/KI7MT/wsprana-spark-scala
[wsprspots-2020-02.csv.gz]: http://wsprnet.org/archive/wsprspots-2020-02.csv.gz
[Apache Arrow]: https://arrow.apache.org/
[Scala]: https://www.scala-lang.org/
[WSPR Query Notebook]: https://github.com/KI7MT/wspr-analytics/blob/main/notebooks/WSPR-Query-Using-PySpark.ipynb
[sdkman]: https://sdkman.io/
[AWS EEMR]: https://aws.amazon.com/emr/features/spark/
[Azure Synapse]: https://azure.microsoft.com/en-us/services/synapse-analytics/
[Databricks]: https://databricks.com/
[GCP]: https://cloud.google.com/compute/
[Google Big Query]: https://cloud.google.com/bigquery/
[Apache Storm]: https://storm.apache.org/
[Spark Streaming]: https://spark.apache.org/streaming/
[Apache Flink]: https://flink.apache.org/
[Spark]: https://spark.apache.org/
[Java]: https://adoptopenjdk.net/
[wspr-analytics]: https://github.com/KI7MT/wspr-analytics
[PyArrow]:
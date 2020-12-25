>Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in Java,
>Scala, Python and R, and an optimized engine that supports general execution graphs. It also supports a rich set
>of higher-level tools including Spark SQL for SQL and structured data processing, MLlib for machine learning,
>GraphX for graph processing, and Structured Streaming for incremental computation and stream processing.
>
> -- <cite>[Apache Spark Project](https://spark.apache.org/)</cite>

Apache Spark is written in a programming language called [Scala][], which runs on a [Java Virtual Machine][]
(JVM). To allow for an easy  integration between [Scala][] and Python, the programming community created a tool set
(libraries/modules/scripts) called [PySpark][]. Other languages such as Ruby, R, and Java also have bindings
that support or work with the [Spark][] framework.

It can get a bit confusing trying to distinguish the manay moving parts of the [Spark][] echosystem. To
make it a bit easier, just remember [Spark][] is the foundation, and [PySpark][] in merely an integration
to that foundation.

For the purposes of the [WSPR Analytics][] project, we'll being using [PySpark][] as a easy gateway to
[Jupyter Notebooks][] in a distributive manner. As with [Spark][], [PySpark][] has it's own shell
when not being forwarded to [Jupyter Notebooks][]. However, both still rely on [Spark][] as the compute
engine, and in this case, [Python][] is the interface via the command-line rather than web page.

You can see by the shell below, I was running Anaconda Python v3.7.9 from with Spark v3.0.1. You can
also see that the `pyspark` shell creates a `SparkContext` for us upon entry. This will be better
understood when executng example scripts.

```shell
Python 3.7.9 (default, Aug 31 2020, 12:42:55) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.0.1
      /_/

Using Python version 3.7.9 (default, Aug 31 2020 12:42:55)
SparkSession available as 'spark'.

>>> spark.version
'3.0.1'

>>> sc.version
'3.0.1'
```

## Additional Resources

There are many high-quailty sites that cover all aspects of [PySpark][] in great detail:

* [Databricks] - The original creator of [Spark][]
* [Learning Spark 2nd Edition][], also from Databricks, is a great book
* [PySpark Docs][] covers SQL, ML, Streaming and more
* [Spark][] itself from the Apache Foundation
* [PySpark at JavaPoint][] is a great resource for all things coding

[Scala]: https://scala-lang.org/
[PySpark]: https://spark.apache.org/docs/latest/api/python/index.html
[Spark]: https://spark.apache.org/
[Jupyter Notebooks]: https://jupyter.org/
[WSPR Analytics]: https://github.com/KI7MT/wspr-analytics
[Python]: https://www.anaconda.com/
[Java VIrtual Machine]: https://www.w3schools.in/java-tutorial/java-virtual-machine/
[Databricks]: https://databricks.com/glossary/pyspark
[Learning Spark 2nd Edition]: https://tinyurl.com/y7ngpjff
[PySpark Docs]: https://spark.apache.org/docs/latest/api/python/index.html
[PySpark at JavaPoint]: https://www.javatpoint.com/pyspark
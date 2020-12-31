>Scala combines object-oriented and functional programming in one concise,
>high-level language. Scala's static types help avoid bugs in complex applications,
>and its JVM and JavaScript runtimes let you build high-performance systems with
>easy access to huge ecosystems of libraries.
>
><cite>[The Scala Project][]</cite>

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

If you can't run run, type: `scala` and have it present the REPL,
see [Installing Scalla](setup/install-scala/)

>NOTE: You're version of Java and Scala may be different.

```scala

(wsprana) ki7mt@3950X:~ $ scala
Welcome to Scala 2.12.12 (OpenJDK 64-Bit Server VM, Java 1.8.0_275).
Type in expressions for evaluation. Or try :help.

scala> val nums = Seq(1,2,3)
nums: Seq[Int] = List(1, 2, 3)

scala> val doubledNums = for (n <- nums) yield n * 2
doubledNums: Seq[Int] = List(2, 4, 6)

```

[The Scala Project]: https://scala-lang.org/
[Scala Projects]: https://scala-lang.org/
[sdkman]: https://sdkman.io/
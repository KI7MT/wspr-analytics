version := "1.0"

name := "TopTenReciever"

scalaVersion := "2.12.12"

libraryDependencies ++= Seq(
    "org.apache.spark" %% "spark-core" % "3.0.1" % "provided",
    "org.apache.spark" %% "spark-sql" % "3.0.1" % "provided"
)

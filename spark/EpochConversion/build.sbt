name          := "EpochConversion"
version       := "1.0"
scalaVersion  := "2.12.12"
organization  := "io.ki7mt"


libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.0.1",
  "org.apache.spark" %% "spark-sql" % "3.0.1",
  "org.apache.spark" %% "spark-mllib" % "3.0.1",
  "org.apache.spark" %% "spark-streaming" % "3.0.1",
  "commons-io" % "commons-io" % "2.8.0"
)

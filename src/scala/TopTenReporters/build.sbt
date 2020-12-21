organization := "com.ki7mt.wsprana.scala"

version := "1.0"

name := "TopTenReporter"

scalaVersion := "2.12.12"

val sparkVersion = "3.0.1"

libraryDependencies ++= Seq(
    "org.apache.spark" %% "spark-core" % "3.0.1" % "provided",
    "org.apache.spark" %% "spark-sql" % "3.0.1" % "provided"
)

// Note: This is for a thin jar only, not the fat jar
// custom package name: name_<scala-version>-<spark-version>-<module-version>.jar
// Example: top-ten-receiver_2.12-3.0.1-1.0.jar
artifactName := { (sv: ScalaVersion, module: ModuleID, artifact: Artifact) =>
  Artifact.artifactName(sv, module, artifact).replaceAll(s"-${module.revision}", s"-${sparkVersion}-${module.revision}")
}

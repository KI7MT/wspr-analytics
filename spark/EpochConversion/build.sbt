name          := "EpochConversion"
version       := "1.0"
scalaVersion  := "2.12.13"
organization  := "com.ki7mt"

val sparkVersion = "3.1.1"

libraryDependencies ++= Seq(
    "org.apache.spark" %% "spark-core" % "3.0.1" % "provided",
    "org.apache.spark" %% "spark-sql" % "3.0.1" % "provided"
)

artifactName := { (sv: ScalaVersion, module: ModuleID, artifact: Artifact) =>
  Artifact.artifactName(sv, module, artifact).replaceAll(s"-${module.revision}", s"-${sparkVersion}-${module.revision}")
}

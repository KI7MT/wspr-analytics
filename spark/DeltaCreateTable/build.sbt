name          := "DeltaCreateTable"
version       := "1.0"
organization  := "io.ki7mt"
scalaVersion  := "2.12.13"

val sparkVersion = "3.0.1"

// compiler options for cleaner code
scalacOptions ++= Seq(
  "-encoding", "utf8",              // Allow option and arguments on same line
  "-deprecation",                   // emit warning and location for usages of deprecated APIs
  "-feature",                       // emit warning and location for usages of features that should be imported explicitly
  "-unchecked",                     // enable additional warnings where generated code depends on assumptions
  "-Xfatal-warnings",               // fail the compilation if there are any warnings
  "-Xmigration",                    // warn about constructs whose behavior may have changed since version
  "-language:implicitConversions",  // Allow definition of implicit functions called views
  "-language:higherKinds",          // Allow higher-kinded types
  "-language:existentials"          // Existential types (besides wildcard types) can be written and inferred      
)

libraryDependencies ++= Seq(
    "org.apache.spark" %% "spark-core" % "3.0.1" % "provided",
    "org.apache.spark" %% "spark-sql" % "3.0.1" % "provided",
    "io.delta" %% "delta-core" % "0.8.0",
)

artifactName := { (sv: ScalaVersion, module: ModuleID, artifact: Artifact) =>
  Artifact.artifactName(sv, module, artifact).replaceAll(s"-${module.revision}", s"-${sparkVersion}-${module.revision}")
}

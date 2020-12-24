# Java Examples

This folder holds a basic Java App used to download WSPR CSV files.

The primary use for Java in this project will be dealing with Avro
files formats and schemas.

At present, all this app does is download a CSV from [WSPRNet][]
You can change what file is pulls by editing the script itself.
In the future, this may be converted to a command line optins
format, but for now it's manual.

```java
// package com.ki7mt.spark.utils;
// Class: DownloadArchive.java

// Edit the following:
// Adjust Year and Month only

    public static void main(String[] args) {

        // Change the year and two digit month to download
        String year = "2008";
        String month = "03";

        /* -- NO FURTHER EDITS NEEDED BELOW THIS LINE -- */

        // Process variables
        String fileName;
        fileName = "wsprspots-" + year + "-" + month + ".csv.zip";
        String inFileUrl = "http://wsprnet.org/archive/" + fileName;
        String outFile = "data/csv/" + fileName;
        String outFileDir = "data/csv";
```

After settin the year and month you want, just right click and run
it from your IDE.

[WSPRNet]: http://www.wsprnet.org/drupal/downloads
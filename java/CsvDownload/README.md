# Java CSV Downloader

This folder holds a basic Java App used to download WSPR CSV files.

The primary use for Java in this project will be dealing with Avro
files formats and schemas.

At present, all this app does is download a CSV from [WSPRnet][]
You can change what file gets pulled by editing the script itself.

In the future, this may be converted to a command-line option
format, but for now, it's manual.

```java
// package com.ki7mt.spark.utils;
// Class: DownloadArchive.java

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

[WSPRnet]: http://www.wsprnet.org/drupal/downloads
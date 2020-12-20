# Overview

WSPR CSV is a set of tools for downloading, managing, and converting [WSPRnet][] `CSV` files
for further processing on analytics stacks such as `R`, `PySpark`, `Spark`, `Scala` or any
other Big Data tool chains.

The original festures of this project performed basic file transformations with a few select
`R` script to render vvisualizations.

The Focus for this project will change over to managing the CSV files themsevs. All post processing will be performed by seperate `PySPark`, `Scala`, and `R`.

>NOTE: During development, this package **is not** intended for pip installaiton.
> It should be checked out and run from source.

[WSPRnet]: http://wsprnet.org/drupal/
[Download Section]: http://wsprnet.org/drupal/downloads
[Epoch]: https://en.wikipedia.org/wiki/Unix_time

# Epoch Conversion

This is a sample program that takes the Epoch Time listed in a WSPRnet Spot and
converts it to seven additional columns in human readable format. It's very fast and efficient,
particularly when processing files with millions of rows. It also corrects `null` values in
the version column. Additional investigation into the `null` values for Azimuth is needed
as show below.

- x_timestamp is the date and time
- x_date is just the date
- x_year year only
- x_month month only
- x_day day only
- x_hours hour only
- x_minute minute only

## Usage

To build the apps, perform the following in a terminal

```bash
# change directories to spark/ and type the following:

python build_jars.py && cd jars/

# run the application supplying a properly formatted csv file
# change the input-path as needed

spark-submit --master local[*] EpochConversion-assembly-1.0.jar /data/wsprspots-2021-02.csv
```

## Sample Output

Using Spark Submit, the following is for `wsprspots-2021-02`.

```bash
Object        : EpochCoversion
Process File  : /data/wsprspots-2021-02.csv
Tiimestamp    : 2021-03-23T03:32:13.210
Description   : Convert Epoch Time to Human Readable Values

Application Actions to Process CSV File
- Create a Spark Session
- Create the Spot Schema
- Read the CSV file into a DataSet
- Cleaning up Version null values
- Select the column we want to process
- Setup Epoch Conversion
- Execute the Query

+----------+----------+--------+------+---+---------+--------+------+-----+-----+--------+-------+----+--------+----+-------------------+----------+------+-------+-----+------+--------+
|    SpotID| Timestamp|Reporter|RxGrid|SNR|Frequency|CallSign|  Grid|Power|Drift|Distance|Azimuth|Band| Version|Code|        x_timestamp|    x_date|x_year|x_month|x_day|x_hour|x_minute|
+----------+----------+--------+------+---+---------+--------+------+-----+-----+--------+-------+----+--------+----+-------------------+----------+------+-------+-----+------+--------+
|2789667222|1612137600|  2E0PYB|JO01is|  6|14.097079|  2E0DYH|JO01ht|   10|    0|       7|   null|  14|   2.1.2|   1|2021-02-01 00:00:00|2021-02-01|  2021|      2|    1|     0|       0|
|2789666501|1612137600|  EA8BFK|IL38bo|-17| 7.040078|  2E0ETU|  IO81|   27|    0|    2699|   null|   7|      nr|   1|2021-02-01 00:00:00|2021-02-01|  2021|      2|    1|     0|       0|
|2789669160|1612137600|  HB9TMC|JN46lj|-20| 7.040076|  2E0ETU|  IO81|   27|    0|    1041|    118|   7|      nr|   1|2021-02-01 00:00:00|2021-02-01|  2021|      2|    1|     0|       0|
|2789667577|1612137600|  HG5ACZ|JN87pq|-16| 7.040077|  2E0ETU|  IO81|   27|    0|    1520|     98|   7|1.3 Kiwi|   1|2021-02-01 00:00:00|2021-02-01|  2021|      2|    1|     0|       0|
|2789667439|1612137600|   I3JPA|JN65dk|-13| 7.040078|  2E0ETU|  IO81|   27|    0|    1311|    115|   7|1.3 Kiwi|   1|2021-02-01 00:00:00|2021-02-01|  2021|      2|    1|     0|       0|
+----------+----------+--------+------+---+---------+--------+------+-----+-----+--------+-------+----+--------+----+-------------------+----------+------+-------+-----+------+--------+
only showing top 5 rows

Elapsed Time : 1.371 sec
Epoch Conversion Processed : (63,369,286) Spots
```

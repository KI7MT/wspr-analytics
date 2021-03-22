# Epoch Conversion

This is a sample program that takes the Epoch Time listed in a WSPRnet Spot and
converts it to seven additional columns in human readable format. It's very fast and effecient,
particularly when processing files with millions of rows:

- x_timestamp is the date and time
- x_date is just the date
- x_year year only
- x_month month only
- x_day day only
- x_hous hour only
- x_minute minute only

## Usage

To build the apps, perform the following in a terminal

```bash
# change directories to spark/ and type the following:

python build_jars.py

# if the build passed

cd jars/

# run the application supplying a properly formatted csv file
# change the input-path as needed

spark-submit --master local[*] EpochConversion-assembly-1.0.jar /data/wsprspots-2008-03.csv
```

## Sample Output

Using Spark Submit, the following is for `wsprspots-2008-03`.

```bash
Object        : EpochCoversion
Process File  : /data/wsprspots-2008-03.csv
Tiimestamp    : 2021-03-22T08:56:22.446
Description   : Convert Epoch Time to Human Readable Values

Steps For Processing The CSV File
- Create a Spark Session
- Create the Spot Schema
- Read the CSV file into a DataSet
- Select the column we want to process
- Setup Epoh Conversion
- Execute the Query

+------+----------+--------+------+---+---------+--------+------+-----+-----+--------+-------+----+-------+----+-------------------+----------+------+-------+-----+------+--------+
|SpotID| Timestamp|Reporter|RxGrid|SNR|Frequency|CallSign|  Grid|Power|Drift|Distance|Azimuth|Band|Version|Code|        x_timestamp|    x_date|x_year|x_month|x_day|x_hour|x_minute|
+------+----------+--------+------+---+---------+--------+------+-----+-----+--------+-------+----+-------+----+-------------------+----------+------+-------+-----+------+--------+
| 17230|1205272920|  WD4KPD|FM15mm|-21|10.140106|    K1JT|FN20qi|   37|    0|     575|   null|  10|   null|   0|2008-03-11 22:02:00|2008-03-11|  2008|      3|   11|    22|       2|
| 11937|1205272920|  WD4KPD|FM15mm|-26|10.140188|    K7EK|CN87tb|   37|    0|    3943|     92|  10|   null|   0|2008-03-11 22:02:00|2008-03-11|  2008|      3|   11|    22|       2|
| 11936|1205273040|  WD4KPD|FM15mm|-21|10.140106|    K1JT|FN20qi|   37|    0|     575|   null|  10|   null|   0|2008-03-11 22:04:00|2008-03-11|  2008|      3|   11|    22|       4|
| 11935|1205273160|  WD4KPD|FM15mm|-26|10.140106|    K1JT|FN20qi|   37|    0|     575|   null|  10|   null|   0|2008-03-11 22:06:00|2008-03-11|  2008|      3|   11|    22|       6|
| 17226|1205273160|  WD4KPD|FM15mm|-26|10.140188|    K7EK|CN87tb|   37|    0|    3943|     92|  10|   null|   0|2008-03-11 22:06:00|2008-03-11|  2008|      3|   11|    22|       6|
+------+----------+--------+------+---+---------+--------+------+-----+-----+--------+-------+----+-------+----+-------------------+----------+------+-------+-----+------+--------+
only showing top 5 rows

Elapsed Time : 1.283 sec

Getting final row count, please wait...
Epoch Conversion Processed : (93,890) Spots 
Elapsed Time : 0.237 sec
```

package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"

	. "github.com/logrusorgru/aurora"

	flag "github.com/spf13/pflag"

	"github.com/xitongsys/parquet-go-source/local"
	"github.com/xitongsys/parquet-go/parquet"
	"github.com/xitongsys/parquet-go/writer"
)

// variables used throughout the apps
var (
	appname     string
	version     string
	date        string
	description string = "Golang app to convert CSV to Parquet."
	//	fileInfo    *os.FileInfo
	err error
)

// Spot is a struct representing on reported WSPR spot.
// IN this case, it's reporesting a parquet-go structure
// For details see: https://github.com/xitongsys/parquet-go
type Spot struct {
	SpotID    string `parquet:"name=spotid, type=BYTE_ARRAY"`
	Timestamp string `parquet:"name=timestamp, type=BYTE_ARRAY"`
	Reporter  string `parquet:"name=reporter, type=BYTE_ARRAY"`
	RxGrid    string `parquet:"name=rxgrid, type=BYTE_ARRAY"`
	SNR       string `parquet:"name=snr, type=BYTE_ARRAY"`
	Frequency string `parquet:"name=frequency, type=BYTE_ARRAY"`
	Callsign  string `parquet:"name=callsign, type=BYTE_ARRAY"`
	Grid      string `parquet:"name=grid, type=BYTE_ARRAY"`
	Power     string `parquet:"name=power, type=BYTE_ARRAY"`
	Drift     string `parquet:"name=drift, type=BYTE_ARRAY"`
	Distance  string `parquet:"name=sdistance, type=BYTE_ARRAY"`
	Azimuth   string `parquet:"name=azimuth, type=BYTE_ARRAY"`
	Band      string `parquet:"name=band, type=BYTE_ARRAY"`
	Version   string `parquet:"name=version, type=BYTE_ARRAY"`
	Code      string `parquet:"name=code, type=BYTE_ARRAY"`
}

// CheckError is a function to print out errors
func CheckError(e error) {
	if err != nil {
		fmt.Println(e)
	}
}

// ClearScreen simply clears the terminal screen of any existing text
func ClearScreen() {
	c := exec.Command("clear")
	c.Stdout = os.Stdout
	c.Run()
}

// UserHomeDir attempts to get the users home directory on Win and Linux
func UserHomeDir() string {
	if runtime.GOOS == "windows" {
		home := os.Getenv("HOMEDRIVE") + os.Getenv("HOMEPATH")
		if home == "" {
			home = os.Getenv("USERPROFILE")
		}
		return home
	}
	return os.Getenv("HOME")
}

// main application entry point
func main() {

	// clear the screen
	ClearScreen()

	// defaul source and destination folder locations
	defaultSrcDir := filepath.Join(UserHomeDir(), "Downloads", "wsprnet", "csv")
	defaultDestDir := filepath.Join(UserHomeDir(), "Downloads", "wsprnet", "parquet")

	var srcdir = flag.StringP("source", "s", defaultSrcDir, "source directory path")
	var destdir = flag.StringP("dest", "d", defaultDestDir, "destination directory path")
	var file = flag.StringP("file", "f", "wsprnet-2008-03.csv", "source file name")
	//var compression = flag.StringP("compression", "c", "CompressionCodec_SNAPPY", "parquet compression format")
	flag.Parse()

	// string builder for source path + filename after args are passed in
	filePath := filepath.Join(*srcdir, *file)

	// if the path + file don't exist, we can't convert it so exit.
	fmt.Println("* Checking CSV File")
	_, err := os.Stat(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			fmt.Println(Red("I/O File Path Error\n"))
			fmt.Println("==> " + filePath + " does not exist.\n")
			os.Exit(-1)
		}
	}

	// check if we can create the parquet file in this location
	fmt.Println("* Checking Write Permissions")
	outfile := filepath.Join(*destdir, "spot.parquet")
	fw, err := local.NewLocalFileWriter(outfile)
	if err != nil {
		log.Println("Can't create local file", err)
		return
	}

	pw, err := writer.NewParquetWriter(fw, new(Spot), 2)
	if err != nil {
		log.Println("Can't create parquet writer", err)
		return
	}

	// TODO: make compresion user selectable
	pw.RowGroupSize = 128 * 1024 * 1024 //128M
	pw.CompressionType = parquet.CompressionCodec_SNAPPY

	// this is the sourceCSV file
	csvFile, _ := os.Open(filePath)
	reader := csv.NewReader(bufio.NewReader(csvFile))
	counter := 0
	fmt.Println("* Processing CSV file\n")
	for {
		line, error := reader.Read()
		if error == io.EOF {
			break
		} else if error != nil {
			log.Fatal(error)
		}
		spot := Spot{
			SpotID:    line[0],
			Timestamp: line[1],
			Reporter:  line[2],
			RxGrid:    line[3],
			SNR:       line[4],
			Frequency: line[5],
			Callsign:  line[6],
			Grid:      line[7],
			Power:     line[8],
			Drift:     line[9],
			Distance:  line[10],
			Azimuth:   line[11],
			Band:      line[12],
			Version:   line[13],
			Code:      line[14],
		}
		if err = pw.Write(spot); err != nil {
			log.Println("Write error", err)
		}
		counter++
		fmt.Print("\r Line Count: ", counter)
	}

	if err = pw.WriteStop(); err != nil {
		log.Println("\nWriteStop error", err)
		return
	}

	log.Println("Write Finished\n")
	fw.Close()
}

/*
	Source: https://github.com/xitongsys/parquet-go/#compression-type

	Supported Compression Types

		CompressionCodec_UNCOMPRESSED 	YES
		CompressionCodec_SNAPPY			YES (default)
		CompressionCodec_GZIP			YES
		CompressionCodec_LZO			NO
		CompressionCodec_BROTLI			NO
		CompressionCodec_LZ4			NO
		CompressionCodec_ZSTD			YES
*/

/*
	Spot struct from scala

val spotSchema = new StructType()
	.add("SpotID", LongType, nullable = false)
	.add("Timestamp", IntegerType, nullable = false)
	.add("Reporter", StringType, nullable = false)
	.add("RxGrid", StringType, nullable = false)
	.add("SNR", ByteType, nullable = false)
	.add("Frequency", DoubleType, nullable = false)
	.add("CallSign", StringType, nullable = false)
	.add("Grid", StringType, nullable = false)
	.add("Power", ByteType, nullable = false)
	.add("Drift", ByteType, nullable = false)
	.add("Distance", ShortType, nullable = false)
	.add("Azimuth", ByteType, nullable = false)
	.add("Band", ByteType, nullable = false)
	.add("Version", StringType, nullable = true)
	.add("Code", ByteType, nullable = true)

Golang parquet-go struct convertion

type Spot struct {
	SpotID    string `parquet:"name=spotid, type=BYTE_ARRAY, convertedtype=INT_64"`
	Timestamp string `parquet:"name=timestamp, type=BYTE_ARRAY, convertedtype=INT_64"`
	Reporter  string `parquet:"name=reporter, type=BYTE_ARRAY"`
	RxGrid    string `parquet:"name=rxgrid, type=BYTE_ARRAY"`
	SNR       string `parquet:"name=snr, type=BYTE_ARRAY, convertedtype=INT_16"`
	Frequency string `parquet:"name=frequency, type=BYTE_ARRAY, convertedtype=DOUBLE"`
	Callsign  string `parquet:"name=callsign, type=BYTE_ARRAY"`
	Grid      string `parquet:"name=grid, type=BYTE_ARRAY"`
	Power     string `parquet:"name=power, type=BYTE_ARRAY, convertedtype=INT_16"`
	Drift     string `parquet:"name=drift, type=BYTE_ARRAY, convertedtype=INT_16"`
	Distance  string `parquet:"name=sdistance, type=BYTE_ARRAY, convertedtype=INT_32"`
	Azimuth   string `parquet:"name=azimuth, type=BYTE_ARRAY, convertedtype=INT_16"`
	Band      string `parquet:"name=band, type=BYTE_ARRAY, convertedtype=INT_16"`
	Version   string `parquet:"name=version, type=BYTE_ARRAY"`
	Code      string `parquet:"name=code, type=BYTE_ARRAY, convertedtype=INT_16"`
}


*/

package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"strings"

	"github.com/dustin/go-humanize"
	flag "github.com/spf13/pflag"
)

// version flags for main funciton
var (
	appname     string
	version     string
	date        string
	description string
)

// WriteCounter counts the number of bytes written to it
type WriteCounter struct {
	Total uint64
}

// progress function
func (wc *WriteCounter) Write(p []byte) (int, error) {
	n := len(p)
	wc.Total += uint64(n)
	wc.PrintProgress()
	return n, nil
}

// print progress
func (wc WriteCounter) PrintProgress() {
	// Clear the line by using a character return to go back to the start and remove
	// the remaining characters by filling it with spaces
	fmt.Printf("\r%s", strings.Repeat(" ", 50))

	// Return again and print current status of download
	// We use the humanize package to print the bytes in a meaningful way (e.g. 10 MB)
	fmt.Printf("\rDownload Progress ..: %s ", humanize.Bytes(wc.Total))
}

// DownloadFile will downlaods a url to a local file.
func DownloadFile(filepath string, url string) error {

	// using *.tmp won't overwrite the file until the download is complete
	out, err := os.Create(filepath + ".tmp")
	if err != nil {
		return err
	}

	// go get the file
	resp, err := http.Get(url)
	if err != nil {
		out.Close()
		return err
	}
	defer resp.Body.Close()

	// progress reporter
	counter := &WriteCounter{}
	if _, err = io.Copy(out, io.TeeReader(resp.Body, counter)); err != nil {
		out.Close()
		return err
	}

	fmt.Print("\n")

	// close the output file
	out.Close()

	if err = os.Rename(filepath+".tmp", filepath); err != nil {
		return err
	}
	return nil
}

// exists returns whether the given file or directory exists
func exists(path string) (bool, error) {
	_, err := os.Stat(path)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, err
}

// clearScreen simple clears the terminal screen of any existing text
func clearScreen() {
	c := exec.Command("clear")
	c.Stdout = os.Stdout
	c.Run()
}

// main ins the main entry point to the application
func main() {

	// clear the screen
	clearScreen()

	fmt.Println("App Name....: ", appname)
	fmt.Println("Version.....: ", version)
	fmt.Println("Build Date..: ", date)

	// if the users does not supply args, 2008 and 03 will be used
	var yearvar = flag.StringP("year", "y", "2008", "specify year like 2008")
	var monthvar = flag.StringP("month", "m", "03", "specify month like 03")
	flag.Parse()

	//  build the string to download the csv file
	fileName := "wsprspots-" + *yearvar + "-" + *monthvar + ".csv.gz"
	fileUrl := "http://wsprnet.org/archive/" + fileName

	// make the destination directory if passes
	//os.MkdirAll(folderPath, os.ModePerm)

	// start dwonloading
	fmt.Println("\nDownloading File ...: " + fileName)

	err := DownloadFile(fileName, fileUrl)
	if err != nil {
		panic(err)
	}

	fmt.Println("Finished")
	fmt.Println()
}

// END - CSVDL

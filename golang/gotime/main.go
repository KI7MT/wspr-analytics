package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"

	flag "github.com/spf13/pflag"

	. "github.com/logrusorgru/aurora"
)

// version flags for main funciton
var (
	appname     string
	version     string
	date        string
	description string = "Golang App to display time zone informaiton."
)

// CheckError is a function to print out errors
func CheckError(e error) {
	if e != nil {
		fmt.Println(e)
	}
}

// clearScreen simple clears the terminal screen of any existing text
func clearScreen() {
	c := exec.Command("clear")
	c.Stdout = os.Stdout
	c.Run()
}

// main is the primary entry point for the app
func main() {

	//clearScreen()

	// set the option flagsd
	var ver = flag.BoolP("version", "v", false, "prints app version information")
	flag.Parse()

	// only print the version informaiton if the user asks for it.
	if *ver {
		fmt.Println("\nApp Name .....: ", Cyan(appname))
		fmt.Println("Version ......: ", Cyan(version))
		fmt.Println("Build Date ...: ", Cyan(date))
		fmt.Println("Description ..: ", Cyan(description))
		fmt.Println()
		os.Exit(0)
	}

	tNow := time.Now()

	fmt.Println(Cyan("\nCurrent Time Data In Local Time Zone"))
	fmt.Println(strings.Repeat("-", 55))

	// Local Time Now in Unix Timestamp format
	tUnix := tNow.Unix()
	fmt.Printf("Unix.Time:\t%d\n", tUnix)

	// Local Time Now serived from unix timestamp
	tLocal := time.Unix(tUnix, 0)
	fmt.Printf("Time.Local:\t%s\n", tLocal)

	// UTC Time serived from unix timestamp
	tUtc := time.Unix(tUnix, 0).UTC()
	fmt.Printf("Time.UTC:\t%s\n", tUtc)

	// Location Source: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
	fmt.Println(Cyan("\nLocal Time For A Specific Zone"))
	fmt.Println(strings.Repeat("-", 58))

	eastern, e := time.LoadLocation("US/Eastern")
	CheckError(e)

	central, e := time.LoadLocation("US/Central")
	CheckError(e)

	mountain, e := time.LoadLocation("US/Mountain")
	CheckError(e)

	pacific, e := time.LoadLocation("US/Pacific")
	CheckError(e)

	alaska, e := time.LoadLocation("US/Alaska")
	CheckError(e)

	hawaii, e := time.LoadLocation("US/Hawaii")
	CheckError(e)

	fmt.Println("US/Eastern:\t", tNow.In(eastern))
	fmt.Println("US/Central:\t", tNow.In(central))
	fmt.Println("US/Mountain:\t", tNow.In(mountain))
	fmt.Println("US/Pacific:\t", tNow.In(pacific))
	fmt.Println("US/Alaska:\t", tNow.In(alaska))
	fmt.Println("US/Hawaii:\t", tNow.In(hawaii))
	/*
	   Goloang Time Format Examples
	*/
	fmt.Println(Cyan("\nGloang Time Package Format Examples"))
	fmt.Println(strings.Repeat("-", 55))
	fmt.Println("ANSIC:  \t", tNow.Format(time.ANSIC))
	fmt.Println("UnixDate:\t", tNow.Format(time.UnixDate))
	fmt.Println("RubyDate:\t", tNow.Format(time.RubyDate))
	fmt.Println("RFC822:  \t", tNow.Format(time.RFC822))
	fmt.Println("RFC822Z:  \t", tNow.Format(time.RFC822Z))
	fmt.Println("RFC850:  \t", tNow.Format(time.RFC850))
	fmt.Println("RFC1123:  \t", tNow.Format(time.RFC1123))
	fmt.Println("RFC1123Z:  \t", tNow.Format(time.RFC1123Z))
	fmt.Println("RFC3339:  \t", tNow.Format(time.RFC3339))
	fmt.Println("Kitchen:    \t", tNow.Format(time.Kitchen))
	fmt.Println("StampMicro:\t", tNow.Format(time.StampMicro))
	fmt.Println("StampMilli:\t", tNow.Format(time.StampMilli))
	fmt.Println("StampNano:\t", tNow.Format(time.StampNano))
	fmt.Println()
}

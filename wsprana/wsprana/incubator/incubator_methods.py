def pavel_rscripts():
    """Pavel Demin Provides the WSPR Analysis Script written in R
       Source: git clone https://github.com/pavel-demin/wsprspots-analyzer.git
    The following has been constructed to feed each of the three script via
    Python.
    Requirements:
        * R Language base
        * R Packages: ggplot, data-table + Deps
    R Language Installation: (may very depending on distribution)
        # In performed in the Gnome terminal:
        sudo apt-get install r-base r-base-dev  libcurl4-gnutls-dev
        # Actions performed in the R console:
        sudo R
        update.packages()
        install.packages("ggplot2", dependencies=TRUE, repos='http://cran.rstudio.com/'
        install.packages("data.table", dependencies=TRUE, repos='http://cran.rstudio.com/')
        quit("no")
    Function Notes:
        * Generates Graph of WSPR Spots Per Hour Per Band using ggplot
        * Generates Average SNR Different Per Day using ggplot
        * Generates SNR over PWR normalized using ggplot
    Each R script requires 5 variables in the following format
        * Input         file-call.csv               # current monthly archive file
        * Output        file-per-hour-call.png      # output image file
        * Call(s)       KI7MT,K1ABC,K1DEF           # callsign(s) to search in archive
        * Start Date    2016-04-01                  # first day of the current month
        * End Date      2016-01-18                  # current day in the month"""
    # setup variables
    now = date_time.strftime("%Y-%m")
    sdate = date_time.strftime("%Y-%m-01")
    edate = date_time.strftime("%Y-%m-%d")
    arg = []

    # this gets passed to the gz extract script
    value = ("wsprspots-" + now + ".csv." + OS_EXT)
    srccsv = (csv_dir + os.sep + 'wsprspots-' + now + '.csv')

    # create the reports directory ../reports/yyyy-mm-dd
    rpt_dir = (reports_dir + os.sep + edate)
    if not os.path.exists(rpt_dir):
        os.makedirs(rpt_dir)

    print("\n" + 45 * '-')
    print(" Pavel Demin's R-Script Report Generator")
    print(45 * '-')
    print(" * Separate Calls with a ',' example: KI7MT,K1ABC,K1DEF")
    callargs = input(" * Enter Callsigns : ").split(',')
    callcount = 0

    # used for snr-diff ( not implemented yet )
    for call in callargs:
        try:
            int(call)
        except ValueError:
            callcount += 1
    # print(" * Processing [ %s ] call(s)" % callcount)
    # loop through the calls and call the R script
    for call in callargs:
        call = call.upper()
        # search_current_month_no_split(call)
        arg1 = rpt_dir + os.sep + now + '-' + call.lower() + '-raw.csv'
        arg3 = call
        arg4 = sdate
        arg5 = edate
        os.chdir(__rscripts__)

        # script 1
        print(" * Generate Spots Per Hour Plot for [ %s ]" % call)
        scr1 = (rpt_dir + os.sep + 'wsprspots-per-hour-' + call.lower() + '.png')
        args = (arg1 + ' ' + scr1 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5)
        with open(os.devnull) as devnull:
            if os.path.isfile(mylogfile):
                subprocess.call(
                    "Rscript wsprspots-per-hour.r " + args,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=devnull)
            else:
                print("   [ %s] Missing CSV. Please generate from the main menu." % call.upper())
        # script 2 ( Not Implemented Yet )
        # print(" * Generate Report ..: SNR DIFF")
        # scr2 = (reports_dir + os.sep + 'wsprspots-snr-diff-' + call + '.png')
        # args = (arg1 + ' ' + scr2 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5)
        # subprocess.call("Rscript wsprspots-snr-diff.r " + args, shell=True)

        # script 3 ( Not Implemented Yet )
        # print(" * Report ......: SNR Normal")
        # scr3 = (reports_dir + os.sep + 'wsprspots-snr-norm-' + call + '.png')
        # args = (arg1 + ' ' + scr3 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5)
        # with open(os.devnull) as devnull:
        #    subprocess.call(
        #        "Rscript wsprspots-snr-norm.r " + args,
        #        shell=True,
        #        stdout=subprocess.PIPE)

    pause()
    return
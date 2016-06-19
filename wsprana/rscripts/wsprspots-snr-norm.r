library(scales)
library(ggplot2)
library(gridExtra)
library(data.table)
library(RColorBrewer)

args <- commandArgs(trailingOnly = TRUE)

file1 <- args[1]
file2 <- args[2]
call <- args[3]
date1 <- args[4]
date2 <- args[5]

# file1 <- 'wsprspots-2016-04-SWLJO20.csv'
# file2 <- 'wsprspots-2016-04-snr-norm-SWLJO20.png'
# call <- 'SWLJO20'
# date1 <- '2016-04-01'
# date2 <- '2016-12-31'

colNames <- c('id', 'epoch', 'rcall',
  'rgrid', 'snr', 'freq', 'call',
  'grid', 'power', 'drift', 'distance',
  'azimuth', 'band', 'version', 'code')
colClasses <- c('numeric', 'numeric', 'character',
  'character', 'numeric', 'numeric', 'character',
  'character', 'numeric', 'numeric', 'numeric',
  'numeric', 'numeric', 'character', 'numeric')

spots <- as.data.table(read.table(file1, header = F, sep = ',', col.names = colNames, colClasses = colClasses))

spots[, time := as.POSIXct(epoch, origin = '1970-01-01')]

freqs <- c(0, 1, 3, 5, 7, 10, 14, 18, 21, 24, 28, 50)
bands <- c('MF', '160m', '80m', '60m', '40m', '30m', '20m', '17m', '15m', '12m', '10m', '6m')

proc1 <- function(x){
  x[
    ,
    list(
      norm = mean(snr/power)
    ),
    list(
      mday = mday(time),
      hour = hour(time),
      band
    )
  ]
}

norm <- proc1(spots)
norm[, time := as.POSIXct(paste0('2016/04/', mday, ' ', hour, ':00:00'))]

subset <- norm[time >= as.POSIXct(paste0(date1, ' 00:00:00')) & time <= as.POSIXct(paste0(date2, ' 23:59:59'))]

p <- lapply(2:7, function(i)
  ggplot(data = subset[band == freqs[i]], aes(x = time, y = norm)) +
    geom_point() +
    scale_x_datetime(breaks = date_breaks('1 day'), minor_breaks = date_breaks('1 hour')) +
    theme(axis.text.x = element_text(angle = 45)) +
    labs(title = bands[i]) + labs(x = '', y = 'SNR over power') +
    theme(legend.position = 'none') + coord_cartesian(ylim = c(-2.0, 1.0))
)

png(file2, width = 1200, height = 600, res = 90)
grid.arrange(arrangeGrob(grobs = p, nrow = 2))
dev.off()

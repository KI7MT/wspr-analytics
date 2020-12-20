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
# file2 <- 'wsprspots-2016-04-per-hour-SWLJO20.png'
# call <- 'SWLJO20'
# date1 <- '2016-04-01'
# date2 <- '2016-12-31'

colNames <- c('id', 'epoch', 'rcall',
  'rgrid', 'snr', 'freq', 'call',
  'grid', 'power', 'drift', 'distance',
  'azimuth', 'band', 'version', 'code')
colClasses = c('numeric', 'numeric', 'character',
  'character', 'numeric', 'numeric', 'character',
  'character', 'numeric', 'numeric', 'numeric',
  'numeric', 'numeric', 'character', 'numeric')

spots <- as.data.table(read.table(file1, header = F, sep = ',', col.names = colNames, colClasses = colClasses))

spots[, time := as.POSIXct(epoch, origin = '1970-01-01')]

bands <- c(0, 1, 3, 5, 7, 10, 14, 18, 21, 24, 28, 50)
names <- c('MF', '160m', '80m', '60m', '40m', '30m', '20m', '17m', '15m', '12m', '10m', '6m')

for(i in 1:length(bands))
{
  spots[band == bands[i], name := names[i]]
}

subset <- spots[time >= as.POSIXct(paste0(date1, ' 00:00:00')) & time <= as.POSIXct(paste0(date2, ' 23:59:59'))]

palette <- rev(brewer.pal(length(names), 'Set3'))
names(palette) <- names

png(file2, width = 760, height = 570, res = 120)

ggplot(data = subset, aes(time, fill = factor(name, levels = names))) +
  geom_histogram(binwidth = 3600) +
  scale_fill_manual(values = palette) +
  scale_x_datetime(breaks = date_breaks('1 day'), minor_breaks = date_breaks('1 hour')) +
  guides(fill = guide_legend(title = NULL, reverse = TRUE)) +
  theme(axis.text.x = element_text(angle = 45)) +
  labs(title = paste0('Number of WSPR spots per hour (', call, ')')) +
  labs(x = '', y = '')

dev.off()

# ggplot(data = subset(subset, band == '40m'), aes(azimuth, distance)) + geom_point() + coord_polar() + scale_x_continuous(breaks = seq(0, 360, 30), limits = c(0, 360))

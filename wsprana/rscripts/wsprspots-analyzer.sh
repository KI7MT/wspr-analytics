file=wsprspots-2016-04

dates="2016-04-01 2016-04-14"

test -f ${file}.csv.gz || curl -LO http://wsprnet.org/archive/${file}.csv.gz

for call in PI4THT PA7T DK5HH DK6UG DL0HT DL1SDZ SWLJO20 LA3JJ IW2MVI
do
  test -f ${file}-${call}.csv || gunzip < ${file}.csv.gz | awk -F, -vcall=${call} '$3==call{print}' > ${file}-${call}.csv

  Rscript wsprspots-per-hour.r ${file}-${call}.csv ${file}-per-hour-${call}.png $call $dates
  Rscript wsprspots-snr-diff.r ${file}-${call}.csv ${file}-PI4THT.csv ${file}-snr-diff-${call}.png $call $dates
  Rscript wsprspots-snr-norm.r ${file}-${call}.csv ${file}-snr-norm-${call}.png $call $dates
done

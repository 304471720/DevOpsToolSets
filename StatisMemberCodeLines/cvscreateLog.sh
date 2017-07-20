echo $1
rm -rf Statis.txt
rm -rf AllStatis.txt
SERVICES=" project5 project6 project7 project8 project9 project10 project11 project12 project13 project14 "
#SERVICES="project8 project9  "

for dir in $SERVICES
do
 cd ${dir}
 cvs up
 cvs log  -d $1 > logfile.log
# ./AndroidStatis.pl logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{for(i in s){  print s[i], i  } }' >> ../Statis.txt
 cd ..
done
./project5/AndroidStatis.pl project5/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{for(i in s){  print s[i], i  } }'  > AndroidStatis.txt
./project6/AndroidStatis.pl project6/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{for(i in s){  print s[i], i  } }'  > project6Statis.txt
./project7/AndroidStatis.pl project7/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{for(i in s){  print s[i], i  } }'  > project7Statis.txt
./project8/IOSStatis.pl project8/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{ for(i in s){  print s[i], i  } }' | sort -rn  > project8Statis.txt
./project9/IOSStatis.pl project9/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{ for(i in s){  print s[i], i  } }' | sort -rn  > IOStatis.txt
./project10/IOSStatis.pl project10/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{ for(i in s){  print s[i], i  } }' | sort -rn  > project10Statis.txt
./project11/AndroidStatis.pl project11/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{for(i in s){  print s[i], i  } }'  > project11Statis.txt
./project12/AndroidStatis.pl project12/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{for(i in s){  print s[i], i  } }'  > project12Statis.txt
./project13/AndroidStatis.pl project13/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{for(i in s){  print s[i], i  } }'  > project13.txt
./project14/AndroidStatis.pl  project14/logfile.log | grep 'lines:' | awk '{if($9+$10>=0) print $5"  "$9; else print  $5"  "0-$10}' | awk '{s[$1] += $2}END{for(i in s){  print s[i], i  } }'  > project14.txt
cat AndroidStatis.txt >> AllStatis.txt
cat project6Statis.txt >> AllStatis.txt
cat project7Statis.txt >> AllStatis.txt
cat project11Statis.txt >> AllStatis.txt
cat project12Statis.txt >> AllStatis.txt
cat project13.txt >> AllStatis.txt
cat project14.txt >> AllStatis.txt
cat project8Statis.txt >> AllStatis.txt
cat IOStatis.txt >> AllStatis.txt
cat project10Statis.txt >> AllStatis.txt
rm -rf AndroidStatis.txt project6Statis.txt project7Statis.txt  project11Statis.txt project12Statis.txt project8Statis.txt IOStatis.txt project10Statis.txt   project13.txt project14.txt
rm -rf project5/logfile.log project6/logfile.log project7/logfile.log project8/logfile.log project9/logfile.log project10/logfile.log project11/logfile.log project12/logfile.log project13/logfile.log project14/logfile.log
#cat AllStatis.conf  >> AllStatis.txt
mv  AllStatis.txt  Statis.txt
#cat Statis.txt | awk '{s[$2] += $1}END{ for(i in s){  print s[i], i } }'  | awk '{if($1>=6000 ){ print 6000-($1%500)" "$2 ;}else  print $1" "$2;}' | sort -rn > result.txt

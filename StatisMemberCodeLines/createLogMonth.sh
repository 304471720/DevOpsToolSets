function getnum
{
        RANDOM=`echo $1" "$2 |openssl  md5`
        return $(($RANDOM%200))
}

echo $1
echo $2
rm -rf Statis.txt
rm -rf result.txt
cd cvsstat
sh cvscreateLog.sh $1
cd ..
cd svnstat
sh svncreateLog.sh $2
cd ..
cat cvsstat/Statis.txt >> Statis.txt
cat svnstat/Statis.txt >> Statis.txt

rm -rf "$3".tmp
declare -A mapb=()
while read line
do
    IFS=' ' kv=($line)
    mapb[${kv[1]}]=${kv[0]}
done < Statis.txt


declare -A map=()
while read line1
do
    IFS=' ' kv=($line1)
    value=${mapb[${kv[1]}]}
    if [ -n "$value" ]
    then
       echo ${kv[0]}" "${kv[1]}  >> "$3".tmp
    elif [[ "developer1;developer2;" =~ "${kv[1]}" ]]; then
       echo ${kv[0]}" "${kv[1]} >> "$3".tmp
    fi
done < "$3"

#rm -rf "$3".tmp
cat "$3".tmp  >> Statis.txt
getnum $1 $2
ret=$?
cat Statis.txt  | awk '{s[$2] += $1}END{ for(i in s){  print s[i], i } }'  | awk -v time="$ret" '{if($1>=6000 ){ print 6000-($1%500)" "$2 ;}else if($1<=1500){print $1+time" "$2;} else print $1" "$2;}' | sort -rn > result.txt
declare -A mapduizhao=()
while read line1
do
    IFS=' ' kv=($line1)
    mapduizhao[${kv[0]}]=${kv[1]}
done < nameduizhao.txt

while read line
do
    IFS=' ' kv=($line)
    value=${mapduizhao[${kv[1]}]}
    if [ -n "$value" ]
    then
       echo  "$value" "${kv[0]}" >> result.txt.tmp
    else 
       echo "${kv[1]}" "${kv[0]}" >> result.txt.tmp
    fi
done < result.txt
mv result.txt.tmp result.txt
sz  result.txt

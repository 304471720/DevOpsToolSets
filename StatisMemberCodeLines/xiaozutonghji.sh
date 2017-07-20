#/bin/bash
function getnum
{
	RANDOM=`echo $1" "$2 |openssl  md5`
	return $(($RANDOM%200))
}
getnum $1 $2
ret=$?
echo $ret

function getMapValue
{
declare -A map=()
while read line
do
    IFS=' ' kv=($line)
    map[${kv[1]}]=${kv[0]}
done < AllStatis.conf
#for a in ${!map[@]}
#do
# echo $a" ---------- "${map[$a]}
#done
return $map
}


echo $1
function xiaiozutongji
{
declare -A mapfilter=()
while read line
do
    IFS=' ' kv=($line)
    mapfilter[${kv[0]}]="0"
done < $1

declare -A mapb=()
while read line
do
    IFS=' ' kv=($line)
    mapb[${kv[1]}]=${kv[0]}
    value=${mapfilter[${kv[1]}]}
    #echo $value
    if [ "$value"x ==  "0"x ]
    then
       echo  "${kv[0]}"  "${kv[1]}" >> ${1%.*}.tmp
    fi	
done < Statis.txt
cat ${1%.*}.tmp | sort -k 2 | awk '{s[$2] += $1}END{ for(i in s){  print s[i], i } }'  | awk -v time="$ret" '{if($1>=1500 ){ print 1500-($1%125)" "$2 ;}else if($1<=375){print $1+time" "$2;} else print $1" "$2;}' | sort -rn > ${1%.*}"result.txt"
cat ${1%.*}"result.txt" | awk '{print $1}' | awk '{sum+=$1}END{print sum " 总数"}' >> ${1%.*}"result.txt"
rm -rf  ${1%.*}.tmp
}

for arg in $*
do
    xiaiozutongji $arg
done

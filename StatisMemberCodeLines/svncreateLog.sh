echo $1
rm -rf Statis.txt
SERVICES=" project1  project2  project3  project4  project4test  "
#SERVICES=" project1   project3  project4   "
#SERVICES="   "
for dir in $SERVICES
do
 cd ${dir}
 svn up
 svn log -v --xml -r $1  > logfile.log
 java -jar ../statsvn.jar  logfile.log  .
 java -jar ../ParseHtml.jar developers.html >> ../Statis.txt
 cd ..
done 

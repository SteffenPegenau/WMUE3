#!/bin/bash

rm -r course-cotrain-data > /dev/null
link=http://www.cs.cmu.edu/afs/cs.cmu.edu/project/theo-51/www/co-training/data/course-cotrain-data.tar.gz

# Get and unzip the training data
#echo "Loading data..."
#wget $link -O archiv.tar.gz -o wget-log.txt
tar -xf archiv.tar.gz

# Make dir hierarchy flat
trainDir="trainingData"
rm -r $trainDir/* > /dev/null
sep="--"
mkdir -p $trainDir

for typeT in course-cotrain-data/*; do
    if [ -d ${typeT} ]; then
        # Will not run if no directories are available
        typeName=`echo $typeT | cut -d '/' -f2`
        for category in $typeT/*; do
        	if [ -d ${category} ]; then
        		#echo $category
        		for file in $category/*; do
                                url=${file}
                                # Remove "course-cotrain-data/" from path (first 20 letters)
                                url=${url:20}
                                # Remove ':' - windows hates this trick
        			url=${url//:/$sepDP$sep}
        			# Remove '^' - windows may dislike it as well
        			#url=${url//^/--SL--}
                                # Replace '/' with seperator
        			url=${url//\//$sep}
        			# Replace http://www. as it becomes more and more unreadable
        			url=${url//http$sepDP$sep^^www./BEG$sep}
        			# Move it to the trainDir
        			cp $file $trainDir/$url
        		done
        	fi
        done
    fi
done


# Generate binary choice, that is, "true" or "false" value.
BINARY=2
# Marking files as test- and training-data
for file in $trainDir/*; do
    #echo $file
    T=1
    number=$RANDOM
    newName=${file}

    let "number %= $BINARY"
    #let "number >>= 14"
    #  Note that    let "number >>= 14"    gives a better random distribution
    #+ (right shifts out everything except last binary digit).
    if [ "$number" -eq $T ]
    then
        # Training data
        newName=${newName/\//\/train--}
    else
        # Test data
        newName=${newName/\//\/test--}
    fi 
    mv $file $newName
done

total=`ls -1 $trainDir/* | wc -l`
trainTot=`ls -1 $trainDir/train--* | wc -l`
testTot=`ls -1 $trainDir/test--* | wc -l`
courseTest=`ls -1 $trainDir/test--*--course--* | wc -l`
courseTrain=`ls -1 $trainDir/train--*--course--* | wc -l`
nonCourseTest=`ls -1 $trainDir/test--*--non-course--* | wc -l`
nonCourseTrain=`ls -1 $trainDir/train--*--non-course--* | wc -l`
courseTot=`ls -1 $trainDir/*--course--* | wc -l`
nonCourseTot=`ls -1 $trainDir/*--non-course--* | wc -l`



block="---------------------------------------------------------"

echo "Statistics"
echo $block
echo -e "|\t|\ttrain\t|\ttest\t|\tSum\t|"
echo -e "|course\t|\t$courseTrain\t|\t$courseTest\t|\t$courseTot\t|"
echo -e "|not\t|\t$nonCourseTrain\t|\t$nonCourseTest\t|\t$nonCourseTot\t|"
echo -e "|Total\t|\t$trainTot\t|\t$testTot\t|\t$total\t|"
echo $block



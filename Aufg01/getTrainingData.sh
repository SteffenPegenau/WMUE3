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
sep="-----"
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
        			url=${url//:/--DP--}
        			# Remove '^' - windows may dislike it as well
        			#url=${url//^/--SL--}
                                # Replace '/' with seperator
        			url=${url//\//$sep}
        			# Replace http://www. as it becomes more and more unreadable
        			url=${url//http--DP--^^www./BEG---}
        			# Move it to the trainDir
        			cp $file $trainDir/$url
        		done
        	fi
        done
    fi
done

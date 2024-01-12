#!/bin/bash
name="$1"
CROP=$(cat ${name}_crop.txt)
convert ${name}_reference.png ${name}_reference.png -crop $CROP +repage miff:- | compare -verbose -metric MAE  - result.png 2>&1 | grep all | awk '{print $2}'

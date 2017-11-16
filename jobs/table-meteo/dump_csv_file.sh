#!/bin/sh
source=$1
sink_ds_path=$2

mkdir -p $sink_ds_path
cd $sink_ds_path
curl -L -O -J $source


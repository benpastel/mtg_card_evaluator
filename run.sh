#!/bin/bash
if [ ! -f data/AllSets.json ]; then
	echo 'unzipping data files...'
	gunzip data/AllSets.json.gz
fi

echo 'generating features...'
python features/generate.py && \
echo 'Done generating features.'
echo 'Run model/main.m in Matlab or Octave to train the model.'

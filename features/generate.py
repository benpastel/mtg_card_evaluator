__author__ = 'Dustin'

import json
import random
import numpy
import features

f = open('../data/AllCards.json', 'r')
js = json.load(f)

# train_examples = [(example, random.randint(0,1)) for example in js]
# test_examples = [(example, random.randint(0,1)) for example in js]

examples = [features.baseline_feature_extractor(js[example]) for example in js]

print "Merging keys..."
keys = []
for example in examples:
    keys = list(set(keys) | set([key for key in example]))
print len(keys)
print "Keys merged"

X = numpy.zeros((len(examples), len(keys)))

print "Creating matrix..."
for i in range(len(examples)):
    for j in range(len(keys)):
        if keys[j] in examples[i]:
            X[i][j] = examples[i][keys[j]]
print "Finished creating matrix"

print "Saving matrix..."
numpy.savetxt('../data/feature_matrix.txt', X, fmt='%i')
print "Save finished"
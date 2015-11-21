__author__ = 'Dustin'

import json
import random
import numpy
import features
import matplotlib.pyplot as plt
from math import *
from itertools import groupby

# read card and price data
f = open('../data/AllSets.json', 'r')
js = json.load(f)
lines = map(lambda string: string.strip().split("\t"), open("../data/id_price.dat").readlines())

# {multiverseid: float price}
price_dict = {int(line[0]): float(line[1]) for line in lines}

# (card, price).  Restricted to creatures with a multiverseid and a price.
card_prices = [(card, price_dict[card["multiverseid"]])
  for card_set in js for card in js[card_set]["cards"]
  if ("multiverseid" in card and card["multiverseid"] in price_dict
  and "types" in card and "Creature" in card["types"])]

# (feature_dict, price)
# feature_dict: {"feature name": feature value}
examples = [(features.feature_extractor(card), price) for card, price in card_prices]
print "Number of examples: {0}".format(len(examples))

# Shuffle the examples.  Useful for making a random train and test set later in MATLAB
random.seed(1)
random.shuffle(examples)

# create feature list
# only use features that show up on example_threshold examples
example_threshold = 100
all_keys = [key for feature_dict, _ in examples for key, val in feature_dict.items()]
key_counts = {key:len(list(g)) for key, g in groupby(sorted(all_keys))}
keys = list({key for key, count in key_counts.items() if count >= example_threshold})
print "number of potential features: ", len(key_counts.keys())
print "features with enough examples: ", len(keys) 
print "feature names: ", keys[0:100], "..."
feature_name_file = file('../data/feature_names.txt', 'w');
for key in keys:
  print >> feature_name_file, key

# Create feature matrix X.  All features not determined for a given card are entered with value 0.
# Create price vector Y
X = numpy.zeros((len(examples), len(keys)))
Y = numpy.zeros((len(examples), 1))
print "Creating matrix..."
for i in range(len(examples)):
    for j in range(len(keys)):
        if keys[j] in examples[i][0]:
            X[i][j] = examples[i][0][keys[j]]
    Y[i] = examples[i][1]
print "Finished creating matrix"

print "Saving matrix..."
numpy.savetxt('../data/feature_matrix.txt', X, fmt='%f')
print "Save finished"
print "Saving prices..."
numpy.savetxt('../data/price_vector.txt', Y, fmt='%f')
print "Save finished"


## Print some examples
# print examples[0]
# print X[0]
# print Y[0]
print "Sen Triplets example"
example = {
               "name" : "Sen Triplets",

           "manaCost" : "{2}{W}{U}{B}",
                "cmc" : 5,
             "colors" : ["White", "Blue", "Black"],

               "type" : "Legendary Artifact Creature - Human Wizard",
         "supertypes" : ["Legendary"],
              "types" : ["Artifact", "Creature"],
           "subtypes" : ["Human", "Wizard"],

             "rarity" : "Mythic Rare",

               "text" : "At the beginning of your upkeep, choose target opponent.  This turn, that player can't cast spells or activate abilities and plays with his or her hand revealed.  You may play cards from that player's hand this turn.",

             "flavor" : "They are the masters of your mind.",

             "artist" : "Greg Staples",
             "number" : "109",

              "power" : "3",
          "toughness" : "3",

             "layout" : "normal",
       "multiverseid" : 180607,
          "imageName" : "sen triplets",
                 "id" : "3129aee7f26a4282ce131db7d417b1bc3338c4d4"
    }

example_features = features.feature_extractor(example)
print {key: val for key, val in example_features.items() if key in keys}
__author__ = 'Dustin'

import json
import random
import numpy
import features
import matplotlib.pyplot as plt
from math import *

# Reads card data into json format and reads price data
f = open('../data/AllSets.json', 'r')
js = json.load(f)
lines = map(lambda string: string.strip().split("\t"), open("../data/id_price.dat").readlines())

# price_dict:   Dictionary with entries     {int multiverseid: float price}
price_dict = {int(line[0]): float(line[1]) for line in lines}

# examples:  List of tuples for each card    (feature_dict, float price)
# feature_dict:  List of features for a card {"Feature name": feature value}
# examples is restricted to cards with a multiverseid and a price.  You can add additional restrictions to the end like ""types" in card and "Creature" in card["types"]" to get only Creatures.
examples = [(features.feature_extractor(card), price_dict[card["multiverseid"]]) for card_set in js for card in js[card_set]["cards"] if ("multiverseid" in card and card["multiverseid"] in price_dict and "types" in card and "Creature" in card["types"])]
print "Number of examples: {0}".format(len(examples))

## If you want to restrict the data based on value, you can sort examples and then take a subset of them
# examples.sort(key=lambda tup: tup[1])
# examples = examples[10000:len(examples)]
# print "Number of examples (restricted): {0}".format(len(examples))

# Shuffle the examples.  Useful for making a random train and test set later in MATLAB
random.seed(1)
random.shuffle(examples)

# Create list of all features extracted from all examples
keys = {key for example in examples for key in example[0]}
keys = list(keys)
print "Number of features: {0}".format(len(keys))
# print keys

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
# print "Sen Triplets example"
# example = {
#                "name" : "Sen Triplets",
#
#            "manaCost" : "{2}{W}{U}{B}",
#                 "cmc" : 5,
#              "colors" : ["White", "Blue", "Black"],
#
#                "type" : "Legendary Artifact Creature - Human Wizard",
#          "supertypes" : ["Legendary"],
#               "types" : ["Artifact", "Creature"],
#            "subtypes" : ["Human", "Wizard"],
#
#              "rarity" : "Mythic Rare",
#
#                "text" : "At the beginning of your upkeep, choose target opponent.  This turn, that player can't cast spells or activate abilities and plays with his or her hand revealed.  You may play cards from that player's hand this turn.",
#
#              "flavor" : "They are the masters of your mind.",
#
#              "artist" : "Greg Staples",
#              "number" : "109",
#
#               "power" : "3",
#           "toughness" : "3",
#
#              "layout" : "normal",
#        "multiverseid" : 180607,
#           "imageName" : "sen triplets",
#                  "id" : "3129aee7f26a4282ce131db7d417b1bc3338c4d4"
#     }
#
# print features.baseline_feature_extractor(example)
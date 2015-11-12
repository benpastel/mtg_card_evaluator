__author__ = 'Dustin'

import json
import random
import numpy
import features

f = open('../data/AllSets.json', 'r')
js = json.load(f)
lines = map(lambda string: string.strip().split("\t"), open("../data/id_price.dat").readlines())
price_dict = {int(line[0]): float(line[1]) for line in lines}

examples = [(features.baseline_feature_extractor(card), price_dict[card["multiverseid"]]) for card_set in js for card in js[card_set]["cards"] if ("multiverseid" in card and card["multiverseid"] in price_dict)]
print "Number of examples: {0}".format(len(examples))

# Shuffle the examples in order to split train and test set easily
# random.seed(1)
# random.shuffle(examples)

keys = {key for example in examples for key in example[0]}
keys = list(keys)
print "Number of features: {0}".format(len(keys))

X = numpy.zeros((len(examples), len(keys)))
Y = numpy.zeros((len(examples), 1))

print "Creating matrix..."
for i in range(len(examples)):
    for j in range(len(keys)):
        if keys[j] in examples[i][0]:
            X[i][j] = examples[i][0][keys[j]]
    Y[i] = examples[i][1]
print "Finished creating matrix"

print examples[0]
print X[0]
print Y[0]

print "Saving matrix..."
numpy.savetxt('../data/feature_matrix.txt', X, fmt='%f')
print "Save finished"
print "Saving prices..."
numpy.savetxt('../data/price_vector.txt', Y, fmt='%f')
print "Save finished"

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

print features.baseline_feature_extractor(example)
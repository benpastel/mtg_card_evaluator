__author__ = 'Dustin'

import json
import random
import numpy
import features

f = open('../data/AllSets.json', 'r')
js = json.load(f)

random.seed(1)
# train_examples = [(example, random.randint(0,1)) for example in js]
# test_examples = [(example, random.randint(0,1)) for example in js]

examples = [features.baseline_feature_extractor(card) for card_set in js for card in js[card_set]["cards"]]
print "Number of cards in json: {0}".format(len(examples))
random.shuffle(examples)

lines = map(lambda string: string.strip().split("\t"), open("../data/id_price.dat").readlines())
price_dict = {int(line[0]): float(line[1]) for line in lines}

print "Merging keys..."
keys = set([])
for example in examples:
    keys = keys | set(example.keys())
keys = list(keys)
print "Keys merged"
print "Number of features: {0}".format(len(keys))

examples_new = []
for example in examples:
    if "multiverseid" in example and example["multiverseid"] in price_dict:
        examples_new.append(example)
examples = examples_new
print "Number of examples with prices: {0}".format(len(examples))


X = numpy.zeros((len(examples), len(keys)))
Y = numpy.zeros((len(examples), 1))

print "Creating matrix..."
for i in range(len(examples)):
    for j in range(len(keys)):
        if keys[j] in examples[i]:
            X[i][j] = examples[i][keys[j]]
    Y[i] = price_dict[examples[i]["multiverseid"]]
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
__author__ = 'Dustin'

import json
import random
import numpy
import features

f = open('../data/AllCards.json', 'r')
js = json.load(f)

# train_examples = [(example, random.randint(0,1)) for example in js]
# test_examples = [(example, random.randint(0,1)) for example in js]

examples = [features.baseline_feature_extractor(js[  example]) for example in js]

print "Merging keys..."
keys = set([])
for example in examples:
    keys = keys | set(example.keys())
keys = list(keys)
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

print features.baseline_feature_extractor(js["Sen Triplets"])


print features.baseline_feature_extractor(example)
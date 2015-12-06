import json
import random
import numpy
import features
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
  if "multiverseid" in card and card["multiverseid"] in price_dict
  and card["multiverseid"] > 2000]

# unique arbitrarily on card name.  fancier methods than this didn't seem
# to help. (e.g. taking the most recent, taking the median price)
name_to_card = {card["name"]: (card, price) for card, price in card_prices}
card_prices = name_to_card.values();

# (feature_dict, price)
# feature_dict: {"feature name": feature value}
examples = [(features.feature_extractor(card), price) for card, price in card_prices]
print "Number of examples: {0}".format(len(examples))

# Shuffle the examples.  Useful for making a random train and test set later in MATLAB
random.seed(1)
random.shuffle(examples)

# create feature list
# only use features that show up on enough examples
example_threshold = 200
all_keys = [key for feature_dict, _ in examples for key, val in feature_dict.items()]
key_counts = {key:len(list(g)) for key, g in groupby(sorted(all_keys))}
key_counts_list = [(key, count) for key, count in key_counts.items()]
key_counts_list = sorted(key_counts_list, key=lambda x: -x[1])
print "number of potential features: ", len(key_counts.keys())

keys = list({key for key, count in key_counts.items() if count >= example_threshold})
print "features with enough examples: ", len(keys) 

# remove n_grams that are very similar
unique_threshold = 120
words = lambda f: {word for word in f.lstrip("ngram: ").split('_')}
indices = lambda f: {idx for idx, example in enumerate(examples) if 
  f in example[0] and example[0][f] > 0}
key_to_examples = {key: indices(key) for key in keys}
ok_keys = set()
for f1 in sorted(keys, key=len): # prefer the shorter one
  too_similar = False;
  for f2 in ok_keys: 
    if ("ngram: " in f1 and "ngram: " in f2
      and len(words(f1).intersection(words(f2))) > 0
      and len(key_to_examples[f1] - key_to_examples[f2]) < unique_threshold
      and len(key_to_examples[f2] - key_to_examples[f1]) < unique_threshold):
      too_similar = True;
 
  if not too_similar:
    ok_keys.add(f1)
keys = list(ok_keys);
print "after removing very similar ngrams:", len(keys)

print "feature names: ", keys[0:100], "..."
feature_name_file = file('../data/feature_names.txt', 'w')
print >> feature_name_file, "(intercept term)" # easier to match file with thetas
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


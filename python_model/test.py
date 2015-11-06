__author__ = 'Dustin'

import json
import random

from mtg_card_evaluator.python_model import features, sgd
from mtg_card_evaluator.model import sgd

f = open('AllCards.json', 'r')
js = json.load(f)

train_examples = [(example, random.randint(0,1)) for example in js]
test_examples = [(example, random.randint(0,1)) for example in js]

sgd.learnPredictor(train_examples, test_examples, features.baseline_feature_extractor)

for example in js:
    features.baseline_feature_extractor(js[example])

example = {
               "name" : "Sen Triplets",

           "manaCost" : "{2}{W}{U}{B}",
                "cmc" : 5,
             "colors" : ["White", "Blue", "Black"],

               "type" : "Legendary Artifact Creature Human Wizard",
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
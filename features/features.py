import sys
import itertools
from math import *
import re
import string

# FEATURE EXTRACTION
# ------------------
# feature_extractor takes in a card in json format.
# It produces a set of features based on the card, and values for each feature
# This uses both given features and feature templates.
# For example, a given feature might be "What is the cmc?" and the value would just be the cmc.
# A feature template might be "Create a new feature named after the first word in the text.  Give it a value of 1".
# The features created from the templates might be different for different cards.
# The value for all features found in other cards but not in the given card are default 0.
# Finally, some functions will not produce a feature (like if a field is missing).  This is equivalent to giving it a value of 0.

# List of meaningful words in card text (not case senstive) (See use below)
keywords = ["Deathtouch", "Defender", "Double Strike", "Enchant", "Equip", "First Strike", "Flash", "Flying", "Haste", "Hexproof", "Indestructible", "Intimidate", "Landwalk", "Lifelink", "Protection", "Reach", "Shroud", "Trample", "Vigilance", "Banding", "Rampage", "Cumulative Upkeep", "Flanking", "Phasing", "Buyback", "Shadow", "Cycling", "Echo", "Horsemanship", "Fading", "Kicker", "Flashback", "Madness", "Fear", "Morph", "Amplify", "Provoke", "Storm", "Affinity", "Entwine", "Modular", "Sunburst", "Bushido", "Soulshift", "Splice", "Offering", "Ninjutsu", "Epic", "Convoke", "Dredge", "Transmute", "Bloodthirst", "Haunt", "Replicate", "Forecast", "Graft", "Recover", "Ripple", "Split Second", "Suspend", "Vanishing", "Absorb", "Aura Swap", "Delve", "Fortify", "Frenzy", "Gravestorm", "Poisonous", "Transfigure", "Champion", "Changeling", "Evoke", "Hideaway", "Prowl", "Reinforce", "Conspire", "Persist", "Wither", "Retrace", "Devour", "Exalted", "Unearth", "Cascade", "Annihilator", "Level Up", "Rebound", "Totem Armor", "Infect", "Battle Cry", "Living Weapon", "Undying", "Miracle", "Soulbond", "Overload", "Scavenge", "Unleash", "Cipher", "Evolve", "Extort", "Fuse", "Bestow", "Tribute", "Dethrone", "Hidden Agenda", "Outlast", "Prowess", "Dash", "Exploit", "Menace", "Renown", "Awaken", "Devoid", "Ingest"]
# keywords =["Flying", "Haste"]

def feature_extractor(example):

    phi = dict()    # Will hold all {feature: value} entries to return

    # Feature template: Integer features
    # Any json field included here has an integer as a value.
    # This will produce a feature named with the field and given the corresponding value.
    # ------------------------------------
    # Example:  "cmc": 5 --> {"cmc": 5}
    integer_features_to_use = [
        "cmc",
        "power",
        "toughness",
        "multiverseid",
    ]

    # Feature template: Function features
    # This allows mixing of features with integer values.
    # ------------------------------------
    # Format: [<name of feature as string>, [<list of json fields to evaluate as strings>], <lambda function with x[i] being the value of the ith json field>]
    # Example:  ["power / (cmc + 1)", ["power", "cmc"], lambda x : x[0] / (x[1] + 1.0)] and values power = 2 and cmc = 5 --> {"power / (cmc + 1)": .3333}
    function_features_to_use = [
        # ["cmc squared", ["cmc"], lambda x : pow(x[0],2)],
        ["power / (cmc + 1)", ["power", "cmc"], lambda x : x[0] / (x[1] + 1.0)],
    ]

    # Feature template: Fancier function features
    # This allows mixing of any features given.
    # The name of the feature is just the name of all the features combined
    # If any of the feature extractors included produce a list of features, each one will be considered (cross multiplies lists of features).
    # ------------------------------------
    # Format: [[<list of feature functions given as (function, [args])], <lambda function with x[i] being the value returned from calling the ith function]
    # Note: example is automatically appended to args.
    # Example:  [[(create_integer_feature,["power"]),(length_rules_text,[]),(create_integer_feature,["cmc"])], lambda x: (x[0]*10 + x[1])/ exp(x[2])] and values power = 2, len(rules_text) = 10 and cmc = 5 --> {"power Text length cmc": 2.0}
    # NEEDS TO BE EDITED IF MORE THAN ONE OF THESE USES SAME LIST OF VARIABLES
    cross_features_to_use = [
        [[(create_integer_feature,["power"]),(length_rules_text,[]),(create_integer_feature,["cmc"])], lambda x: (x[0]*10 + x[1])/ exp(x[2])],
        [[(length_rules_text,[]),(create_integer_feature,["cmc"])], lambda x: x[0]/(x[1] + 1.0)],
    ]

    # If you write a custom feature, include it here
    # Format: phi.update(<function>(<args>)
    phi.update(number_of_keywords_in_text(example))
    phi.update(length_rules_text(example))
    phi.update(rarity_as_integer(example))
    phi.update(n_grams(1, example))

    fn = lambda x : phi.update(create_integer_feature(x, example))
    map(fn, integer_features_to_use)

    fn = lambda x : phi.update(create_function_feature(x, example))
    map(fn, function_features_to_use)

    fn = lambda x : phi.update(create_cross_feature(x, example))
    map(fn, cross_features_to_use)

    return phi

############### NON-GENERIC FEATURES FUNCTIONS ##########################

def n_grams(n, example):
    """ returns {token sequence of length <= n: # of occurences of sequence} """
    # use all attributes except ID
    example = {k:v for k,v in example.items() if not k == "id"} 

    # dump all the values together into an ascii string
    def get_ascii(val):
        if isinstance(val, unicode):
            return str(val.encode('ascii', 'ignore'))
        elif isinstance(val, dict):
            return ' '.join([get_ascii(subval) for subval in val.values()])
        elif isinstance(val, list):
            return ' '.join([get_ascii(subval) for subval in val])
        else:
            return str(val)
    all_text = get_ascii(example);
    
    # split on everything except letters
    tokens = re.sub(r'[^a-z]+',' ', all_text.lower()).split()

    # TODO: use smarter stop word filtering than just length
    tokens = [token for token in tokens if len(token) > 0]

    seqs = []
    for i in range(len(tokens)):
        seq = []
        for j in range(n):
            if i+j < len(tokens):
                seq.append(tokens[i+j])
                seqs.append('_'.join(seq))

    # return {seq: count}
    return {seq: len(list(g)) for seq, g in itertools.groupby(sorted(seqs))}

def number_of_keywords_in_text(example):
    if not "text" in example:
        return {}
    count = 0
    for keyword in keywords:
        if keyword.lower() in example["text"].lower():
            count = count + 1
    return {"# keywords in text": count + 1}

def length_rules_text(example):
    if not "text" in example:
        return {}
    return {"Text length" : len(example["text"]) + 1}

def rarity_as_integer(example):
    if not "rarity" in example:
        return {}
    rarity_dict = {"Basic Land": 1, "Common": 2, "Uncommon": 4, "Rare": 8, "Special": 16, "Mythic Rare": 20}
    if not example["rarity"] in rarity_dict:
        print example["rarity"]
        return {}
    return {"rarity as integer": rarity_dict[example["rarity"]]}


############### GENERIC FEATURES FUNCTIONS ##########################

def create_text_feature(json_key, example):
    if not json_key in example:
        return {}
    return {"{0} $ {1}".format(json_key, example[json_key].encode('ascii',errors='ignore')) : 1}

def create_text_array_feature(json_key, example):
    if not json_key in example:
        return {}
    phi = {}
    for element in example[json_key]:
        phi["{0} $ {1}".format(json_key, element.encode('ascii',errors='ignore'))] = 1
    return phi

def create_text_array_combo_feature(json_key, example):
    if not json_key in example:
        return {}
    phi = {}
    for i in range(1, len(example[json_key]) + 1):
        for combo in itertools.combinations(example[json_key], i):
            phi["{0} $ {1}".format(json_key, ' '.join(combo).encode('ascii',errors='ignore'))] = 1
    return phi

def create_field_includes_keyword_feature(field_keyword_tuple, example):
    field, keyword = field_keyword_tuple
    if not field in example:
        return {}
    if keyword.lower() in example[field].lower():
        return {"{0} in {1}".format(keyword, field): 2}
    return {"{0} in {1}".format(keyword, field): 1}

def create_boolean_feature(json_key, example):
    if not json_key in example:
        return {}
    if example[json_key]:
        return {json_key: 1}
    else:
        return {json_key: 0}

def create_integer_feature(json_key, example):
    if not json_key in example:
        return {}
    try:
        value = int(example[json_key])
    except ValueError:
        value = 10;
    return {json_key: value + 1}

def create_function_feature(fn_description, example):
    name, keys, fn = fn_description
    for key in keys:
        if not key in example:
            return {}
    try:
        x = [int(example[key]) for key in keys]
    except ValueError:
        return {}
    return {name: fn(x)}

def create_cross_feature(fn_description, example):
    feature_fn_pairs, fn = fn_description
    phis = []
    for feature_fn_pair in feature_fn_pairs:
        feature_fn, args = feature_fn_pair
        args.append(example)
        phis.append(feature_fn(*args))
    phi = {}
    for element in itertools.product(*phis):
        key = ' '.join(element)
        x = []
        for i in range(len(element)):
            x.append(phis[i][element[i]])
        phi[key] = fn(x)
    return phi

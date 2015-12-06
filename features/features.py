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
keywords = ["deathtouch", "defender", "double strike", "enchant", "equip", "first strike", "flash", "flying", "haste", "hexproof", "indestructible", "intimidate", "landwalk", "lifelink", "protection", "reach", "shroud", "trample", "vigilance", "banding", "rampage", "cumulative upkeep", "flanking", "phasing", "buyback", "shadow", "cycling", "echo", "horsemanship", "fading", "kicker", "flashback", "madness", "fear", "morph", "amplify", "provoke", "storm", "affinity", "entwine", "modular", "sunburst", "bushido", "soulshift", "splice", "offering", "ninjutsu", "epic", "convoke", "dredge", "transmute", "bloodthirst", "haunt", "replicate", "forecast", "graft", "recover", "ripple", "split second", "suspend", "vanishing", "absorb", "aura swap", "delve", "fortify", "frenzy", "gravestorm", "poisonous", "transfigure", "champion", "changeling", "evoke", "hideaway", "prowl", "reinforce", "conspire", "persist", "wither", "retrace", "devour", "exalted", "unearth", "cascade", "annihilator", "level up", "rebound", "totem armor", "infect", "battle cry", "living weapon", "undying", "miracle", "soulbond", "overload", "scavenge", "unleash", "cipher", "evolve", "extort", "fuse", "bestow", "tribute", "dethrone", "hidden agenda", "outlast", "prowess", "dash", "exploit", "menace", "renown", "awaken", "devoid", "ingest"]# keywords =["Flying", "Haste"]

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

    # Feature template: Rule features
    # This allows you to check for a rule by matching a series of text
    # WANT TO EXTEND TO ALSO INCLUDE A REGEX FOR TAPPING AND MANA SYMBOLS, and more :)
    # ------------------------------------
    # Format: [<feature name>, [<list of words substrings that must exist in order in the text,  Entering 0 searches for a number>], <lambda function with x[i] being the value of the ith 0-word]
    # Example:  ["Number of cards drawn",["draw",0,"card"], lambda x:x[0]]
    rule_template_features_to_use = [
        ["Number of cards drawn",["draw",0,"card"], lambda x:x[0]],
    ]

    # WRITE YOUR OWN FEATURE FUNCTION
    # If you write a custom feature, place it with the NON-GENERIC features below
    # Remember to call it on example and update phi here
    # -----------------------------------
    # Format: phi.update(<function>(<args>)
    phi.update(number_of_keywords_in_text(example))
    phi.update(length_rules_text(example))
    phi.update(rarity_as_integer(example))
    phi.update(n_grams(3, example))

    fn = lambda x : phi.update(create_integer_feature(x, example))
    map(fn, integer_features_to_use)

    fn = lambda x : phi.update(create_function_feature(x, example))
    map(fn, function_features_to_use)

    fn = lambda x : phi.update(create_cross_feature(x, example))
    map(fn, cross_features_to_use)

    fn = lambda x : phi.update(create_rule_template_feature(x, example))
    map(fn, rule_template_features_to_use)

    phi.update(n_lines(example))
    phi.update(n_tap(example))
    phi.update(n_untap(example))
    phi.update(n_powertoughness(example))
    phi.update(n_draw_cards(example))

    return phi


############### RULE_SPECIFIC TEXT PARSING ##############################

numerals = {"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"11":11,"12":12,"13":13,"14":14,"15":15,"16":16,"17":17,"18":18,"19":19,"20":20}
numbers = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20}

def isNumber(word):
    return word in numerals or word in numbers

def number(word):
    if word in numerals:
        return numerals[word]
    if word in numbers:
        return numbers[word]
    return False

def create_rule_template_feature(rule_template_and_fn, example):
    if not "text" in example:
        return {}
    name, rule_template, val_fn = rule_template_and_fn
    words = example["text"].split()
    i = 0
    j = 0
    val = []
    while i < len(words):
        if rule_template[j] == 0:
            if isNumber(words[i]):
                val.append(number(words[i]))
                j = j + 1
        elif rule_template[j] in words[i]:
            j = j + 1
            if j == len(rule_template):
                return {name: val_fn(val)} #success
        i = i + 1
    return {}

def n_lines(example):
    if not "text" in example:
        return {}
    return {"n_lines": len(example["text"].split('\n'))}

def n_tap(example):
    if not "text" in example:
        return {}
    return {"n_tap": example["text"].count("{T}")}

def n_untap(example):
    if not "text" in example:
        return {}
    return {"n_untap": example["text"].count("{U}")}

def n_powertoughness(example):
    if not "text" in example:
        return {}
    if not(re.match('.*\+[0-9].\+[0-9].*',example["text"]) is None):
        return {"pt": 1}
    return {}

def n_draw_cards(example):
    if not "text" in example:
        return {}
    text = example["text"]
    text = text.lower()
    if not "draw" in text:
        return {}
    if "draw a card" in text or "draws a card" in text:
        return {"n_draw_cards":1}
    if "draw that many card" in text or "draws that many card" in text:
        return {"n_draw_cards":10}
    if "draw three cards" in text:
        return {"n_draw_cards":3}
    if "draws two cards" in text or "draw two cards" in text:
        return {"n_draw_cards":2}
    if "draws x cards" in text:
        return {"n_draw_cards":10}
    # print text
    return {}

############### NON-GENERIC FEATURES FUNCTIONS ##########################

def n_grams(n, example):
    """ returns {token sequence of length <= n: # of occurences of sequence} """
    # use all attributes except ID
    example = {k:v for k,v in example.items() if 
        not k == "id"
        and not k == "flavor"}

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
    
    tokens = re.sub(r'[^a-z0-9]+',' ', all_text.lower()).split()

    tokens = [token for token in tokens]

    seqs = []
    for i in range(len(tokens)):
        seq = []
        for j in range(n):
            if i+j < len(tokens):
                seq.append(tokens[i+j])
                seqs.append('_'.join(seq))

    return {"ngram: " + seq: 1 for seq in seqs if len(seq) > 2}

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

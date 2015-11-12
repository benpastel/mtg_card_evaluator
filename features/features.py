__author__ = 'Dustin'

import sys
import itertools
from math import *

keywords = ["Deathtouch", "Defender", "Double Strike", "Enchant", "Equip", "First Strike", "Flash", "Flying", "Haste", "Hexproof", "Indestructible", "Intimidate", "Landwalk", "Lifelink", "Protection", "Reach", "Shroud", "Trample", "Vigilance", "Banding", "Rampage", "Cumulative Upkeep", "Flanking", "Phasing", "Buyback", "Shadow", "Cycling", "Echo", "Horsemanship", "Fading", "Kicker", "Flashback", "Madness", "Fear", "Morph", "Amplify", "Provoke", "Storm", "Affinity", "Entwine", "Modular", "Sunburst", "Bushido", "Soulshift", "Splice", "Offering", "Ninjutsu", "Epic", "Convoke", "Dredge", "Transmute", "Bloodthirst", "Haunt", "Replicate", "Forecast", "Graft", "Recover", "Ripple", "Split Second", "Suspend", "Vanishing", "Absorb", "Aura Swap", "Delve", "Fortify", "Frenzy", "Gravestorm", "Poisonous", "Transfigure", "Champion", "Changeling", "Evoke", "Hideaway", "Prowl", "Reinforce", "Conspire", "Persist", "Wither", "Retrace", "Devour", "Exalted", "Unearth", "Cascade", "Annihilator", "Level Up", "Rebound", "Totem Armor", "Infect", "Battle Cry", "Living Weapon", "Undying", "Miracle", "Soulbond", "Overload", "Scavenge", "Unleash", "Cipher", "Evolve", "Extort", "Fuse", "Bestow", "Tribute", "Dethrone", "Hidden Agenda", "Outlast", "Prowess", "Dash", "Exploit", "Menace", "Renown", "Awaken", "Devoid", "Ingest"]
# keywords =["Flying", "Haste"]

def empty_feature_extractor(example):

    phi = dict()
    return phi

def baseline_feature_extractor(example):

    phi = dict()

    text_features_to_use = [
        # Name of feature function
        # "name",
        # "manaCost",
        # "type",
        # "rarity",
        # "text",
        # "flavor",
        # "artist",
        # "number",
        # "power",
        # "toughness",
        # "layout",
        # "imageName",
        # "id",
        # "imageName",
        # "watermark",
        # "border",
        # "releaseDate",
    ]

    boolean_features_to_use = [
        # "timeshifted",
        # "reversed",
        # "starter",
    ]

    text_array_features_to_use = [
        # "colors",
        # "supertypes",
        # "types",
        # "subtypes",
    ]

    text_array_combo_features_to_use = [
        # "colors",
        # "supertypes",
        # "types",
        # "subtypes",
    ]

    integer_features_to_use = [
        "cmc",
        # "number",
        "power",
        "toughness",
        # "loyalty",
        # "hand",
        # "life",
        "multiverseid",
    ]

    integer_array_features_to_use = [
        # "variations",
    ]

    function_features_to_use = [
        # ["cmc squared", ["cmc"], lambda x : pow(x[0],2)],
        ["power / cmc", ["power", "cmc"], lambda x : x[0] / (x[1] + 1.0)],
    ]

    cross_features_to_use = [
        # [[(create_text_feature, ["toughness"]),(create_text_array_feature, ["colors"]),(create_integer_feature, ["cmc"])], lambda x : x[0]*x[1]*x[2]],
        [[(create_integer_feature,["power"]),(length_rules_text,[]),(create_integer_feature,["cmc"])], lambda x: (x[0]*10 + x[1])/ exp(x[2])],
        [[(length_rules_text,[]),(create_integer_feature,["cmc"])], lambda x: x[0]/(x[1] + 1.0)],
    ]

    field_includes_keyword_to_use = [
        # ("text", keyword) for keyword in keywords
    ]

    phi.update(number_of_keywords_in_text(example))
    phi.update(length_rules_text(example))
    phi.update(rarity_as_integer(example))

    mod = sys.modules[__name__]
    fn = lambda x : phi.update(create_text_feature(x, example))
    map(fn, text_features_to_use)

    fn = lambda x : phi.update(create_boolean_feature(x, example))
    map(fn, boolean_features_to_use)

    fn = lambda x : phi.update(create_text_array_feature(x, example))
    map(fn, text_array_features_to_use)

    fn = lambda x : phi.update(create_text_array_combo_feature(x, example))
    map(fn, text_array_combo_features_to_use)

    fn = lambda x : phi.update(create_integer_feature(x, example))
    map(fn, integer_features_to_use)

    fn = lambda x : phi.update(create_integer_array_feature(x, example))
    map(fn, integer_array_features_to_use)

    fn = lambda x : phi.update(create_function_feature(x, example))
    map(fn, function_features_to_use)

    fn = lambda x : phi.update(create_cross_feature(x, example))
    map(fn, cross_features_to_use)

    fn = lambda x : phi.update(create_field_includes_keyword_feature(x, example))
    map(fn, field_includes_keyword_to_use)

    return phi

###############

def number_of_keywords_in_text(example):
    if not "text" in example:
        return {}
    count = 0
    for keyword in keywords:
        if keyword.lower() in example["text"].lower():
            count = count + 1
    return {"# keywords in text": count + 1}

def create_field_includes_keyword_feature(field_keyword_tuple, example):
    field, keyword = field_keyword_tuple
    if not field in example:
        return {}
    if keyword.lower() in example[field].lower():
        return {"{0} in {1}".format(keyword, field): 2}
    return {"{0} in {1}".format(keyword, field): 1}

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

def create_integer_array_feature(json_key, example):
    if not json_key in example:
        return {}
    phi = {}
    for i in range(len(example[json_key])):
        try:
            value = int(example[json_key][i])
        except ValueError:
            continue
        phi["{0} ({1})".format(json_key, i)] = value
    return phi



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
__author__ = 'Dustin'

import sys
import itertools

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
        # "rarity", #Nothing has rarity in AllCards.json
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
        # ["toughness + power - cmc", ["toughness", "power", "cmc"], lambda x : x[0] + x[1] - x[2]],
    ]

    cross_features_to_use = [
        # [[(create_text_feature, "toughness"),(create_text_array_feature, "colors"),(create_integer_feature, "cmc")], lambda x : x[0]*x[1]*x[2]],
    ]

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

    return phi

###############

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
        # value = 10;
        return {};
    return {json_key: value}

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
        feature_fn, json_key = feature_fn_pair
        phis.append(feature_fn(json_key, example))
    phi = {}
    for element in itertools.product(*phis):
        key = ' '.join(element)
        x  = []
        for i in range(len(element)):
            x.append(phis[i][element[i]])
        phi[key] = fn(x)
    return phi
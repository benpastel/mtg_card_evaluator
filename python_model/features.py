__author__ = 'Dustin'

import sys

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
        "rarity",
        # "text",
        # "flavor",
        # "artist",
        # "number",
        "power",
        "toughness",
        # "layout",
        # "imageName",
        # "id",
        # "imageName",
        # "watermark",
        # "border",
        # "releaseDate",
    ]

    boolean_features_to_use = [
        "timeshifted",
        "reversed",
        "starter",
    ]

    text_array_features_to_use = [
        "colors",
        "supertypes",
        "types",
        "subtypes",
    ]

    integer_features_to_use = [
        "cmc",
        "number",
        "power",
        "toughness",
        "loyalty",
        "hand",
        "life",
    ]

    integer_array_features_to_use = [
        # "variations",
    ]

    pair_features = [
        # [create_text_feature, "name", create_text_feature, "manaCost"],
    ]

    mod = sys.modules[__name__]
    fn = lambda x : phi.update(create_text_feature(x, example))
    map(fn, text_features_to_use)

    fn = lambda x : phi.update(create_boolean_feature(x, example))
    map(fn, boolean_features_to_use)

    fn = lambda x : phi.update(create_text_array_feature(x, example))
    map(fn, text_array_features_to_use)

    fn = lambda x : phi.update(create_integer_feature(x, example))
    map(fn, integer_features_to_use)

    fn = lambda x : phi.update(create_integer_array_feature(x, example))
    map(fn, integer_array_features_to_use)

    fn = lambda x : phi.update(create_pair_feature(x, example))
    map(fn, pair_features)

    return phi

def create_pair_feature(fn_names, example):
    phi = {}
    feature1, json_key1, feature2, json_key2 = fn_names
    phi1 = feature1(json_key1, example)
    phi2 = feature2(json_key2, example)
    for key1 in phi1:
        for key2 in phi2:
            phi["pair({0}, {1})".format(key1, key2)] = phi1[key1] * phi2[key2]
    return phi

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
        return {}
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
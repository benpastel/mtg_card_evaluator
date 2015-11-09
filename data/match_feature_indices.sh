# match price data with features
# parses json with 'jq' from https://stedolan.github.io/jq/

# (1) get (name, multiverseid) from AllSets
cat AllSets.json | jq ' .[]."cards" | .[]."name" ' > names &&
cat AllSets.json | jq ' .[]."cards" | .[]."multiverseid" ' > ids && 
paste -d'$' names ids | grep -v 'null' | sort > name_id && 
rm names ids

# (2) get (name, line) from AllCards.json
#
# line numbers are indices into the feature array, if the feature generation
# is working correctly
cat AllCards.json | jq '.[]."name"' | awk '{print $0 "$" NR}' | sort > name_line

# (3) match
join -t'$' name_id name_line > name_id_line &&
rm name_id name_line

# (4) format for matlab 
cat name_id_line | cut -d'$' -f2 -f3 | tr '$' ' ' > id_featureidx.dat && 
rm name_id_line

# criteria is the where clause specifying characteristics of features (e.g. volume > 10 and time_signature = 4)
# returns the following query (string):
#   SELECT select_features
#   FROM table
#   WHERE track_id IN (SELECT track_id FROM

def get_features(where_clause, table, select_features):
    feature_query = 'SELECT track_id, '
    for feature in select_features:
        feature_query += feature + ', '
    feature_query += 'year FROM ' + table + ' WHERE ' + where_clause
    return feature_query


def get_lyrics (where_clause, table):
    myQuery = 'SELECT word FROM ' + table + ' WHERE ' + where_clause
    return myQuery


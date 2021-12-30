import sqlite3
import pandas as pd

def data_from_sql(path):
    con = sqlite3.connect(path)

    df_user = pd.read_sql("SELECT * from user", con)
    df_ascent = pd.read_sql("SELECT * from ascent", con)
    df_grade = pd.read_sql("SELECT * from grade", con)

    return df_user, df_ascent, df_grade

def preprocess_users(df_user):
    # change countries with less than 100 entries to OTH (other)
    country_values = df_user['country'].value_counts()
    bool_df = country_values[df_user['country']] < 100
    df_user.loc[bool_df.values] = 'OTH'

    # remove users with empty started, height, or weight rows
    df_user = df_user.drop(df_user[(df_user['started'] == 0) | (df_user['height'] == 0) | (df_user['weight'] == 0)].index)
    df_user = df_user.drop(['occupation', 'first_name', 'last_name', 'city', 'competitions', 'sponsor1', 'sponsor2', 'sponsor3', 'best_area', 'worst_area', 'guide_area', 'interests', 'birth', 'presentation', 'deactivated', 'anonymous'], axis=1)
    return df_user

def preprocess_ascents(df_ascent, df_grade):

    # preprocess df_grade to be used in df_ascents transformations
    def standardize_usa_boulder_ratings(row):
        """Group and standardize V-scale ratings"""
        rating = row.usa_boulders
        if rating == 'VB':
            rating = 'V0-'
        elif rating == 'V3/4':
            rating = 'V3'
        elif rating == 'V4/V5':
            rating = 'V4'
        elif rating == 'V5/V6':
            rating = 'V5'
        elif rating == 'V8/9':
            rating = 'V8'
        row.usa_boulders = rating
        
        return row
    
    df_grade_processed = (
        df_grade
        .loc[df_grade.usa_boulders != '', :] # filter for climbs with V-scale ratings 
        .apply(standardize_usa_boulder_ratings, axis=1)  # group and standardize V-scale ratings
    )

    df_ascent_processed = df_ascent.loc[df_ascent.climb_type == 1, :] # filter for bouldering climbs

    # Merge and filter ascent + grade data to create interim dataset
    df_interim = (
        df_ascent_processed
        .merge(df_grade_processed, how='inner', left_on='grade_id', right_on='id', suffixes=('_ascent', '_grade'))
        .loc[:, ['id_ascent', 'id_grade', 'user_id', 'date', 'year', 'usa_boulders', 'name']]  # select relevant columns for project
        .sort_values(by=['user_id', 'date'])
        .reset_index(drop=True)   
    )

    def v_to_int(row):
        """Convert V-scale ratings into integers, mass grouping all ratings after and including 10."""
        rating = row.usa_boulders
        if rating == 'V0-':
            rating = 0
        elif rating == 'V0':
            rating = 0
        elif rating == 'V1':
            rating = 1
        elif rating == 'V2':
            rating = 2
        elif rating == 'V3':
            rating = 3
        elif rating == 'V4':
            rating = 4
        elif rating == 'V5':
            rating = 5
        elif rating == 'V6':
            rating = 6
        elif rating == 'V7':
            rating = 7
        elif rating == 'V8':
            rating = 8
        elif rating == 'V9':
            rating = 9
        else:
            rating = 10
        row.usa_boulders = rating
        return row

    # convert V-scale ratings to integers in df_interim
    df_interim = df_interim.apply(v_to_int, axis=1)

    # next you need a table of each user's earliest highest ascent
    earliest_ascents = []
    for id in df_interim['user_id'].unique():
        id_climbs = df_interim[df_interim['user_id'] == id]
        id_max = id_climbs['usa_boulders'].max()
        id_climbs_maxes = id_climbs[id_climbs['usa_boulders'] == id_max]
        id_climbs_maxes_earliest = id_climbs_maxes[id_climbs_maxes['year'] == id_climbs_maxes['year'].min()]
        if isinstance(id_climbs_maxes_earliest, pd.DataFrame): # take the first entry of their earliest highest ascent
            id_climbs_maxes_earliest = id_climbs_maxes_earliest.iloc[0]
        assert isinstance(id_climbs_maxes_earliest, pd.Series)
        earliest_ascents.append(id_climbs_maxes_earliest)
    ea_frame = pd.DataFrame(earliest_ascents)
    
    return ea_frame

def merge_user_ascents(df_user, ea_frame):
    """merges user and ascents, creating the 'difference' column and dropping unnecessary ones."""
    new_frame = df_user.merge(ea_frame, left_on='id', right_on='user_id')
    new_frame = new_frame.drop(['date', 'name', 'user_id', 'id', 'id_ascent', 'id_grade'], axis=1)

    dummies = pd.get_dummies(new_frame['country'])
    difference = new_frame['year'] - new_frame['started']
    for (idx, val) in difference.iteritems():
        if val < 0:
            difference[idx] = 0
        if val > 50:
            difference[idx] = 50
    data = pd.concat([dummies, difference, new_frame], axis=1).drop(['country', 'started', 'year'], axis=1)
    data = data.rename(columns={0: 'difference'})

    return data


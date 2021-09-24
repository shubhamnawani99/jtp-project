import pandas as pd
# Pearson correlation
from scipy.stats import pearsonr

from .db import get_db

# Constants
SCORE_LIMIT = 3
MUTUAL_USERS_LIMIT = 100
TOP_USERS_LIMIT = 50
RECOMMENDATION_LIMIT = 10


def compute_similarity(top_users, new_user):
    pearson_corr = {}
    for user_id, features in top_users:
        # Books should be sorted
        features = features.sort_values(by='book_id')
        features_list = features['book_id'].values

        new_user_ratings = new_user[new_user['book_id'].isin(features_list)]['rating'].values
        user_ratings = features[features['book_id'].isin(features_list)]['rating'].values

        # the ratings (Lists) in comparison should have at least 2 values.
        if len(new_user_ratings) > 1:
            corr = pearsonr(new_user_ratings, user_ratings)
            pearson_corr[user_id] = corr[0]

    return pearson_corr


def get_grouped_ratings(users_rating):
    # Calculate sum of similarity index and weighted rating for each book
    # higher the sum of weighted ratings => more users have read the same book
    # higher the sum of similarity index => number of users that have read and liked the book as much as you
    group = users_rating.groupby('book_id')

    # we only select those books, which have at least 3 ratings by different users
    # this is done so that, we get more diverse scores and we don't get
    # books recommended by a single user
    ratings_mask = group.count()['user_id'] < 2

    # if the number of mutual users are less
    if len(ratings_mask.index) == 0:
        ratings_mask = group.count()['user_id'] > 0

    # using the mask, we calculate the sum of weighted ratings and sim indices
    # of all the books and drop the single ratings
    grouped_ratings = group.sum()[['similarity_index', 'weighted_rating']].mask(ratings_mask).dropna()

    return grouped_ratings


def get_recommendations_from_score(grouped_ratings: pd.DataFrame) -> pd.DataFrame:
    # Create a new dataframe to store our average recommendation score
    recommend_books = pd.DataFrame()
    # Calculate the average recommendation score
    recommend_books['avg_recommend_score'] = grouped_ratings['weighted_rating'] / grouped_ratings['similarity_index']
    # Fix the dataframe
    recommend_books['book_id'] = grouped_ratings.index
    recommend_books = recommend_books.reset_index(drop=True)
    # Return books with the high scores
    return recommend_books[(recommend_books['avg_recommend_score'] > SCORE_LIMIT)]


def get_recommendations(books_df, result_df, recommend_books):
    # get the general overall user-recommendations
    user_recommendation = books_df[books_df['book_id'].isin(recommend_books['book_id'])][['authors', 'title']].sample(
        RECOMMENDATION_LIMIT, replace=True).drop_duplicates().to_dict('records')

    # get the list of all the genre generated
    genre_chosen = result_df.groupby(by='tag_name').size().sort_values()[-3:].reset_index()['tag_name'].to_list()

    filtered_recommendations = []
    if len(genre_chosen) == 3:
        # Top Recommendations for each top-3 genre
        for i in range(3):
            filtered_df = result_df[result_df['tag_name'] == genre_chosen[i]] \
                .sample(RECOMMENDATION_LIMIT, replace=True).drop_duplicates().to_dict('records')
            filtered_recommendations.append(filtered_df)

    return user_recommendation, filtered_recommendations


def collaborative_filtering(user, ratings_df, books_df, books_df_with_genres):
    # Create dataframe for new user (me)
    user = pd.DataFrame(columns=['title', 'rating'], data=user.items())

    # Add book_id from books_df
    new_user = pd.merge(user, books_df, on='title', how='inner')
    new_user = new_user[['book_id', 'title', 'rating']].sort_values(by='book_id')

    # calculate the ratings of other users that have read the same books as me
    other_users = ratings_df[ratings_df['book_id'].isin(new_user['book_id'].values)]

    # Sort users by count of most mutual books with me
    # The higher the user in the table, the more mutual books I have with that user
    users_mutual_books = other_users.groupby(['user_id'])
    users_mutual_books = sorted(users_mutual_books, key=lambda x: len(x[1]), reverse=True)

    # Get the top 100 mutual users
    top_users = users_mutual_books[:MUTUAL_USERS_LIMIT]

    # Initialize the pearson correlation
    pearson_corr = compute_similarity(top_users=top_users, new_user=new_user)

    # Get top50 users with the highest similarity indices
    pearson_df = pd.DataFrame(columns=['user_id', 'similarity_index'], data=pearson_corr.items()).dropna()
    pearson_df = pearson_df.sort_values(by='similarity_index', ascending=False)[:TOP_USERS_LIMIT]

    # Get all books for these users and add weighted book's ratings
    users_rating = pearson_df.merge(ratings_df, on='user_id', how='inner')
    users_rating['weighted_rating'] = users_rating['rating'] * users_rating['similarity_index']

    # Get the grouped ratings
    grouped_ratings = get_grouped_ratings(users_rating=users_rating)

    # Get the top recommended book_ids, based on average recommend score
    recommend_books = get_recommendations_from_score(grouped_ratings=grouped_ratings)

    result_df = books_df_with_genres[books_df_with_genres['book_id'].isin(recommend_books['book_id'])][
        ['authors', 'title', 'book_id', 'tag_name']]

    # return the final user and filtered recommendations
    return get_recommendations(books_df=books_df, result_df=result_df, recommend_books=recommend_books)


def check_ratings(user_selections):
    temp = user_selections
    ratings_len = len(set(user_selections.values()))
    if ratings_len == 1:
        for title in temp.keys():
            user_selections[title] = (len(title) % 5) + 1
    return user_selections


def main(user_selections: dict):
    # get the database instance
    db = get_db()

    # create the dataframes
    books_df = pd.read_sql_query("SELECT * FROM books", db)
    ratings_df = pd.read_sql_query("SELECT * FROM ratings", db)
    books_df_with_genres = pd.read_sql_query("SELECT * FROM books_with_genres", db)

    # check for same ratings
    user_selections = check_ratings(user_selections)

    print('USER SELECTIONS', user_selections)

    # run the recommendation system
    user_recommendation, filtered_recommendations = collaborative_filtering(user_selections, ratings_df, books_df,
                                                                            books_df_with_genres)

    # return the recommendations
    return user_recommendation, filtered_recommendations


# Main driver
if __name__ == "__main__":
    main()

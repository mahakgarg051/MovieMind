import streamlit as st
import pandas as pd
import joblib

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Movie Mind",
    page_icon="🎬",
    layout="wide"
)

# ==============================
# LOAD SAVED MODEL
# ==============================
@st.cache_resource
def load_model():
    return joblib.load("movie_recommender_model.pkl")

model_data = load_model()

train_matrix = model_data["train_matrix"]
train_user_clusters = model_data["train_user_clusters"]
train_similarity_df = model_data["train_similarity_df"]
train_df = model_data["train_df"]


# ==============================
# RECOMMENDATION FUNCTION
# ==============================
def recommend_movies(user_id, n=5):

    if user_id not in train_matrix.index:
        return pd.DataFrame()

    # Find target user's cluster
    target_cluster = train_user_clusters[
        train_user_clusters["User_ID"] == user_id
    ]["Cluster"].iloc[0]

    # Users in same cluster
    cluster_users = train_user_clusters[
        train_user_clusters["Cluster"] == target_cluster
    ]["User_ID"].tolist()

    # Similarity inside cluster
    similarities = train_similarity_df.loc[
        user_id,
        cluster_users
    ].drop(user_id, errors="ignore")

    # Top similar users
    similar_users = similarities.sort_values(
        ascending=False
    ).head(10)

    recommendation_data = []

    for similar_user, similarity_score in similar_users.items():

        ratings = train_df[
            train_df["User_ID"] == similar_user
        ]

        for _, row in ratings.iterrows():

            recommendation_data.append({
                "Movie_ID": row["Movie_ID"],
                "Movie_Title": row["Movie_Title"],
                "Rating": row["Rating"],
                "Similarity": similarity_score
            })

    recommendation_df = pd.DataFrame(
        recommendation_data
    )

    if recommendation_df.empty:
        return recommendation_df

    # Weighted recommendation score
    recommendation_df["Weighted_Score"] = (
        recommendation_df["Rating"] *
        recommendation_df["Similarity"]
    )

    # Remove movies already watched/rated
    already_rated = set(
        train_df[
            train_df["User_ID"] == user_id
        ]["Movie_ID"]
    )

    recommendation_df = recommendation_df[
        ~recommendation_df["Movie_ID"].isin(already_rated)
    ]

    # Final recommendations
    final_recommendations = (
        recommendation_df
        .groupby(
            ["Movie_ID", "Movie_Title"],
            as_index=False
        )["Weighted_Score"]
        .mean()
        .sort_values(
            "Weighted_Score",
            ascending=False
        )
        .head(n)
    )

    return final_recommendations


# ==============================
# MOVIE MIND WEBSITE
# ==============================

st.title("🎬 Movie Mind")

st.markdown(
    "### Discover movies that match your taste"
)

st.write(
    "Personalized recommendations powered by "
    "K-Means Clustering + Cosine Similarity."
)

st.divider()


# ==============================
# USER SELECTION
# ==============================

user_ids = sorted(
    train_matrix.index.tolist()
)

selected_user = st.selectbox(
    "👤 Select User",
    user_ids
)

number_of_movies = st.selectbox(
    "🎯 Number of Recommendations",
    [5, 10]
)


# ==============================
# RECOMMENDATION BUTTON
# ==============================

if st.button(
    "✨ Get My Recommendations",
    use_container_width=True
):

    recommendations = recommend_movies(
        selected_user,
        number_of_movies
    )

    if recommendations.empty:

        st.warning(
            "No recommendations available for this user."
        )

    else:

        st.subheader(
            "🍿 Recommended Movies For You"
        )

        for i, (_, movie) in enumerate(
            recommendations.iterrows(),
            start=1
        ):

            col1, col2, col3 = st.columns(
                [1, 5, 2]
            )

            with col1:
                st.write(f"### {i}")

            with col2:
                st.write(
                    f"### {movie['Movie_Title']}"
                )

                st.caption(
                    f"Movie ID: {movie['Movie_ID']}"
                )

            with col3:
                st.metric(
                    "Score",
                    f"{movie['Weighted_Score']:.2f}"
                )

            st.divider()
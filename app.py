import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import re
import base64


# ============================================================
# PAGE CONFIGURATION (MOBILE OPTIMIZED)
# ============================================================

st.set_page_config(
    page_title="Movie Mind - Netflix + IMDb AI Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PROJECT PATHS & DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "movie_recommender_model.pkl"
ASSETS_DIR = BASE_DIR / "assets"
POSTERS_DIR = ASSETS_DIR / "posters"

IMAGE_DIRECTORIES = [
    POSTERS_DIR,
    ASSETS_DIR,
    BASE_DIR / "images",
    BASE_DIR / "posters",
    BASE_DIR / "movie_posters",
    BASE_DIR / "movie_images"
]


# ============================================================
# EXACT MOVIE POSTER MAPPING
# ============================================================

POSTER_MAP = {
    "Beyond the Stars": POSTERS_DIR / "beyond_the_stars.png",
    "Broken Roads": POSTERS_DIR / "broken_roads.png",
    "Campus Days": POSTERS_DIR / "campus_days.png",
    "City Lights": POSTERS_DIR / "city_lights.png",
    "Code Breaker": POSTERS_DIR / "code_breaker.png",
    "Digital Age": POSTERS_DIR / "digital_age.png",
    "Dream Maker": POSTERS_DIR / "dream_maker.png",
    "Dream Makers": POSTERS_DIR / "dream_makers.png",
    "Final Verdict": POSTERS_DIR / "final_verdict.png",
    "Future World": POSTERS_DIR / "future_world.png",
    "Hidden Truth": POSTERS_DIR / "hidden_truth.png",
    "Love in Winter": POSTERS_DIR / "love_in_winter.png",
    "Midnight Chase": POSTERS_DIR / "midnight_chase.png",
    "Ocean Quest": POSTERS_DIR / "ocean_quest.png",
    "Parallel Lives": POSTERS_DIR / "parallel_lives.png",
    "Secret Agent": POSTERS_DIR / "secret_agent.png",
    "Shadow Hunter": POSTERS_DIR / "shadow_hunter.png",
    "The Last Mission": POSTERS_DIR / "the_last_mission.png",
    "The Lost Kingdom": POSTERS_DIR / "the_lost_kingdom.png",
    "The Silent House": POSTERS_DIR / "the_silent_house.png",
    "Wild Frontier": POSTERS_DIR / "wild_frontier.png"
}


# ============================================================
# ASSET ENCODING & HELPER FUNCTIONS
# ============================================================

def get_image_base64(path):
    """
    Safely loads an image file and converts it into a base64 data URI string.
    """
    p = Path(path)
    if p.exists() and p.is_file():
        try:
            suffix = p.suffix.lower().replace(".", "")
            mime = "jpeg" if suffix in ["jpg", "jpeg"] else suffix
            b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
            return f"data:image/{mime};base64,{b64}"
        except Exception:
            return ""
    return ""


# Preload brand visual assets
LOGO_BASE64 = get_image_base64(ASSETS_DIR / "logo_icon_transparent.png") or get_image_base64(ASSETS_DIR / "logo_icon.png")
PROJECTOR_BASE64 = get_image_base64(ASSETS_DIR / "projector_banner.png") or get_image_base64(ASSETS_DIR / "projector.png")
DREAM_CARD_BASE64 = get_image_base64(ASSETS_DIR / "dream_card.png")
GREAT_MOVIES_BASE64 = get_image_base64(ASSETS_DIR / "great_movies_trans.png") or get_image_base64(ASSETS_DIR / "great_movies.png")


# ============================================================
# RESPONSIVE CSS - DESKTOP & MOBILE OPTIMIZED
# ============================================================

st.markdown(
    """<style>
/* Google Fonts: Poppins & Inter */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&family=Caveat:wght@600;700&display=swap');

*, *::before, *::after {
    box-sizing: border-box !important;
}

html, body {
    overflow-x: hidden !important;
    max-width: 100vw !important;
    margin: 0;
    padding: 0;
}

.stApp {
    font-family: 'Poppins', 'Inter', -apple-system, sans-serif;
    background:
        radial-gradient(ellipse at 85% 10%, rgba(147, 51, 234, 0.22) 0%, rgba(236, 72, 153, 0.12) 32%, transparent 65%),
        radial-gradient(circle at 10% 80%, rgba(236, 72, 153, 0.12) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.6) 0%, transparent 100%),
        #080914;
    color: #f1f5f9;
    overflow-x: hidden !important;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1380px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #090c1a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    width: 280px !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.4rem;
    padding-left: 1.1rem;
    padding-right: 1.1rem;
}

/* Touch-friendly inputs */
div[data-baseweb="select"] > div {
    background-color: #111528 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    min-height: 48px !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: rgba(236, 72, 153, 0.6) !important;
    box-shadow: 0 0 12px rgba(236, 72, 153, 0.2) !important;
}

div[data-baseweb="select"] * {
    color: #ffffff !important;
    font-weight: 500 !important;
}

div[data-baseweb="popover"] > div,
div[data-baseweb="menu"] {
    background-color: #111528 !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
    border-radius: 12px !important;
}

div[data-baseweb="menu"] li {
    color: #cbd5e1 !important;
    min-height: 42px !important;
    display: flex !important;
    align-items: center !important;
}

div[data-baseweb="menu"] li:hover {
    background-color: rgba(168, 85, 247, 0.25) !important;
    color: #ffffff !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #ec4899 0%, #a855f7 50%, #3b82f6 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    min-height: 48px !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.45) !important;
    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 28px rgba(236, 72, 153, 0.65) !important;
    color: #ffffff !important;
}

/* Headings */
h1, h2, h3, h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Hero Banner */
.hero-banner {
    position: relative;
    background: linear-gradient(135deg, rgba(18, 24, 52, 0.75) 0%, rgba(10, 13, 28, 0.85) 100%);
    border: 1px solid rgba(168, 85, 247, 0.22);
    border-radius: 20px;
    padding: 24px 32px;
    margin-bottom: 22px;
    overflow: hidden;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.5);
    width: 100%;
}

.hero-projector-wrap {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    z-index: 1;
}

/* Statistics Cards */
.stat-card {
    background: rgba(15, 19, 38, 0.72);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.35);
    width: 100%;
}

.stat-card:hover {
    transform: translateY(-3px) scale(1.015);
    border-color: rgba(168, 85, 247, 0.45);
    box-shadow: 0 10px 28px rgba(168, 85, 247, 0.22);
}

.stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}

.icon-movies {
    background: linear-gradient(135deg, #ec4899, #be185d);
    box-shadow: 0 0 16px rgba(236, 72, 153, 0.45);
}

.icon-clusters {
    background: linear-gradient(135deg, #a855f7, #7c3aed);
    box-shadow: 0 0 16px rgba(168, 85, 247, 0.45);
}

.icon-method {
    background: linear-gradient(135deg, #06b6d4, #0284c7);
    box-shadow: 0 0 16px rgba(6, 182, 212, 0.45);
}

.icon-rating {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    box-shadow: 0 0 16px rgba(245, 158, 11, 0.45);
}

/* Selected Movie Hero Card */
.selected-movie-card {
    background: rgba(16, 20, 42, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(168, 85, 247, 0.25);
    border-radius: 20px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 26px;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45);
    width: 100%;
}

.selected-poster-img {
    width: 200px;
    height: 165px;
    object-fit: cover;
    border-radius: 14px;
    border: 1px solid rgba(168, 85, 247, 0.35);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.55);
    flex-shrink: 0;
}

/* IMDb Chip */
.imdb-chip {
    background: #f5c518;
    color: #000000;
    font-weight: 800;
    font-size: 11.5px;
    padding: 3px 8px;
    border-radius: 5px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(245, 197, 24, 0.4);
}

/* Circular Rating Badge */
.circular-rating-badge {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(15, 20, 40, 0.85);
    border: 2.5px solid #f5c518;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 14px rgba(245, 197, 24, 0.4);
    flex-shrink: 0;
}

/* Metadata Badges */
.netflix-badge {
    padding: 4px 10px;
    border-radius: 7px;
    font-size: 11px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    letter-spacing: 0.3px;
}

.badge-genre {
    background: rgba(168, 85, 247, 0.16);
    color: #d8b4fe;
    border: 1px solid rgba(168, 85, 247, 0.32);
}

.badge-lang {
    background: rgba(6, 182, 212, 0.16);
    color: #67e8f9;
    border: 1px solid rgba(6, 182, 212, 0.32);
}

.badge-year {
    background: rgba(236, 72, 153, 0.16);
    color: #f472b6;
    border: 1px solid rgba(236, 72, 153, 0.32);
}

.badge-runtime {
    background: rgba(16, 185, 129, 0.16);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.32);
}

/* Movie Information Panel */
.movie-info-panel {
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 12px 16px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 12px;
    margin-top: 14px;
    width: 100%;
}

.movie-info-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

/* Recommendation Card */
.rec-card {
    position: relative;
    background: linear-gradient(145deg, rgba(18, 22, 46, 0.8) 0%, rgba(12, 15, 32, 0.85) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    transition: all 0.32s cubic-bezier(0.25, 0.8, 0.25, 1);
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow: hidden;
    width: 100%;
}

.rec-card:hover {
    transform: translateY(-5px) scale(1.025);
    border-color: rgba(236, 72, 153, 0.55);
    box-shadow: 0 14px 34px rgba(236, 72, 153, 0.28), 0 0 18px rgba(168, 85, 247, 0.25);
}

.rec-poster-img {
    width: 100%;
    height: 140px;
    object-fit: cover;
    border-radius: 10px;
    border: 1px solid rgba(168, 85, 247, 0.35);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    display: block;
}

.rec-card-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: linear-gradient(90deg, #ec4899, #a855f7);
    color: #ffffff;
    font-size: 9px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    letter-spacing: 0.4px;
    box-shadow: 0 2px 10px rgba(236, 72, 153, 0.4);
    z-index: 2;
}

/* How It Works Card */
.how-it-works-card {
    background: rgba(16, 20, 42, 0.75);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 22px 24px;
    height: 100%;
    box-shadow: 0 10px 32px rgba(0, 0, 0, 0.4);
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
}

.step-pill {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 7px 0;
    font-size: 13px;
    font-weight: 500;
    color: #d1d5db;
}

.step-badge {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    color: white;
    flex-shrink: 0;
}

/* Popular Movie Card */
.pop-card {
    background: rgba(14, 18, 38, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.25s ease;
    width: 100%;
}

.pop-card:hover {
    border-color: rgba(236, 72, 153, 0.45);
    transform: translateY(-2px);
}

.pop-poster-img {
    width: 58px;
    height: 48px;
    object-fit: cover;
    border-radius: 7px;
    flex-shrink: 0;
}


/* ============================================================
   MOBILE RESPONSIVE OVERRIDES (max-width: 768px)
   ============================================================ */

@media (max-width: 768px) {
    /* Full mobile width with minimal side padding */
    .block-container {
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
        padding-top: 0.8rem !important;
        padding-bottom: 2rem !important;
        max-width: 100vw !important;
    }

    /* Force all Streamlit columns to stack vertically on mobile */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
        margin-bottom: 12px !important;
    }

    /* Smaller responsive headings */
    h1 {
        font-size: 26px !important;
    }
    h2 {
        font-size: 20px !important;
    }
    h3 {
        font-size: 17px !important;
    }

    /* Hero section: stack on phones */
    .hero-banner {
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
        padding: 18px 14px !important;
        gap: 14px !important;
    }

    .hero-banner > div:first-child {
        align-items: center !important;
    }

    .hero-projector-wrap {
        display: none !important;
    }

    /* Selected Movie Card: Stack vertically */
    .selected-movie-card {
        flex-direction: column !important;
        padding: 16px 14px !important;
        gap: 16px !important;
        text-align: center !important;
    }

    .selected-poster-img {
        width: 100% !important;
        max-width: 290px !important;
        height: 180px !important;
        margin: 0 auto !important;
    }

    .selected-movie-card > div:nth-child(2) {
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    /* Badges wrap neatly and center on mobile */
    .selected-movie-card .netflix-badge {
        font-size: 10px !important;
        padding: 4px 8px !important;
    }

    .movie-info-panel {
        grid-template-columns: 1fr 1fr !important;
        gap: 8px !important;
        text-align: left !important;
    }

    /* Recommendation card: single column, larger touch-friendly poster */
    .rec-card {
        padding: 14px !important;
        margin-bottom: 14px !important;
    }

    .rec-poster-img {
        height: 190px !important;
    }

    /* Full-width tap button */
    div.stButton > button {
        width: 100% !important;
        min-height: 50px !important;
        font-size: 16px !important;
    }

    /* Statistics cards */
    .stat-card {
        padding: 14px 16px !important;
        margin-bottom: 8px !important;
    }
}
</style>""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL & COMPONENTS (UNCHANGED ML LOGIC)
# ============================================================

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error("movie_recommender_model.pkl was not found in the project folder.")
        st.stop()
    return joblib.load(MODEL_PATH)


model_data = load_model()

movie_user_matrix = model_data["movie_user_matrix"]
movie_kmeans = model_data["movie_kmeans"]
movie_cluster_df = model_data["movie_cluster_df"]
movie_similarity_df = model_data["movie_similarity_df"]
df = model_data["df"]


# ============================================================
# DATASET RATINGS & METADATA CACHE
# ============================================================

# Average movie ratings: df.groupby("Movie_Title")["Rating"].mean()
MOVIE_AVG_RATINGS = df.groupby("Movie_Title")["Rating"].mean().to_dict()
DATASET_AVG_RATING = float(df["Rating"].mean())

# Unique movie metadata dictionary
MOVIE_META_DICT = {}
for title, group in df.groupby("Movie_Title"):
    row = group.iloc[0]
    MOVIE_META_DICT[title] = {
        "Genre": str(row.get("Genre", "Unknown")),
        "Release_Year": str(row.get("Release_Year", "Unknown")),
        "Language": str(row.get("Language", "Unknown")),
        "Runtime_Minutes": str(row.get("Runtime_Minutes", "Unknown")),
        "Number_of_Ratings": int(row.get("Number_of_Ratings", len(group)))
    }


def get_movie_meta(title):
    clean_title = str(title).strip()
    return MOVIE_META_DICT.get(clean_title, {
        "Genre": "Unknown",
        "Release_Year": "Unknown",
        "Language": "Unknown",
        "Runtime_Minutes": "Unknown",
        "Number_of_Ratings": 0
    })


def get_movie_rating(title):
    clean_title = str(title).strip()
    val = MOVIE_AVG_RATINGS.get(clean_title)
    if val is None or pd.isna(val):
        return None
    return float(val)


def render_star_rating_html(rating_val, show_out_of_10=True):
    """
    Renders golden stars and numeric rating based on 5-star & 10-star scales.
    If rating_val is None, returns 'Not Rated'.
    """
    if rating_val is None or pd.isna(rating_val):
        return '<span style="color:#94a3b8; font-size:12px; font-weight:600;">Not Rated</span>'

    rating_5 = rating_val / 2.0
    full_stars = min(max(int(round(rating_5)), 0), 5)
    stars_html = ("&#9733;" * full_stars) + ("&#9734;" * (5 - full_stars))

    if show_out_of_10:
        return f'<span style="color:#fbbf24; font-size:16px; letter-spacing:1px;">{stars_html}</span> <span style="color:#ffffff; font-weight:700; font-size:14px; margin-left:4px;">{rating_5:.1f}/5</span> <span style="color:#94a3b8; font-size:12px; margin-left:2px;">({rating_val:.1f}/10)</span>'
    else:
        return f'<span style="color:#fbbf24; font-size:13px; letter-spacing:0.5px;">{stars_html}</span> <span style="color:#ffffff; font-weight:700; font-size:12px; margin-left:3px;">{rating_5:.1f}/5</span>'


# ============================================================
# POSTER RENDERING
# ============================================================

def normalize_movie_name(name):
    name = str(name).lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


def find_movie_image(movie_title):
    normalized_title = normalize_movie_name(movie_title)
    extensions = [".png", ".jpg", ".jpeg", ".webp"]

    for directory in IMAGE_DIRECTORIES:
        if not directory.exists():
            continue
        for extension in extensions:
            image_file = directory / f"{normalized_title}{extension}"
            if image_file.exists():
                return image_file
        try:
            for file in directory.rglob("*"):
                if not file.is_file() or file.suffix.lower() not in extensions:
                    continue
                if normalize_movie_name(file.stem) == normalized_title:
                    return file
        except Exception:
            pass
    return None


GRADIENT_PALETTES = [
    ("rgba(88, 28, 135, 0.85)", "rgba(15, 23, 42, 0.95)"),
    ("rgba(190, 24, 93, 0.85)", "rgba(15, 23, 42, 0.95)"),
    ("rgba(3, 105, 161, 0.85)", "rgba(15, 23, 42, 0.95)"),
    ("rgba(13, 148, 136, 0.85)", "rgba(15, 23, 42, 0.95)"),
    ("rgba(109, 40, 217, 0.85)", "rgba(30, 27, 75, 0.95)")
]


def get_movie_poster_html(movie_title, img_class="rec-poster-img"):
    clean_title = str(movie_title).strip()
    poster_file = POSTER_MAP.get(clean_title)

    if not poster_file or not poster_file.exists():
        poster_file = find_movie_image(clean_title)

    if poster_file and Path(poster_file).exists():
        b64 = get_image_base64(poster_file)
        if b64:
            return f'<img src="{b64}" alt="{clean_title}" class="{img_class}" />'

    idx = sum(ord(c) for c in clean_title) % len(GRADIENT_PALETTES)
    g1, g2 = GRADIENT_PALETTES[idx]
    return f'<div class="{img_class}" style="background:linear-gradient(145deg, {g1}, {g2}); border:1px solid rgba(255,255,255,0.12); display:flex; flex-direction:column; align-items:center; justify-content:center; padding:8px; text-align:center;"><div style="font-size:22px;">🎬</div><div style="font-size:11px; font-weight:700; color:#ffffff; margin-top:4px;">{clean_title}</div></div>'


# ============================================================
# RECOMMENDATION ALGORITHM (UNCHANGED ML LOGIC)
# ============================================================

def recommend_similar_movies(movie_title, n=5):
    if movie_title not in movie_user_matrix.index:
        return pd.DataFrame()

    cluster_rows = movie_cluster_df.loc[
        movie_cluster_df["Movie_Title"] == movie_title,
        "Cluster"
    ]

    if cluster_rows.empty:
        return pd.DataFrame()

    selected_cluster = cluster_rows.iloc[0]

    same_cluster_movies = (
        movie_cluster_df[
            movie_cluster_df["Cluster"] == selected_cluster
        ]["Movie_Title"].tolist()
    )

    valid_movies = [
        movie
        for movie in same_cluster_movies
        if movie in movie_similarity_df.columns and movie != movie_title
    ]

    if movie_title not in movie_similarity_df.index or not valid_movies:
        return pd.DataFrame()

    similarities = movie_similarity_df.loc[
        movie_title,
        valid_movies
    ]

    recommendations = (
        similarities
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )

    recommendations.columns = [
        "Movie_Title",
        "Similarity"
    ]

    return recommendations


# ============================================================
# SIDEBAR (COLLAPSED BY DEFAULT ON MOBILE)
# ============================================================

with st.sidebar:
    # Logo & Brand Header
    logo_img_tag = (
        f'<img src="{LOGO_BASE64}" style="width:44px; height:44px; object-fit:contain; filter:drop-shadow(0 0 12px rgba(168,85,247,0.7));" />'
        if LOGO_BASE64 else
        '<div style="width:44px; height:44px; border-radius:12px; background:linear-gradient(135deg, #a855f7, #ec4899); display:flex; align-items:center; justify-content:center; font-size:24px; box-shadow:0 0 14px rgba(168,85,247,0.6);">🎬</div>'
    )

    st.markdown(
        f"""<div style="display:flex; align-items:center; gap:12px; margin-bottom:24px; padding-top:4px;">
{logo_img_tag}
<div>
<div style="font-size:23px; font-weight:800; letter-spacing:-0.4px; line-height:1.1;">
<span style="color:#ffffff;">Movie</span>
<span style="background:linear-gradient(135deg, #ec4899, #a855f7); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Mind</span>
</div>
<div style="font-size:11px; color:#94a3b8; font-weight:500; margin-top:2px;">
Netflix + IMDb AI Engine
</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    # Navigation Menu
    st.markdown(
        """<div style="display:flex; flex-direction:column; gap:6px; margin-bottom:28px;">
<div style="display:flex; align-items:center; gap:12px; padding:11px 16px; border-radius:12px; background:linear-gradient(90deg, #ec4899, #a855f7, #3b82f6); color:white; font-weight:700; font-size:13.5px; box-shadow:0 4px 20px rgba(236,72,153,0.45); cursor:pointer;">
<span style="font-size:17px;">🏠</span> Home Dashboard
</div>
<div style="display:flex; align-items:center; gap:12px; padding:11px 16px; border-radius:12px; color:#94a3b8; font-weight:500; font-size:13.5px; cursor:pointer;">
<span style="font-size:17px;">🔍</span> Discover Movies
</div>
<div style="display:flex; align-items:center; gap:12px; padding:11px 16px; border-radius:12px; color:#94a3b8; font-weight:500; font-size:13.5px; cursor:pointer;">
<span style="font-size:17px;">⭐</span> IMDb Top Rated
</div>
<div style="display:flex; align-items:center; gap:12px; padding:11px 16px; border-radius:12px; color:#94a3b8; font-weight:500; font-size:13.5px; cursor:pointer;">
<span style="font-size:17px;">✨</span> AI Matches
</div>
<div style="display:flex; align-items:center; gap:12px; padding:11px 16px; border-radius:12px; color:#94a3b8; font-weight:500; font-size:13.5px; cursor:pointer;">
<span style="font-size:17px;">🔥</span> Trending Now
</div>
<div style="display:flex; align-items:center; gap:12px; padding:11px 16px; border-radius:12px; color:#94a3b8; font-weight:500; font-size:13.5px; cursor:pointer;">
<span style="font-size:17px;">🎬</span> Movie Details
</div>
</div>""",
        unsafe_allow_html=True
    )

    # Decorative Dream Card
    if DREAM_CARD_BASE64:
        st.markdown(
            f"""<div style="margin-top:10px; margin-bottom:20px; border-radius:16px; overflow:hidden; border:1px solid rgba(168,85,247,0.3); box-shadow:0 6px 24px rgba(0,0,0,0.5);">
<img src="{DREAM_CARD_BASE64}" style="width:100%; display:block;" />
</div>""",
            unsafe_allow_html=True
        )

    # Sidebar Bottom Info
    st.markdown(
        """<div style="margin-top:20px; padding-top:14px; border-top:1px solid rgba(255,255,255,0.08); display:flex; align-items:center; gap:8px; color:#64748b; font-size:11.5px;">
<span>⚡</span> Collaborative AI + Cosine Similarity
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# CINEMATIC HERO SECTION
# ============================================================

hero_logo_tag = (
    f'<img src="{LOGO_BASE64}" style="width:48px; height:48px; object-fit:contain; filter:drop-shadow(0 0 14px rgba(236,72,153,0.8));" />'
    if LOGO_BASE64 else
    '<div style="width:48px; height:48px; border-radius:14px; background:linear-gradient(135deg, #ec4899, #a855f7); display:flex; align-items:center; justify-content:center; font-size:24px; box-shadow:0 0 16px rgba(236,72,153,0.6);">🎬</div>'
)

hero_projector_tag = (
    f'<img src="{PROJECTOR_BASE64}" style="height:110px; object-fit:contain; mix-blend-mode:screen; opacity:0.95;" />'
    if PROJECTOR_BASE64 else
    ''
)

st.markdown(
    f"""<div class="hero-banner">
<div style="display:flex; flex-direction:column; gap:6px; z-index:2; flex:1;">
<div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
{hero_logo_tag}
<div>
<div class="hero-title" style="font-size:32px; font-weight:800; letter-spacing:-0.5px; line-height:1.1;">
<span style="color:#ffffff;">Movie</span>
<span style="background:linear-gradient(135deg, #ec4899, #a855f7, #38bdf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Mind</span>
</div>
<div style="font-size:13.5px; font-weight:600; color:#e2e8f0; margin-top:2px; display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
<span>Your taste. Our intelligence.</span>
<span style="background:rgba(236,72,153,0.25); color:#f472b6; border:1px solid rgba(236,72,153,0.4); font-size:10px; font-weight:700; padding:2px 8px; border-radius:6px; text-transform:uppercase;">AI Engine</span>
</div>
</div>
</div>
<div style="font-size:13px; color:#94a3b8; margin-top:4px;">
Discover movies similar to the ones you love, backed by collaborative rating intelligence.
</div>
</div>
<div class="hero-projector-wrap">
{hero_projector_tag}
</div>
</div>""",
    unsafe_allow_html=True
)


# ============================================================
# STATISTICS SECTION (STACKS VERTICALLY ON MOBILE)
# ============================================================

total_movies_count = len(movie_user_matrix)
clusters_count = movie_cluster_df["Cluster"].nunique()

stat_c1, stat_c2, stat_c3, stat_c4 = st.columns(4)

with stat_c1:
    st.markdown(
        f"""<div class="stat-card">
<div class="stat-icon icon-movies">🎬</div>
<div>
<div style="color:#94a3b8; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Total Movies</div>
<div style="color:#ffffff; font-size:22px; font-weight:800; line-height:1.2;">{total_movies_count:,}</div>
<div style="color:#ec4899; font-size:10.5px; font-weight:600; margin-top:2px;">↑ Active Catalog</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

with stat_c2:
    st.markdown(
        f"""<div class="stat-card">
<div class="stat-icon icon-clusters">🧠</div>
<div>
<div style="color:#94a3b8; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Total Clusters</div>
<div style="color:#ffffff; font-size:22px; font-weight:800; line-height:1.2;">{clusters_count}</div>
<div style="color:#a855f7; font-size:10.5px; font-weight:600; margin-top:2px;">↑ K-Means Groups</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

with stat_c3:
    st.markdown(
        """<div class="stat-card">
<div class="stat-icon icon-method">⚡</div>
<div>
<div style="color:#94a3b8; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Method</div>
<div style="color:#ffffff; font-size:17px; font-weight:800; line-height:1.2;">K-Means + Cosine</div>
<div style="color:#06b6d4; font-size:10.5px; font-weight:600; margin-top:2px;">↑ Collaborative AI</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

with stat_c4:
    st.markdown(
        f"""<div class="stat-card">
<div class="stat-icon icon-rating">⭐</div>
<div>
<div style="color:#94a3b8; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Avg Dataset Rating</div>
<div style="color:#ffffff; font-size:22px; font-weight:800; line-height:1.2;">{DATASET_AVG_RATING:.1f} <span style="font-size:13px; color:#f59e0b;">/10</span></div>
<div style="color:#f59e0b; font-size:10.5px; font-weight:600; margin-top:2px;">★ {DATASET_AVG_RATING/2:.1f}/5 IMDb Mean</div>
</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# CHOOSE A MOVIE CONTROLS
# ============================================================

st.markdown(
    """<div style="margin-top:20px; margin-bottom:8px;">
<div style="display:flex; align-items:center; gap:8px;">
<span style="font-size:20px;">🍿</span>
<span style="font-size:18px; font-weight:700; color:#ffffff;">Choose a Movie</span>
</div>
<div style="color:#94a3b8; font-size:12.5px; margin-top:2px;">
Select a movie to inspect its IMDb metadata and discover matching recommendations with similar user rating patterns.
</div>
</div>""",
    unsafe_allow_html=True
)

movie_titles = sorted(movie_user_matrix.index.tolist())
default_movie_index = movie_titles.index("Final Verdict") if "Final Verdict" in movie_titles else 0

ctrl_c1, ctrl_c2, ctrl_c3 = st.columns([4.2, 2.8, 3.0])

with ctrl_c1:
    selected_movie = st.selectbox(
        "🎬 Select Movie",
        movie_titles,
        index=default_movie_index
    )

with ctrl_c2:
    number_of_movies = st.selectbox(
        "🎯 Number of Similar Movies",
        [5, 10],
        index=0
    )

with ctrl_c3:
    st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
    find_movies = st.button(
        "✨ Find Similar Movies  ›",
        use_container_width=True
    )


# ============================================================
# SELECTED MOVIE (RESPONSIVE VERTICAL STACK ON MOBILE)
# ============================================================

st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

# Fetch selected movie metadata & rating
selected_meta = get_movie_meta(selected_movie)
selected_rating = get_movie_rating(selected_movie)

selected_genre = selected_meta["Genre"]
selected_year = selected_meta["Release_Year"]
selected_lang = selected_meta["Language"]
selected_runtime = selected_meta["Runtime_Minutes"]

selected_poster_html = get_movie_poster_html(
    selected_movie,
    img_class="selected-poster-img"
)

# Rating stars HTML
stars_markup = render_star_rating_html(selected_rating, show_out_of_10=True)

# Circular rating badge markup
if selected_rating is not None:
    circular_badge_html = f'<div class="circular-rating-badge"><span style="font-size:15px; font-weight:800; color:#ffffff; line-height:1;">{selected_rating:.1f}</span><span style="font-size:8px; font-weight:700; color:#f5c518; text-transform:uppercase;">IMDb</span></div>'
    imdb_chip_html = f'<span class="imdb-chip">IMDb <b>{selected_rating:.1f}</b></span>'
    rating_num_text = f"{selected_rating:.1f} / 10"
else:
    circular_badge_html = '<div class="circular-rating-badge" style="border-color:#64748b;"><span style="font-size:10px; font-weight:700; color:#94a3b8;">N/A</span></div>'
    imdb_chip_html = '<span class="imdb-chip" style="background:#64748b; color:#ffffff;">IMDb N/A</span>'
    rating_num_text = "Not Rated"

sel_col, how_col = st.columns([6.4, 3.6])

with sel_col:
    st.markdown(
        f"""<div style="font-size:16px; font-weight:700; color:#ffffff; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
<span>🎬</span> Selected Movie Overview
</div>
<div class="selected-movie-card">
<div class="selected-movie-poster-wrap">
{selected_poster_html}
</div>
<div style="flex:1; min-width:0;">
<div style="display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:6px; flex-wrap:wrap;">
<div style="font-size:24px; font-weight:800; color:#ffffff; letter-spacing:-0.4px; line-height:1.2;">
{selected_movie}
</div>
{circular_badge_html}
</div>
<div style="display:flex; align-items:center; gap:10px; margin-bottom:10px; flex-wrap:wrap;">
{imdb_chip_html}
<div>{stars_markup}</div>
</div>
<div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:10px;">
<span class="netflix-badge badge-genre">🎭 {selected_genre}</span>
<span class="netflix-badge badge-lang">🌐 {selected_lang}</span>
<span class="netflix-badge badge-year">📅 {selected_year}</span>
<span class="netflix-badge badge-runtime">⏱️ {selected_runtime} min</span>
</div>
<div class="movie-info-panel">
<div class="movie-info-item">
<span style="color:#94a3b8; font-size:10px; font-weight:600; text-transform:uppercase;">⏱️ Runtime</span>
<span style="color:#ffffff; font-size:12px; font-weight:700;">{selected_runtime} min</span>
</div>
<div class="movie-info-item">
<span style="color:#94a3b8; font-size:10px; font-weight:600; text-transform:uppercase;">🌐 Language</span>
<span style="color:#ffffff; font-size:12px; font-weight:700;">{selected_lang}</span>
</div>
<div class="movie-info-item">
<span style="color:#94a3b8; font-size:10px; font-weight:600; text-transform:uppercase;">🎭 Genre</span>
<span style="color:#ffffff; font-size:12px; font-weight:700;">{selected_genre}</span>
</div>
<div class="movie-info-item">
<span style="color:#94a3b8; font-size:10px; font-weight:600; text-transform:uppercase;">📅 Release Year</span>
<span style="color:#ffffff; font-size:12px; font-weight:700;">{selected_year}</span>
</div>
<div class="movie-info-item">
<span style="color:#94a3b8; font-size:10px; font-weight:600; text-transform:uppercase;">⭐ Avg Rating</span>
<span style="color:#f59e0b; font-size:12px; font-weight:700;">{rating_num_text}</span>
</div>
</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

with how_col:
    st.markdown(
        """<div style="font-size:16px; font-weight:700; color:#ffffff; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
<span>💡</span> How Movie Mind Works
</div>
<div class="how-it-works-card">
<div class="step-pill">
<div class="step-badge" style="background:#3b82f6;">1</div>
<div>Movie × User Rating Matrix</div>
</div>
<div class="step-pill">
<div class="step-badge" style="background:#06b6d4;">2</div>
<div>K-Means Movie Clustering</div>
</div>
<div class="step-pill">
<div class="step-badge" style="background:#10b981;">3</div>
<div>Target Cluster Identification</div>
</div>
<div class="step-pill">
<div class="step-badge" style="background:#a855f7;">4</div>
<div>Cosine Similarity Computation</div>
</div>
<div class="step-pill">
<div class="step-badge" style="background:#ec4899;">5</div>
<div>Top Ranked Recommendations</div>
</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# MOVIES YOU MAY LIKE (SINGLE COLUMN ON MOBILE, MULTI ON DESKTOP)
# ============================================================

recommendations = recommend_similar_movies(selected_movie, number_of_movies)

st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)

st.markdown(
    """<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
<div>
<div style="font-size:19px; font-weight:700; color:#ffffff; display:flex; align-items:center; gap:8px;">
<span>❤️</span> Movies You May Like
</div>
<div style="color:#94a3b8; font-size:12.5px; margin-top:2px;">
Personalized Netflix-style picks matching your selected title's cluster and cosine similarity.
</div>
</div>
<div style="color:#ec4899; font-size:12.5px; font-weight:700; cursor:pointer;">
View All Recommendations →
</div>
</div>""",
    unsafe_allow_html=True
)

if recommendations.empty:
    st.info("No similar movies found for the selected title in this cluster.")
else:
    num_recs = len(recommendations)
    grid_cols_count = min(num_recs, 5)
    rec_columns = st.columns(grid_cols_count)

    for i, (_, row) in enumerate(recommendations.iterrows(), start=1):
        col_idx = (i - 1) % grid_cols_count
        target_col = rec_columns[col_idx]

        rec_title = str(row["Movie_Title"]).strip()
        sim_val = float(row["Similarity"])
        sim_pct = sim_val * 100.0
        bar_pct = min(max(sim_pct, 5.0), 100.0)

        # Meta & Rating for recommended movie
        rec_meta = get_movie_meta(rec_title)
        rec_rating = get_movie_rating(rec_title)

        rec_genre = rec_meta["Genre"]
        rec_year = rec_meta["Release_Year"]
        rec_lang = rec_meta["Language"]

        # Responsive poster
        poster_thumb = get_movie_poster_html(
            rec_title,
            img_class="rec-poster-img"
        )

        # Star rating markup
        star_html = render_star_rating_html(rec_rating, show_out_of_10=False)

        # IMDb chip
        imdb_badge = (
            f'<span class="imdb-chip" style="font-size:9.5px; padding:2px 5px;">★ {rec_rating:.1f}</span>'
            if rec_rating is not None else
            '<span class="imdb-chip" style="background:#64748b; color:#fff; font-size:9.5px; padding:2px 5px;">N/A</span>'
        )

        with target_col:
            st.markdown(
                f"""<div class="rec-card">
<div class="rec-card-badge">✨ Recommended For You</div>
<div style="width:100%; overflow:hidden; border-radius:10px;">
{poster_thumb}
</div>
<div style="flex:1; min-width:0; width:100%;">
<div style="font-size:15px; font-weight:700; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="{rec_title}">
{rec_title}
</div>
<div style="display:flex; align-items:center; justify-content:space-between; margin-top:4px;">
<div>{star_html}</div>
{imdb_badge}
</div>
<div style="display:flex; gap:5px; flex-wrap:wrap; margin-top:8px;">
<span class="netflix-badge badge-genre" style="font-size:9px; padding:2px 6px;">{rec_genre}</span>
<span class="netflix-badge badge-lang" style="font-size:9px; padding:2px 6px;">{rec_lang}</span>
<span class="netflix-badge badge-year" style="font-size:9px; padding:2px 6px;">{rec_year}</span>
</div>
<div style="margin-top:10px;">
<div style="display:flex; justify-content:space-between; align-items:center; font-size:11px;">
<span style="color:#94a3b8;">🎯 Similarity</span>
<span style="color:#38bdf8; font-weight:700;">{sim_pct:.1f}% Match</span>
</div>
<div style="height:5px; background:rgba(255,255,255,0.08); border-radius:3px; overflow:hidden; margin-top:4px;">
<div style="height:100%; width:{bar_pct:.1f}%; background:linear-gradient(90deg, #06b6d4, #a855f7, #ec4899); box-shadow:0 0 8px rgba(236,72,153,0.7);"></div>
</div>
</div>
</div>
</div>""",
                unsafe_allow_html=True
            )


# ============================================================
# POPULAR MOVIES (TRENDING NETFLIX STYLE)
# ============================================================

st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

st.markdown(
    """<div style="font-size:19px; font-weight:700; color:#ffffff; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
<span>🔥</span> Trending on Movie Mind
</div>""",
    unsafe_allow_html=True
)

popular_movies = (
    df.groupby("Movie_Title")
    .size()
    .sort_values(ascending=False)
    .head(5)
)

pop_cols = st.columns([1.7, 1.7, 1.7, 1.7, 1.7, 1.5])

for i, (pop_movie, count) in enumerate(popular_movies.items()):
    pop_meta = get_movie_meta(pop_movie)
    pop_rat = get_movie_rating(pop_movie)
    pop_rat_str = f"★ {pop_rat:.1f}" if pop_rat is not None else "N/A"

    with pop_cols[i]:
        pop_poster_thumb = get_movie_poster_html(
            pop_movie,
            img_class="pop-poster-img"
        )

        st.markdown(
            f"""<div class="pop-card">
{pop_poster_thumb}
<div style="flex:1; min-width:0;">
<div style="color:#ffffff; font-size:12px; font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="{pop_movie}">
{pop_movie}
</div>
<div style="display:flex; align-items:center; gap:6px; margin-top:2px;">
<span class="imdb-chip" style="font-size:9px; padding:1px 5px;">{pop_rat_str}</span>
<span style="color:#94a3b8; font-size:10px;">{count:,} ratings</span>
</div>
</div>
</div>""",
            unsafe_allow_html=True
        )

with pop_cols[5]:
    if GREAT_MOVIES_BASE64:
        st.markdown(
            f"""<div style="display:flex; align-items:center; justify-content:center; height:100%;">
<img src="{GREAT_MOVIES_BASE64}" style="max-height:50px; object-fit:contain;" />
</div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """<div style="display:flex; align-items:center; gap:8px; height:100%; justify-content:center;">
<span style="font-size:20px;">🎬</span>
<span style="font-family:'Caveat', cursive; font-size:15px; color:#ec4899; font-weight:700; text-shadow:0 0 8px rgba(236,72,153,0.5);">
Great movies find you
</span>
</div>""",
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown('<div style="height:26px;"></div>', unsafe_allow_html=True)

st.markdown(
    """<div style="text-align:center; padding:22px 0; border-top:1px solid rgba(255,255,255,0.08); color:#64748b; font-size:11.5px; display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap;">
<span>🎬</span>
<span style="color:#ffffff; font-weight:700;">Movie Mind</span>
<span>•</span>
<span>Netflix + IMDb Hybrid Experience</span>
<span>•</span>
<span>K-Means Clustering + Cosine Similarity</span>
<span>•</span>
<span>Mobile & Desktop Optimized</span>
</div>""",
    unsafe_allow_html=True
)
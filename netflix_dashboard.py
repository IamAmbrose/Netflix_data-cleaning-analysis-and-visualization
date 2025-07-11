import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Standard light theme
sns.set_theme(style="whitegrid")  # default light Seaborn style

st.set_page_config(
    page_title="🎬 Netflix Data Dashboard",
    page_icon=":clapper:",
    layout="wide"
)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix1.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month_name()
    df['month_num'] = df['date_added'].dt.month
    df['duration_int'] = df['duration'].str.extract(r'(\\d+)').astype(float)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("📊 Filters")
content_type = st.sidebar.multiselect(
    "Type", df['type'].unique(), default=df['type'].unique()
)
selected_country = st.sidebar.multiselect(
    "Country", df['country'].dropna().unique(), default=[]
)
min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
release_year = st.sidebar.slider(
    "Release Year", min_year, max_year, (min_year, max_year)
)

# Apply filters
filtered_df = df[
    df['type'].isin(content_type) &
    df['release_year'].between(release_year[0], release_year[1])
]

if selected_country:
    filtered_df = filtered_df[
        filtered_df['country'].fillna('NA').str.contains('|'.join(selected_country))
    ]

# Page Title & Preview
st.title("🎥 Netflix Data Dashboard")
st.markdown("Explore Netflix’s global catalog — filter by type, country, year — and discover trends 📈")

st.write(f"**Total Titles:** {filtered_df.shape[0]}")
st.dataframe(filtered_df.head(5))

#  Type Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("Movies vs TV Shows")
    type_counts = filtered_df['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    fig, ax = plt.subplots()
    sns.barplot(data=type_counts, x='Type', y='Count', palette="Reds_r", ax=ax)
    ax.set_xlabel("Type")
    ax.set_ylabel("Count")
    ax.set_title("Movies vs TV Shows")
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Top 10 Ratings")
    top_ratings = filtered_df['rating'].value_counts().head(10).reset_index()
    top_ratings.columns = ["Rating", "Count"]
    fig, ax = plt.subplots()
    sns.barplot(data=top_ratings, x="Rating", y="Count", hue="Rating", dodge=False, palette="tab10", ax=ax, legend=False)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    ax.set_title("Top 10 Ratings")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

#Top 10 Countries
st.subheader("🌍 Top 10 Countries")
top_countries = (
    filtered_df['country']
    .dropna()
    .str.split(',')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)
top_countries.columns = ["Country", "Count"]
fig, ax = plt.subplots()
sns.barplot(data=top_countries, x="Country", y="Count", hue="Country", dodge=False, palette="tab10", ax=ax, legend=False)
ax.set_xlabel("Country")
ax.set_ylabel("Count")
ax.set_title("Top 10 Countries")
plt.xticks(rotation=45)
st.pyplot(fig)
plt.close(fig)

# Top 10 Directors
st.subheader("🎬 Top 10 Directors")
top_directors = (
    filtered_df['director']
    .dropna()
    .str.split(',')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)
top_directors.columns = ["Director", "Count"]
fig, ax = plt.subplots()
sns.barplot(data=top_directors, x="Director", y="Count", hue="Director", dodge=False, palette="tab10", ax=ax, legend=False)
ax.set_xlabel("Director")
ax.set_ylabel("Count")
ax.set_title("Top 10 Directors")
plt.xticks(rotation=90)
st.pyplot(fig)
plt.close(fig)

# Top Genres: Movies vs TV Shows
st.subheader("🎭 Popular Genres")

movies_df = filtered_df[filtered_df['type'] == 'Movie']
tvshows_df = filtered_df[filtered_df['type'] == 'TV Show']

movie_genres = (
    movies_df['listed_in']
    .dropna()
    .str.split(',')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)
movie_genres.columns = ['Genre', 'Count']

tvshow_genres = (
    tvshows_df['listed_in']
    .dropna()
    .str.split(',')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)
tvshow_genres.columns = ['Genre', 'Count']

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Movies:**")
    fig, ax = plt.subplots()
    sns.barplot(data=movie_genres, x="Genre", y="Count", palette="Reds_r", ax=ax)
    ax.set_xlabel("Genre")
    ax.set_ylabel("Count")
    ax.set_title("Top 10 Movie Genres")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

with col4:
    st.markdown("**TV Shows:**")
    fig, ax = plt.subplots()
    sns.barplot(data=tvshow_genres, x="Genre", y="Count", palette="Set2", ax=ax)
    ax.set_xlabel("Genre")
    ax.set_ylabel("Count")
    ax.set_title("Top 10 TV Show Genres")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

#Yearly & Monthly Trends
st.subheader("📅 Content Added Over Time")

yearly = (
    filtered_df.groupby(['year_added', 'type']).size().reset_index(name='Count').dropna()
)
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(data=yearly, x='year_added', y='Count', hue='type', palette='tab10', ax=ax)
ax.set_xlabel("Year Added")
ax.set_ylabel("Number of Titles")
ax.set_title("Yearly Releases")
st.pyplot(fig)
plt.close(fig)

monthly = (
    filtered_df.groupby(['month_num', 'month_added', 'type'])
    .size()
    .reset_index(name='Count')
    .dropna()
    .sort_values('month_num')
)
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(
    data=monthly,
    x='month_added',
    y='Count',
    hue='type',
    order=[
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ],
    palette='tab10',
    ax=ax
)
ax.set_xlabel("Month Added")
ax.set_ylabel("Number of Titles")
ax.set_title("Monthly Releases")
plt.xticks(rotation=45)
st.pyplot(fig)
plt.close(fig)

# Duration Analysis
st.subheader("⏱️ Duration Analysis")
col5, col6 = st.columns(2)

with col5:
    st.markdown("**Movies (Minutes)**")
    movie_durations = movies_df['duration_int'].dropna()
    fig, ax = plt.subplots()
    sns.histplot(movie_durations, bins=30, kde=True, color="#E50914", ax=ax)
    ax.set_xlabel("Minutes")
    ax.set_ylabel("Frequency")
    ax.set_title("Movie Durations")
    st.pyplot(fig)
    plt.close(fig)

with col6:
    st.markdown("**TV Shows (Seasons)**")
    tv_durations = tvshows_df['duration_int'].dropna()
    fig, ax = plt.subplots()
    sns.countplot(x=tv_durations, palette="tab10", ax=ax)
    ax.set_xlabel("Seasons")
    ax.set_ylabel("Count")
    ax.set_title("TV Show Seasons")
    st.pyplot(fig)
    plt.close(fig)

# Download Cleaned Data
st.markdown("###Download Filtered Dataset")
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='netflix_cleaned.csv',
    mime='text/csv'
)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>Built Streamlit | Netflix Data Project</p>",
    unsafe_allow_html=True
)

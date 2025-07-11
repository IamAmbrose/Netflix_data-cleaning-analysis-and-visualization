import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Netflix-style dark theme
sns.set_style("darkgrid")
plt.rcParams['axes.facecolor'] = '#121212'
plt.rcParams['figure.facecolor'] = '#121212'
plt.rcParams['axes.labelcolor'] = '#FFFFFF'
plt.rcParams['xtick.color'] = '#FFFFFF'
plt.rcParams['ytick.color'] = '#FFFFFF'
plt.rcParams['text.color'] = '#FFFFFF'

st.set_page_config(
    page_title="🎬 Netflix Data Dashboard",
    page_icon=":clapper:",
    layout="wide"
)

#Load Data
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


#Sidebar Filters
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

#Type Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("Movies vs TV Shows")
    type_counts = filtered_df['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    sns.barplot(data=type_counts, x='Type', y='Count', palette="Reds_r")
    plt.xlabel("Type")
    plt.ylabel("Count")
    st.pyplot(plt.gcf())
    plt.clf()

with col2:
    st.subheader("Top 10 Ratings")
    top_ratings = filtered_df['rating'].value_counts().head(10).reset_index()
    top_ratings.columns = ["Rating", "Count"]
    sns.barplot(data=top_ratings, x="Rating", y="Count", hue="Rating", dodge=False, palette="tab10", legend=False)
    plt.xticks(rotation=45)
    plt.xlabel("Rating")
    plt.ylabel("Count")
    st.pyplot(plt.gcf())
    plt.clf()

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
sns.barplot(data=top_countries, x="Country", y="Count", hue="Country", dodge=False, palette="tab10", legend=False)
plt.xticks(rotation=45)
plt.xlabel("Country")
plt.ylabel("Count")
st.pyplot(plt.gcf())
plt.clf()

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
sns.barplot(data=top_directors, x="Director", y="Count", hue="Director", dodge=False, palette="tab10", legend=False)
plt.xticks(rotation=90)
plt.xlabel("Director")
plt.ylabel("Count")
st.pyplot(plt.gcf())
plt.clf()

# -------------------------------
# ✅ Top Genres: Movies vs TV Shows
# -------------------------------
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
    sns.barplot(data=movie_genres, x="Genre", y="Count", palette="Reds_r")
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.clf()

with col4:
    st.markdown("**TV Shows:**")
    sns.barplot(data=tvshow_genres, x="Genre", y="Count", palette="Set2")
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.clf()

# -------------------------------
# ✅ Yearly & Monthly Trends
# -------------------------------
st.subheader("📅 Content Added Over Time")

yearly = (
    filtered_df.groupby(['year_added', 'type']).size().reset_index(name='Count').dropna()
)

plt.figure(figsize=(12,6))
sns.barplot(data=yearly, x='year_added', y='Count', hue='type', palette='tab10')
plt.xlabel("Year Added")
plt.ylabel("Number of Titles")
plt.title("Yearly Releases")
st.pyplot(plt.gcf())
plt.clf()

monthly = (
    filtered_df.groupby(['month_num', 'month_added', 'type'])
    .size()
    .reset_index(name='Count')
    .dropna()
    .sort_values('month_num')
)

plt.figure(figsize=(12,6))
sns.barplot(
    data=monthly,
    x='month_added',
    y='Count',
    hue='type',
    order=[
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ],
    palette='tab10'
)
plt.xlabel("Month Added")
plt.ylabel("Number of Titles")
plt.title("Monthly Releases")
plt.xticks(rotation=45)
st.pyplot(plt.gcf())
plt.clf()

#Duration Analysis
st.subheader("⏱️ Duration Analysis")

# ✅ Define the columns first!
col5, col6 = st.columns(2)

# Movies Duration
with col5:
    st.markdown("**Movies (Minutes)**")
    movie_durations = movies_df['duration_int'].dropna()
    fig1, ax1 = plt.subplots()
    sns.histplot(movie_durations, bins=30, kde=True, color="#E50914", ax=ax1)
    ax1.set_xlabel("Minutes")
    ax1.set_title("Movie Durations")
    st.pyplot(fig1)

# TV Shows Duration
with col6:
    st.markdown("**TV Shows (Seasons)**")
    tv_durations = tvshows_df['duration_int'].dropna()
    fig2, ax2 = plt.subplots()
    sns.countplot(x=tv_durations, palette="tab10", ax=ax2)
    ax2.set_xlabel("Seasons")
    ax2.set_ylabel("Count")
    ax2.set_title("TV Show Seasons")
    st.pyplot(fig2)

#Download Cleaned Data
st.markdown("### 📥 Download Filtered Dataset")
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='netflix_cleaned.csv',
    mime='text/csv'
)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>Built using Streamlit | Netflix Data Project</p>",
    unsafe_allow_html=True
)

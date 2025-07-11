# 🎬 Netflix Data: Cleaning, Analysis & Visualization (Beginner ML Project)

This project analyzes a real Netflix dataset with **Python, Pandas, Matplotlib, Seaborn, and Streamlit**.  
It includes data cleaning, exploratory data analysis (EDA), clear insights, and is ready for beginner-level machine learning tasks.

---

## 📌 **Project Objective**

- Clean and preprocess Netflix data.
- Explore core content patterns: **type, genres, countries, ratings, durations, trends**.
- Visualize content trends over time and by categories.
- Prepare insights for a possible content recommender or classification task.
- Deploy an **interactive dashboard** for live exploration.

---

## 🗂️ **Dataset**

- ~8,790 titles: **Movies** & **TV Shows**
- Columns: `show_id`, `type`, `title`, `director`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`
- Each row is a title on Netflix.

---

## 🔍 **Key Insights & Findings**

✅ **Content Type:**  
- ~70% Movies, ~30% TV Shows  
- TV Shows often short-run (1–2 seasons).

✅ **Top Countries:**  
- US leads (3,240+ titles) — India, UK, Japan & South Korea add global variety.

✅ **Popular Genres:**  
- Movies: *International Movies*, *Dramas*, *Comedies*, *Documentaries*
- TV Shows: *International TV Shows*, *Crime*, *TV Dramas*, *Kids' TV*

✅ **Ratings:**  
- Mostly mature: *TV-MA*, *TV-14* dominate.
- Smaller share: family/kids (TV-Y, TV-PG).

✅ **Directors:**  
- Many missing (`Not Given`) but top contributors include **Rajiv Chilaka**, **Martin Scorsese**, etc.

✅ **Time Trends:**  
- Huge spike 2016–2019, slight drop during pandemic.
- Monthly peaks in Jan/Mar → strategic releases.

✅ **Durations:**  
- Average Movie: ~99 mins
- Average TV Show: ~1.75 seasons

---

## ✅ **Conclusion**

Netflix’s library is:
- Heavy on **US content** but strongly global.
- Dominated by **adult-oriented genres**.
- Focused on **short, binge-ready series**.
- Ready for beginner ML — clustering genres, classifying type, or building a recommender.

---

## 📈 **Visuals**

Key charts:
- Movies vs TV Shows bar plot
- Top genres for both
- Top countries & directors
- Rating distribution (multi-colored)
- Content trends by year & month
- Duration analysis: Movie runtimes & TV Show seasons

---

## ⚙️ **How to Run Locally**

```bash
# 1️⃣ Clone this repo
git clone https://github.com/yourusername/netflix-data-analysis.git
cd netflix-data-analysis

# 2️⃣ Install Python dependencies
pip install pandas matplotlib seaborn streamlit

# 3️⃣ Run the notebook or the Streamlit dashboard
streamlit run netflix_dashboard.py

Streamlit Dashboard
This project includes a Streamlit app with:

Filters for Type, Country, Release Year

Visuals for Type, Ratings, Genres, Countries

Duration insights

Cleaned data download button

👉 Demo: Streamlit App
👉 Live Demo: Streamlit App
(Replace with your deployed link)

🛠️ Technologies Used
Python 3

Pandas

Matplotlib

Seaborn

📜 Author
Ambrose Henry

🔗 GitHub | LinkedIn

⭐️ Show Your Support!
If you like this project:

⭐️ Star this repo

📣 Share with other beginners

✅ Fork it and try your own analysis!
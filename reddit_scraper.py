import streamlit as st
import praw
import pandas as pd
import time

st.set_page_config(page_title="Reddit Scraper", layout="centered")
st.title("📄 Reddit Post Scraper")
st.markdown("Easily fetch posts from any public subreddit using Reddit's API.")

# 🔒 Hardcoded Reddit API credentials
client_id = "cgP68H1kYit8qRQqrHF0og"
client_secret = "sP0XbjbYo5FN8TvDRXKHMvDDazd3qA"
user_agent = "Reddit scraper"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

st.subheader("📥 Scrape Settings")
subreddit_name = st.text_input("Subreddit Name (e.g., technology)", value="technology")
download_all = st.checkbox("Download all available posts (up to 1000)", value=True)

if not download_all:
    limit = st.slider("Number of posts", 1, 1000, 100)
else:
    limit = 1000

sort_option = st.selectbox("Sort by", ["hot", "new", "top"])
fetch_button = st.button("Fetch Posts")

if fetch_button and subreddit_name:
    try:
        with st.spinner("Fetching posts..."):
            subreddit = reddit.subreddit(subreddit_name)
            if sort_option == "hot":
                posts = subreddit.hot(limit=limit)
            elif sort_option == "new":
                posts = subreddit.new(limit=limit)
            else:
                posts = subreddit.top(limit=limit)

            data = []
            for post in posts:
                data.append({
                    "Title": post.title,
                    "Score": post.score,
                    "URL": post.url,
                    "Comments": post.num_comments,
                    "Created_UTC": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(post.created_utc))
                })

            df = pd.DataFrame(data)
            st.success(f"Fetched {len(df)} posts from r/{subreddit_name}")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{subreddit_name}_posts.csv",
                mime='text/csv',
            )

    except Exception as e:
        st.error(f"Error: {e}")

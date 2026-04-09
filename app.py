# app.py
# AI Support Ticket Analyzer - Enhanced Version with Weekly Ticket Trend

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(
    page_title="AI Support Ticket Analyzer",
    layout="wide"
)

st.title("AI Support Ticket Analyzer")
st.write("Interactive dashboard for analyzing support tickets, trends, sentiment, and top issues.")

# -----------------------
# Load preprocessed data
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/tickets_processed.csv")
    if 'ticket_created_date' in df.columns:
        df['ticket_created_date'] = pd.to_datetime(df['ticket_created_date'], errors='coerce')
    return df

df = load_data()

# -----------------------
# Generate human-readable topic names
# -----------------------
def generate_topic_names(df, top_n_words=3):
    topic_names = {}
    for topic in df["topic"].unique():
        if topic == -1:
            topic_names[topic] = "Other / Outliers"
            continue
        words = " ".join(df[df["topic"] == topic]["clean_text"].astype(str)).split()
        most_common = [w for w, _ in Counter(words).most_common(top_n_words)]
        topic_names[topic] = " ".join(most_common)
    return topic_names

topic_names = generate_topic_names(df)
df["topic_name"] = df["topic"].map(topic_names)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")
st.sidebar.markdown("### Product Filter")

products = st.sidebar.multiselect(
    "Select Product",
    options=df["product"].unique(),
    default=df["product"].unique()
)

sentiments = st.sidebar.multiselect(
    "Select Sentiment",
    options=df["sentiment"].unique(),
    default=df["sentiment"].unique()
)

max_topics = st.sidebar.slider(
    "Number of Topics to Display",
    min_value=5,
    max_value=30,
    value=10
)

filtered_df = df[
    (df["product"].isin(products)) &
    (df["sentiment"].isin(sentiments))
]

# -----------------------
# KPI Metrics
# -----------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Tickets", len(filtered_df))
col2.metric("Unique Topics", filtered_df["topic"].nunique())
col3.metric("Products", filtered_df["product"].nunique())

st.divider()

# -----------------------
# Tabs for charts
# -----------------------
tabs = st.tabs([
    "Top Topics",
    "Sentiment Distribution",
    "Topic Exploration",
    "Sentiment Over Time",
    "Weekly Ticket Volume"
])

# --- Tab 1: Top Topics ---
with tabs[0]:
    st.subheader("Top Topics by Ticket Volume")
    topic_counts = filtered_df["topic_name"].value_counts().head(max_topics)
    fig, ax = plt.subplots(figsize=(10,5))
    topic_counts.plot(kind="bar", ax=ax, color='skyblue')
    ax.set_title("Top Topics by Ticket Volume")
    ax.set_ylabel("Number of Tickets")
    ax.set_xlabel("Topic")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

# --- Tab 2: Sentiment Distribution ---
with tabs[1]:
    st.subheader("Sentiment Distribution")
    sentiment_counts = filtered_df["sentiment"].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6,4))
    sentiment_counts.plot(kind="bar", ax=ax2, color=['red','gray','green'])
    ax2.set_title("Sentiment Distribution")
    ax2.set_ylabel("Number of Tickets")
    ax2.set_xlabel("Sentiment")
    st.pyplot(fig2)

# --- Tab 3: Topic Exploration ---
with tabs[2]:
    st.subheader("Explore Individual Topics")
    selected_topic = st.selectbox(
        "Select Topic",
        sorted(filtered_df["topic_name"].unique())
    )
    topic_df = filtered_df[filtered_df["topic_name"] == selected_topic]
    st.write(f"Tickets in Topic '{selected_topic}': {len(topic_df)}")

    st.subheader("Example Tickets")
    st.dataframe(
        topic_df[["ticket_id","product","issue_description","sentiment"]].head(20)
    )

    st.subheader("Top Words in Topic")
    text = " ".join(topic_df["clean_text"].astype(str))
    words = text.split()
    word_freq = pd.Series(words).value_counts().head(20)
    fig3, ax3 = plt.subplots(figsize=(10,5))
    word_freq.plot(kind="bar", ax=ax3, color='orange')
    ax3.set_title(f"Top Words in Topic '{selected_topic}'")
    ax3.set_ylabel("Frequency")
    ax3.set_xlabel("Word")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig3)

# --- Tab 4: Sentiment Over Time ---
with tabs[3]:
    st.subheader("Sentiment Over Time")
    if 'ticket_created_date' in filtered_df.columns:
        df_time = filtered_df.groupby([filtered_df['ticket_created_date'].dt.to_period('W'), 'sentiment']).size().unstack(fill_value=0)
        fig4, ax4 = plt.subplots(figsize=(10,5))
        df_time.plot(ax=ax4)
        ax4.set_title("Sentiment Trends Over Time (weekly)")
        ax4.set_ylabel("Number of Tickets")
        ax4.set_xlabel("Week")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig4)
    else:
        st.write("No date information available for sentiment over time chart.")

# --- Tab 5: Weekly Ticket Volume ---
with tabs[4]:
    st.subheader("Weekly Ticket Volume (Total Tickets)")
    if 'ticket_created_date' in filtered_df.columns:
        df_weekly = filtered_df.groupby(filtered_df['ticket_created_date'].dt.to_period('W')).size()
        fig5, ax5 = plt.subplots(figsize=(10,5))
        df_weekly.plot(ax=ax5, color='purple')
        ax5.set_title("Total Tickets Per Week")
        ax5.set_ylabel("Number of Tickets")
        ax5.set_xlabel("Week")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig5)
    else:
        st.write("No date information available for weekly ticket volume chart.")
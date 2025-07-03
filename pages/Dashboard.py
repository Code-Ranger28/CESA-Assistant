import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.title("📊 Chatbot Dashboard")
st.write("Insights into chatbot usage and performance.")

LOG_FILE = "chat_logs.jsonl"

@st.cache_data # Cache data loading for performance
def load_chat_logs():
    if not os.path.exists(LOG_FILE):
        st.warning("No chat logs found yet. Interact with the chatbot first!")
        return pd.DataFrame()

    data = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                st.error(f"Error parsing log line: {line.strip()}")
                continue
    df = pd.DataFrame(data)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
    return df

chat_df = load_chat_logs()

if not chat_df.empty:
    st.header("Overall Usage")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Interactions", len(chat_df))
    with col2:
        st.metric("Unique Days Active", chat_df['date'].nunique())
    
    # You can add more sophisticated metrics like average response length, etc.
    chat_df['user_query_length'] = chat_df['user_query'].apply(len)
    chat_df['bot_response_length'] = chat_df['bot_response'].apply(len)
    with col3:
        st.metric("Avg User Query Length", f"{chat_df['user_query_length'].mean():.1f} chars")
        st.metric("Avg Bot Response Length", f"{chat_df['bot_response_length'].mean():.1f} chars")

    st.header("Daily Interactions Trend")
    daily_interactions = chat_df.groupby('date').size().reset_index(name='count')
    fig_daily = px.line(daily_interactions, x='date', y='count', title='Number of Interactions Per Day')
    st.plotly_chart(fig_daily, use_container_width=True)

    st.header("Top User Queries (Simple Word Cloud - placeholder)")
    # For a real word cloud, you'd use libraries like wordcloud
    # This is just a simple frequency count
    all_user_words = ' '.join(chat_df['user_query'].tolist()).lower().split()
    word_counts = pd.Series(all_user_words).value_counts().head(10)
    st.bar_chart(word_counts)

    st.header("Raw Chat Log Data")
    st.dataframe(chat_df[['timestamp', 'user_query', 'bot_response']].tail(20), use_container_width=True) # Show last 20
else:
    st.info("No chat interactions recorded yet to display on the dashboard. Go to the '💬 Chatbot' page and start chatting!")
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Bible NLP Dashboard", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Search", "PCA & Word2Vec", "Generator"])

if page == "Dashboard":
    st.title("Dashboard")
    
    col1, col2, col3 = st.columns(3)
    testament = col1.selectbox("Testament", ["All", "0", "1"])
    book_name = col2.text_input("Book Name (Optional)")
    chapter_id = col3.text_input("Chapter ID (Optional)")
    
    params = {}
    if testament != "All": params["testament"] = testament
    if book_name: params["book_name"] = book_name
    if chapter_id: params["chapter_id"] = chapter_id
        
    response = requests.get(f"{API_URL}/dashboard", params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        counts = data.get("verse_counts", {})
        lengths = data.get("verse_lengths", {})
        freqs = data.get("frequencies", {})
        
        if counts:
            df_counts = pd.DataFrame(list(counts.items()), columns=["Book", "Verses"])
            fig1 = px.bar(df_counts, x="Book", y="Verses", title="Verses per Book")
            st.plotly_chart(fig1, use_container_width=True)
            
            df_lengths = pd.DataFrame(list(lengths.items()), columns=["Book", "Avg Length"])
            fig2 = px.bar(df_lengths, x="Book", y="Avg Length", title="Average Verse Length per Book")
            st.plotly_chart(fig2, use_container_width=True)
            
            st.subheader("Top Words WordCloud")
            if freqs:
                wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(freqs)
                fig3, ax = plt.subplots()
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig3)
        else:
            st.warning("No data found for the selected filters.")

elif page == "Search":
    st.title("Semantic Search")
    query = st.text_input("Enter phrase to search:")
    
    if st.button("Search") and query:
        response = requests.get(f"{API_URL}/search", params={"query": query})
        if response.status_code == 200:
            results = response.json()
            df = pd.DataFrame(results)
            st.dataframe(df)

elif page == "PCA & Word2Vec":
    st.title("Dimensionality Reduction")
    
    method = st.selectbox("Vectorization Method", ["tfidf", "word2vec"])
    dims = st.selectbox("Dimensions", [2, 3])
    
    if st.button("Render Plot"):
        with st.spinner("Loading coordinates..."):
            response = requests.get(f"{API_URL}/embeddings", params={"method": method, "dims": dims})
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                
                if dims == 2:
                    fig = px.scatter(df, x="x", y="y", color="testament", hover_data=["book"])
                else:
                    fig = px.scatter_3d(df, x="x", y="y", z="z", color="testament", hover_data=["book"])
                    
                fig.update_traces(marker=dict(size=3))
                st.plotly_chart(fig, use_container_width=True)

elif page == "Generator":
    st.title("Text Generator")
    
    n_gram = st.selectbox("N-Gram Model", [1, 2, 3, 4], index=1)
    start_word = st.text_input("Start Word")
    max_len = st.slider("Max Length", min_value=5, max_value=50, value=20)
    
    if st.button("Generate"):
        params = {"n": n_gram, "max_length": max_len}
        if start_word:
            params["start_word"] = start_word
            
        response = requests.get(f"{API_URL}/generate", params=params)
        if response.status_code == 200:
            text = response.json().get("text", "")
            st.success(text)
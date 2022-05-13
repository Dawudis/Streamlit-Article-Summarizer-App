import streamlit as st
import pandas as pd

st.title("Mass Article Extractive Summarizer")
st.write("1. Import a CSV dataset containing the article URLs you wish to be summarized.")
st.write("2. Choose the length of your summaries.")
st.write("3. We give you your summarized articles back in a downloadable dataframe.")
st.caption("WARNING: Column name with the urls must be titled 'urls', otherwise the summarizer won't work.")
st.caption("WARNING: Depending on the size of your dataset, the summarizer may take several minutes.")

st.header("Import Your Dataframe")
uploaded_file = st.file_uploader('Import Your CSV')
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  st.table(df.head())
  def run_model(df):
    from newsplease import NewsPlease
    from summarizer import Summarizer
    model = Summarizer()
    data = pd.DataFrame(columns=['Article Summaries'])
    for i in df['urls']:
      article = NewsPlease.from_url(i).maintext
      result = model(article, num_sentences = number)
      temporary_df = pd.DataFrame([result], columns = ['Article Summaries'])
      data = data.append(temporary_df, ignore_index=True)
    st.header('Results')
    st.table(data.head())
    @st.cache
    def convert_df_to_csv(df):
      return df.to_csv().encode('utf-8')
    st.download_button(
    label = "Download Dataframe as CSV",
    data = convert_df_to_csv(data),
    file_name = 'article_summaries.csv',
    mime = 'text/csv',
    )

st.header("Choose the Length of Your Summaries")
number = st.number_input('Number of Sentences', min_value=1, max_value=10)

if st.button('Summarize'):
  run_model(df)

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(chain, portfolio, clean_text):
    st.title("📧 Cold Email Generator")
    input_url = st.text_input("Enter a job description URL:", value="https://jobs.apple.com/en-in/details/200536464/machine-learning-engineer")
    submit_button  = st.button("Submit", type='secondary')

    if submit_button:
        try:
            loader = WebBaseLoader([input_url])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            # job description is parsed in JSON format
            jobs = chain.extract_jobs(data)
            for job_description in jobs:
                skills = job_description.get('skills', [])
                portfolio_links = portfolio.query_links(skills)
                email = chain.write_mail(job_description, portfolio_links)
                st.code(email, language='markdown', wrap_lines=True)
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
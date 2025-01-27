# Cold-Email-Llama

## About
This project is an automated cold email generator leveraging LLama 3.1 to generate personalized emails and Chromadb to include relevant portfolios based on the skills provided on job postings.

![Project image](project_img.png)

## Features
* **Job Description Extraction:** Automatically extracts job details from a given URL, including role, experience, skills, and description.
* **AI-Powered Email Generation:** Utilizes the Groq LLM to generate contextually relevant cold emails.
* **Portfolio Matching:** Matches job requirements with a company's portfolio to include relevant portfolio links in the email.

## Methodology
1. **URL Input:** Users input a job description URL into the Streamlit interface.
2. **Web Scraping:** WebBaseLoader to scrape the job details from the provided URL.
3. **Job Extraction:** LLaMA 3.1 model extracts key information from the scraped text, further parsing it into a JSON format.
4. **Portfolio Matching:** The system queries a Chromadb vector database to find relevant portfolio links based on the job skills.
5. **Email Generation:** The LLaMA 3.1 70B model generates a personalized cold email, incorporating the job details and relevant portfolio links.

## Tech Stack
* **LangChain:** For creating AI-powered chains of operations
* **Chromadb:** Vector database for storing and querying portfolio data
* **Groq:** For generating cold emails with fast inference

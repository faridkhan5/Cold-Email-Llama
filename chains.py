import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,
                       model="llama-3.1-70b-versatile")
        
    def extract_jobs(self, cleaned_text):
        extract_prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: `role`, `experience`, `skills` and `description`.

            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        extract_chain = extract_prompt | self.llm
        response = extract_chain.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            json_response = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Context is too big. Unable to parse the job description.")
        return json_response if isinstance(json_response, list) else [json_response]
    
    def write_mail(self, job_description, portfolio_links):
        email_prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are Rocky, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Atliq's portfolio: {links_list}
            Remember you are Mohan, BDE at AtliQ.

            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):  
            """
        )
        email_chain = email_prompt | self.llm
        response = email_chain.invoke({"job_description": str(job_description), "links_list": portfolio_links})
        return response.content
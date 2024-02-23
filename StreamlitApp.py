import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.MCQ_Generator.utils import read_file, get_table_data
import streamlit as st
from src.MCQ_Generator.MCQGen import generate_evaluate_chain
from src.MCQ_Generator.logger import logging
import google.generativeai as genai


# Load environment variables
load_dotenv()
#st.write(os.getenv("GOOGLE_API_KEY"))

def get_api_key():
    try:
        return os.getenv("GOOGLE_API_KEY")
    except KeyError:
        raise ValueError("Missing GOOGLE_API_KEY environment variable")


#loading json file
with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)


#creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

with st.form("user input"):
    uploaded_file = st.file_uploader("upload pdf or text")

    mcq_count = st.number_input("Number of MCQs you want", min_value=3, max_value=50)

    subject = st.text_input("Insert Subject",max_chars=30)

    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
    
         with st.spinner("loading..."):
             

            try:

                api_key = get_api_key()

            # Configure Google Generative AI
                genai.configure(api_key=api_key)
                
                text= read_file(uploaded_file)
            
                response=generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count,
                        "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                #st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"Error: {str(e)}")

            else:
                
                if isinstance(response, dict):
                    #Extract the quiz data from the response
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in atext box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")

                else:
                    st.write(response)





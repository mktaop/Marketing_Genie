#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 16:46:38 2023

@author: avi_patel
"""

import os, openai
from dotenv import load_dotenv 
import streamlit as st
from streamlit_option_menu import option_menu  
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def init_page() -> None:

    st.sidebar.title("Options")

def select_llm():
    """
    Read user selection of parameters in Streamlit sidebar.
    """
    model_name = st.sidebar.radio("Choose LLM:",
                                  ("gpt-3.5-turbo",
                                   "gpt-3.5-turbo-16k",
                                   "gpt-4"))
    temperature = st.sidebar.slider("Temperature:", min_value=0.0,
                                    max_value=1.0, value=0.0, step=0.01)
    return model_name, temperature

def load_llm(model_name: str, temperature: float):
    """
    Load LLM.
    """
    return ChatOpenAI(temperature=temperature, model_name=model_name)




def main():
    
    """
    1. use getenv get api keys needed
    2. provide option: a-keywords, b-email, c-content
    3. depending on choice populte main and sidebar options/headers/etc
    4. execute on the option chosen in #1, including output
    """
    
    page_title="MARKETING GENIE"
    page_icon=":genie:"
    layout="wide"

    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_icon + "    " + page_title + "    " + page_icon)
    init_page()

    selected = option_menu(
        menu_title="What's your wish? Select by clicking on your choice!",
        options=["Keywords generation", "Email generation", "Content generation"],
        icons=["key","envelope"],
        orientation="horizontal"
        )
    
    model_name, temperature = select_llm()
    llm = load_llm(model_name, temperature)
    
    if selected == "Keywords generation":
        kwrds = st.sidebar.slider("Number of keywords:", min_value=1,
                                        max_value=15, value=7, step=1)
        
        st.markdown("Provide a banking product to generate keywords for your PAID SEARCH MARKETING campaign")
        user_input1 = st.text_input("Enter your product below: ")
        if user_input1:
            user_input2 = str(kwrds)
            system_prompt = """You are a creative copywriter.
            You're given a category of financial services product and number of keywords needed, \
            and your goal is to provide keywords that we can use for search engine marketing."""
            messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input1},
                    {"role": "user", "content": user_input2}
                ]
            response = openai.ChatCompletion.create(
                model=model_name, temperature=temperature, 
                messages=messages
                )
            for responses in response.choices:
                generation = responses.message.content
            st.text(generation)
            
          


    if selected == "Email generation":
        ewrds = st.sidebar.slider("Number of words in desired in the email:", min_value=50,
                                        max_value=500, value=175, step=10)
        st.markdown("Provide a prompt to generate the copy you desire, be as specific as possible !")
        user_input3 = st.text_input("Enter your prompt below, be as specific and detailed as possible!")
        if user_input3:
            user_input4 = str(ewrds)
            system_prompt2 = """You are a creative copywriter.  You're given instructions \
                to generate an email copy and maximum number of words to use in the email copy and you can't exceed that number.  \
                Your goal is craft an email in a professional tone and provide bullet points if \
                that is helpful."""
                
            messages2 = [
                    {"role": "system", "content": system_prompt2},
                    {"role": "user", "content": user_input3},
                    {"role": "user", "content": user_input4}
                ]
            response2 = openai.ChatCompletion.create(
                model=model_name, temperature=temperature, max_tokens = ewrds,
                messages=messages2
                )
            for responses in response2.choices:
                generation2 = responses.message.content
            st.markdown(generation2)
            

    if selected == "Content generation":
        ewrds2 = st.sidebar.slider("Number of words in desired:", min_value=50,
                                        max_value=500, value=175, step=10)
        agebin = st.sidebar.selectbox('Select age range of your intended audience:',
                              ('Ages 18-24', 'Ages 25-34', 'Ages 35-49', 'Ages 50-64', 'Ages 65+', 'Ages 18+'))
        st.markdown("Provide a prompt to generate the content you desire, be as specific as possible !")
        user_input5 = st.text_input("Enter your prompt below, include things like: purpose or objective, etc!")
        if user_input5:
            user_input6 = str(ewrds2)
            system_prompt3 = """You are a creative copywriter.  You're given instructions \
                to generate marketing content and maximum number of words to use and the age range of the target \
                audience.  \
                Your goal is create this in a professional tone and provide bullet points if \
                that is helpful."""
                
            messages3 = [
                    {"role": "system", "content": system_prompt3},
                    {"role": "user", "content": user_input5},
                    {"role": "user", "content": user_input6},
                    {"role": "user", "content": agebin}
                ]
            response3 = openai.ChatCompletion.create(
                model=model_name, temperature=temperature, max_tokens = ewrds2,
                messages=messages3
                )
            for responses in response3.choices:
                generation3 = responses.message.content
            st.markdown(generation3)


if __name__ == '__main__':
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    main()
    
import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from typing import Dict, Union
import json
import prompts as pt

#keys
os.environ["OPENAI_API_KEY"] =st.secrets["OPENAI_API_KEY"]

#CONSTANTS
MODEL="gpt-4o-mini"

# set the openai model
llm = ChatOpenAI(model=MODEL, temperature=0)


#Function to check grammer and get suggestions to improve
def language_corrector(text: str) -> Dict[str, Union[str, list]]:
    """
    Analyzes text for grammatical errors in specified language.
    
    Args:
        text: Input text to analyze
        language: Target language for analysis (e.g., "French", "Spanish")
    
    Returns:
        Dictionary containing:
        {
            "original": str,
            "corrected": str,
            "errors": list[dict],
            "overall_feedback": str
        }
    """
    prompt = ChatPromptTemplate.from_template(pt.GRAMMAR_CHECKER_PROMPT)
    model=llm
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    try:
        response = chain.invoke({"text": text})
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse response",
            "raw_response": response
        }
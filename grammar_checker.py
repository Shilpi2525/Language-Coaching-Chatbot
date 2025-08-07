import streamlit as st
#from openai import OpenAI
#import os
#import json 
from utils import language_corrector 
#from langchain_core.prompts import ChatPromptTemplate
#from langchain_core.output_parsers import StrOutputParser
#from langchain_openai import ChatOpenAI
#import prompts as pt


def grammar_ui():


    # Page config
    st.title("Grammar Correction")
    st.markdown("Type a sentence, and I’ll help you fix any grammar mistakes!")

    # Input text
    user_input = st.text_area("Your sentence:")

    if st.button("Check My Sentence"):
        if not user_input.strip():
            st.warning("Please enter some text!")
        else:
            with st.spinner("Analyzing.."):
                result=language_corrector(user_input)

            if "error" in result:
                st.error(f"🚨 Error: {result['error']}")
            else:
                # Display results
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 📝 Original Text")
                    st.text(result.get("original", ""))
                with col2:
                    st.markdown(f"### 🌐 Language: {result.get('language', 'Unknown')}")
                    st.caption(f"Status: {result.get('status', 'unclear')}")
                
                # Handle different correction states
                corrected = result.get("corrected")
                if corrected == "Input Correct":
                    st.success("Perfect! No errors found.")
                elif corrected is None:
                    st.warning("Input unclear - couldn't analyze !!")
                else:
                    st.markdown("### ✅ Corrected Version")
                    st.success(corrected)
                
                # Show errors if any
                if result.get("errors"):
                    st.markdown("### 🔍 Found Errors")
                    for error in result["errors"]:
                        st.markdown(f"""
                        **{error.get('type', 'Error')}**  
                        `{error.get('original')}` → `{error.get('corrected')}`  
                        *Explanation*: {error.get('explanation')}
                        """)
                
                # Show additional notes
                if result.get("notes"):
                    st.markdown("### 📌 Notes")
                    for note in result["notes"]:
                        st.info(note)






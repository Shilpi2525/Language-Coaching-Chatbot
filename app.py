import streamlit as st
from PIL import Image
from grammar_checker import grammar_ui
from pronounciation_checker import pronounciation_feedback

# Configure page
st.set_page_config(
    page_title="Language Coaching Chatbot",
    page_icon="💬",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Learn with us")
page = st.sidebar.selectbox(
    "Choose an option",
    ["Select", "Grammar Correction"]
)

# Home/Intro Page
if page == "Select":
    col1, col2 = st.columns([1, 3])
    with col1:
        img = Image.open("background.jpeg")
        st.image(img, width=200)
    with col2:
        st.title("Language Coaching Chatbot")
        st.markdown("""
        **Improve your language skills with AI!**  
        ✍️ Get **grammar corrections**  
        🎤 Practice **pronunciation** with real-time feedback  
        🌍 Supports **multiple languages**  
        """)
    st.success("Select an option on the left.")

# Grammar Correction Page
elif page == "Grammar Correction":
    grammar_ui()

elif page=="Pronounciation Feedback":
    pronounciation_feedback()


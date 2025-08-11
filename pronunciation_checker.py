import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# --- API Configuration ---
API_BASE_URL = 'https://thefluent.me/api'


#keys
FLUENT_API_KEY =st.secrets["FLUENT_API_KEY"]
def get_auth_token():
    try:
        response = requests.get(
            "https://thefluent.me/api/swagger/login",
            headers={
                "x-api-key": st.secrets["FLUENT_API_KEY"],
                "accept": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json().get("token")
        else:
            st.error(f"API Response: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
        return None

'''
def get_auth_token():
    try:
        response = requests.get(
            f"{API_BASE_URL}/swagger/login",
            headers={"x-api-key": st.secrets["FLUENT_API_KEY"]},
            timeout=50  # Add timeout
        )
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json().get("token")
    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Failed: {str(e)}")
        return None

'''
# --- API Functions ---
def get_supported_languages():
    token = get_auth_token()
    if not token:
        return []
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_BASE_URL}/swagger/language", headers=headers)
        return response.json().get('supported_languages', []) if response.status_code == 200 else []
    except:
        return []

def create_post(language_id, text):
    token = get_auth_token()
    if not token:
        return None, None
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "post_language_id": int(language_id),
        "post_title": text[:50],
        "post_content": text
    }
    try:
        response = requests.post(f"{API_BASE_URL}/swagger/post", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('ai_reading'), data.get('post_id')
    except:
        pass
    return None, None

def score_pronunciation(post_id, audio_file):
    token = get_auth_token()
    if not token:
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (audio_file.name, audio_file, audio_file.type)}
    try:
        response = requests.post(
            f"{API_BASE_URL}/swagger/score/{post_id}",
            files=files,
            headers=headers
        )
        return response.json() if response.status_code == 200 else None
    except:
        return None

# --- Streamlit UI ---
def pronunciation_feedback():
    st.title("🎤 Pronunciation Coach")
    
    # Step 1: Language selection
    with st.spinner("Loading languages..."):
        languages = get_supported_languages()
    
    if not languages:
        st.error("Failed to load languages. Check your API key.")
        return
    
    lang_choice = st.selectbox(
        "Choose language/voice:",
        options=[f"{lang['language_name']} - {lang['language_voice']}" for lang in languages],
        format_func=lambda x: x.split(" - ")[0]
    )
    language_id = next(lang["language_id"] for lang in languages if f"{lang['language_name']} - {lang['language_voice']}" == lang_choice)

    # Step 2: Text input
    text = st.text_area("Enter text to practice (max 200 characters):", max_chars=200)
    if not st.button("Generate Model Pronunciation") or not text.strip():
        st.info("Enter text and click the button above")
        return

    # Step 3: Get AI pronunciation
    with st.spinner("Creating practice session..."):
        ai_audio_url, post_id = create_post(language_id, text)
    
    if not ai_audio_url:
        st.error("Failed to generate model pronunciation")
        return
    
    st.session_state.post_id = post_id
    st.audio(ai_audio_url, format="audio/mp3")
    st.success("Listen carefully, then record your attempt below")

    # Step 4: User recording and scoring
    st.divider()
    st.subheader("Your Attempt")
    audio_file = st.file_uploader("Upload your recording (MP3/WAV)", type=["mp3", "wav"])
    
    if audio_file and st.button("Get Pronunciation Score"):
        with st.spinner("Analyzing your pronunciation..."):
            scores = score_pronunciation(st.session_state.post_id, audio_file)
        
        if not scores:
            st.error("Scoring failed. Try again later.")
            return
        
        # Display results
        st.audio(audio_file, format=audio_file.type.split("/")[-1])
        overall = scores.get("overall_result_data", [{}])[0]
        words = scores.get("word_result_data", [])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Score", f"{overall.get('overall_points', 0)}/100")
        with col2:
            st.metric("Transcript Accuracy", f"{overall.get('transcript_accuracy', 0)}%")
        
        if words:
            st.subheader("Word-by-word Feedback")
            for word in words:
                st.progress(
                    word.get("points", 0)/100,
                    text=f"{word['word']}: {word['points']} pts (Speed: {word['speed']})"
                )


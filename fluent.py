import streamlit as st
import requests
import json


st.title('fluent api check')

# Configuration
API_BASE_URL = "https://thefluent.me/api"
#keys
FLUENT_API_KEY =st.secrets["FLUENT_API_KEY"]

def check_fluent():
    st.title('TheFluent.me API Health Check')

    with st.status("Running diagnostics...", expanded=True) as status:
        # Test 1: Authentication
        st.write("🔐 Testing authentication...")
        auth_response = requests.get(
            f"{API_BASE_URL}/swagger/login",
            headers={"x-api-key": FLUENT_API_KEY, "accept": "application/json"},
            timeout=10
        )
        
        if auth_response.status_code == 200:
            token = auth_response.json().get("token")
            st.success(f"✅ Authenticated (Token: ...{token[-6:]})")
            
            # Test 2: Language Endpoint
            st.write("🌐 Testing language endpoint...")
            lang_response = requests.get(
                f"{API_BASE_URL}/swagger/language",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10
            )
            
            if lang_response.status_code == 200:
                languages = lang_response.json()
                st.success(f"✅ Found {len(languages)} languages")
                st.json(languages[:2])  # Show first 2 as sample
            else:
                st.error(f"❌ Language fetch failed ({lang_response.status_code})")
                st.text(lang_response.text)
                
        elif auth_response.status_code == 401:
            st.error("❌ Invalid API key")
            st.link_button("Get New Key", "https://thefluent.me/api/register")
        else:
            st.error(f"❌ API Error ({auth_response.status_code})")
            st.text(auth_response.text)

        status.update(label="Diagnostics complete", state="complete")

    # Show raw responses
    with st.expander("Debug Details"):
        st.subheader("Authentication Response")
        st.code(f"""
        Status: {auth_response.status_code}
        Headers: {dict(auth_response.headers)}
        Body: {auth_response.text}
        """)
        
        if 'lang_response' in locals():
            st.subheader("Language Response")
            st.code(f"""
            Status: {lang_response.status_code}
            Headers: {dict(lang_response.headers)}
            Body: {lang_response.text}
            """)


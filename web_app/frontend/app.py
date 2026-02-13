import streamlit as st
import pandas as pd
import json
import sys
import os

# Add project root to sys.path to allow importing web_app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from web_app.logic import (
    get_levels, 
    get_random_word_logic, 
    update_progress_logic, 
    get_full_vocab_logic, 
    load_progress
)

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def init_session_state():
    if "current_word" not in st.session_state:
        st.session_state.current_word = None
    if "feedback" not in st.session_state:
        st.session_state.feedback = None
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

def fetch_random_word(level, retry_mode):
    word = get_random_word_logic(level, retry_mode)
    if word:
        st.session_state.current_word = word
        st.session_state.feedback = None
        st.session_state.user_input = ""
        return True
    else:
        st.info("No words found (or no incorrect words to retry)!")
        return False

def check_answer(level):
    if not st.session_state.current_word:
        return

    word_data = st.session_state.current_word
    user_meaning = st.session_state.user_input.strip()
    correct_meaning = word_data["meaning"]

    if not user_meaning:
        st.warning("Please enter a meaning!")
        return

    # Basic substring matching
    if user_meaning in correct_meaning or correct_meaning in user_meaning:
        st.session_state.feedback = "correct"
        status = "correct"
        st.balloons()
    else:
        st.session_state.feedback = "incorrect"
        status = "incorrect"

    # Update Progress
    update_progress_logic(level, word_data["word"], status)

import io
from gtts import gTTS

def play_audio(text):
    try:
        # Generate Audio with gTTS
        with st.spinner("Generating audio..."):
            tts = gTTS(text=text, lang='ja')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            
            # Check if data was actually written
            if audio_fp.getbuffer().nbytes == 0:
                st.error("TTS Error: No audio data generated.")
                return

        # Play Audio
        st.audio(audio_fp, format='audio/mp3', autoplay=True)
        
    except Exception as e:
        st.error(f"TTS Error: {e}")
        # Detailed log for debugging
        print(f"TTS Failed: {e}")

def main():
    st.set_page_config(page_title="Cute Japanese Learning", page_icon="🌸", layout="centered")
    load_css()
    init_session_state()

    st.title("🌸 Japanese Learning App 🌸")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        levels = get_levels()
        if not levels:
            levels = ["n5"] # Fallback
        
        selected_level = st.selectbox("Select Level", levels, index=0)
        
        mode = st.radio("Mode", ["📚 Start Learning", "📝 Review List"])

        st.markdown("---")
        retry_mode = st.checkbox("Retry Incorrect Words Only")

    # --- Learning Mode ---
    if mode == "📚 Start Learning":
        
        # "Next Word" Logic
        if st.session_state.current_word is None:
             if st.button("Start Quiz", use_container_width=True):
                 fetch_random_word(selected_level, retry_mode)
                 st.rerun()
        
        if st.session_state.current_word:
            word = st.session_state.current_word
            
            # Card Display
            st.markdown(f"""
            <div class="word-card">
                <div class="japanese-text">{word['word']}</div>
                <div class="reading-text">{word['reading']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Audio Button
            if st.button("🔊 Listen"):
                play_audio(word["reading"])

            # Input Form
            with st.form("quiz_form", clear_on_submit=False):
                st.text_input("Meaning (Korean):", key="user_input")
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Check Answer", use_container_width=True, on_click=check_answer, args=(selected_level,))
                with col2:
                    # Next button clears state and fetches new via callback
                    st.form_submit_button("Next Word ➡️", use_container_width=True, on_click=fetch_random_word, args=(selected_level, retry_mode))

            # Feedback Display
            if st.session_state.feedback == "correct":
                st.success("Correct! (정답) 🎉") 
            elif st.session_state.feedback == "incorrect":
                st.error(f"Incorrect. Answer: {word['meaning']}")

    # --- Review Mode ---
    else:
        st.subheader(f"📝 Review List ({selected_level.upper()})")
        
        vocab_list = get_full_vocab_logic(selected_level)
        progress = load_progress()
        level_progress = progress.get(selected_level, {})
        
        if vocab_list:
            table_data = []
            for item in vocab_list:
                status = level_progress.get(item["word"], "Not Attempted")
                table_data.append({
                    "Word": item["word"],
                    "Reading": item["reading"],
                    "Meaning": item["meaning"],
                    "Status": status
                })
            
            df = pd.DataFrame(table_data)
            
            filter_status = st.multiselect("Filter by Status", ["correct", "incorrect", "Not Attempted"], default=["correct", "incorrect", "Not Attempted"])
            
            if filter_status:
                df = df[df["Status"].isin(filter_status)]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No vocabulary data loaded.")

if __name__ == "__main__":
    main()

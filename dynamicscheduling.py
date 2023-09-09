#!/usr/bin/env python
# coding: utf-8

# In[2]:


#pip install pyaudio


# In[3]:


import streamlit as st
import speech_recognition as sr
import pyttsx3

# Initialize speech recognition
r = sr.Recognizer()

# Initialize text-to-speech with female voice (you can choose the desired voice name)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voice_id = None
for voice in voices:
    if "female" in voice.name.lower():  # Look for a female voice
        female_voice_id = voice.id
        break
if female_voice_id:
    engine.setProperty('voice', female_voice_id)

# Initialize session state
if 'engine_initialized' not in st.session_state:
    st.session_state.engine_initialized = False

# Set page title and subtitle
st.title("Interview Scheduling AI")
st.markdown(
    """
    <div style='text-align: center;'><h4>Dynamic Conversational AI</h4></div>
    """,
    unsafe_allow_html=True
)

# Get candidate information
candidate_name = st.text_input("Your Name")
candidate_phone = st.text_input("Your Phone Number")

# Process button
click = st.button("Start Interview")

# Add event handler to stop the engine when the page is refreshed
if st.session_state.engine_initialized:
    engine.stop()
st.session_state.engine_initialized = True

if click:
    engine.say(f"Hello I am urjja from NTT Data business Solution hiring Team looking for a position.")
    engine.runAndWait()

    # Introduction
    engine.say(f"Hello, {candidate_name}! Welcome to the interview scheduling process.")
    engine.runAndWait()

    # Ask if the candidate is interested in the position
    engine.say("Are you interested in the position? Please respond with 'yes' or 'no'.")
    engine.runAndWait()

    interested_response = ""
    while not interested_response:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            interested_response = r.recognize_google(audio)
        except sr.UnknownValueError:
            engine.say("Sorry, I didn't catch that. Please respond with 'yes' or 'no'.")
            engine.runAndWait()

    if "yes" in interested_response.lower():
        engine.say("Great! Let's proceed with the interview scheduling.")
        engine.runAndWait()

        # Gather interview details
        engine.say("Please provide the position you applied for.")
        engine.runAndWait()
        position = ""
        while not position:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            try:
                position = r.recognize_google(audio)
            except sr.UnknownValueError:
                engine.say("Sorry, I didn't catch that. Please repeat the position you applied for.")
                engine.runAndWait()

        engine.say(f"Thank you for applying for the position of {position}.")
        engine.runAndWait()

        engine.say("Please let me know your preferred date and time for the interview.")
        engine.runAndWait()
        date_time = ""
        while not date_time:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            try:
                date_time = r.recognize_google(audio)
            except sr.UnknownValueError:
                engine.say("Sorry, I didn't catch that. Please repeat your preferred date and time.")
                engine.runAndWait()

        engine.say("Thank you for providing the interview schedule. We will contact you shortly with the confirmation details.")
        engine.runAndWait()

        # End of interview
       

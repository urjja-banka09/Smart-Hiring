#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import openai
import pyttsx3
import speech_recognition as sr

# Initialize OpenAI API
# openai.api_key = "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"
openai.api_key = "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"

# Initialize speech recognition
r = sr.Recognizer()

# Initialize text-to-speech with a female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voice_id = None
for voice in voices:
    if "female" in voice.name.lower():
        female_voice_id = voice.id
        break
if female_voice_id:
    engine.setProperty('voice', female_voice_id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_candidate_response():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        response = r.recognize_google(audio)
        return response
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please repeat your response.")
        return get_candidate_response()

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7):
    messages = [
        {"role": "system", "content": "You are an interviewer.\n"},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

def main():
    candidate_name = "John"  # Replace with actual candidate's name
    conversation = []

    # Step 1: Initiate conversation
    initial_question = f"Hello {candidate_name},i'm urjja from NTT Data business solution hiring team, how was your day?"
    speak(f"{initial_question}")
    candidate_response = get_candidate_response()
    conversation.append(f"Interviewer: {initial_question}\nCandidate: {candidate_response}")

    # Step 2: Ask for introduction
    introduction_prompt = "Please introduce yourself."
    speak(f"{introduction_prompt}")
    candidate_response = get_candidate_response()
    conversation.append(f"Interviewer: {introduction_prompt}\nCandidate: {candidate_response}")

    # Step 3: Generate and ask multiple follow-up questions about hobbies, interests, etc.
    follow_up_questions = [
        "okay,What are your hobbies and interests outside of work?",
        "thats great ,Tell me about a project or activity you're passionate about.",
        "great,Do you have any favorite books, movies, or sports?",
    ]

    for follow_up_question in follow_up_questions:
        speak(f"{follow_up_question}")
        candidate_response = get_candidate_response()
        conversation.append(f"Interviewer: {follow_up_question}\nCandidate: {candidate_response}")

    # Step 4: Transition to technical round
    technical_round_prompt = "Great! Let's move on to the technical round."
    speak(f"{technical_round_prompt}")

    # Part 2: Technical Round
    position = 'software engineer'
    follow_up_count = 0
    question = f"Can you describe a challenging  project you have worked on and how you approached solving it?"
    speak(f"{question}")
    conversation.append(f"Interviewer: {question}")
    candidate_response = get_candidate_response()
    conversation.append(f"Candidate: {candidate_response}")
    while follow_up_count < 3:
        question = get_completion(candidate_response)
        #     engine="davinci",
        #     prompt=f"Interviewer: {candidate_response}\n",
        #     max_tokens=50
        # ).choices[0].text
        speak(f"{question}")
        conversation.append(f"Interviewer: {question}")
        candidate_response = get_candidate_response()
        conversation.append(f"Candidate: {candidate_response}")
        follow_up_count += 1

    if len(conversation) >= 7:
        speak("Do you have any questions or queries for us?")
        candidate_questions = get_candidate_response()
        conversation.append(f"Candidate: {candidate_questions}")
        speak("Thank you for your time, the interview has concluded.")

if __name__ == "__main__":
    main()


#!/usr/bin/env python
# coding: utf-8
# In[1]:
#pip install transformers
# In[2]:
#pip install torch
# In[3]:
import streamlit as st
import os
import glob
import pdfplumber
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import torch



# Set page configuration
st.set_page_config(page_title="Automated Resume Screening", layout="wide")

# Set sidebar width
st.markdown(
    """
    <style>
    .reportview-container .sidebar .sidebar-content {
        width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set page title and subtitle
st.title("Automated Resume Screening")
# st.markdown(
#     """
#     <div style='text-align: center;'><h4>NLP Based Resume Screening</h4></div>
#     """,
#     unsafe_allow_html=True
# )

# File upload section
uploadedJD = st.file_uploader("Upload Job Description", type="pdf")
uploadedResumes = st.file_uploader("Upload Resumes (Multiple PDFs)", accept_multiple_files=True)

# Process button
click = st.button("Process")

# Check if files are uploaded and button is clicked
if uploadedJD and uploadedResumes and click:
    # Extract text from the job description
    try:
        with pdfplumber.open(uploadedJD) as pdf:
            pages = pdf.pages[0]
            job_description = pages.extract_text()
    except:
        st.error("Error extracting text from the job description")

    # Load the BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # Get embeddings for the job description
    job_description_tokens = tokenizer(job_description, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        job_description_outputs = model(**job_description_tokens)

    job_description_embeddings = job_description_outputs.last_hidden_state[:, 0, :]

    # Process each resume
    results = []
    for resume_file in uploadedResumes:
        try:
            with pdfplumber.open(resume_file) as pdf:
                resume_text = ""
                for page in pdf.pages:
                    resume_text += page.extract_text()

            # Get embeddings for the resume
            resume_tokens = tokenizer(resume_text, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                resume_outputs = model(**resume_tokens)

            resume_embeddings = resume_outputs.last_hidden_state[:, 0, :]

            # Calculate the cosine similarity between job description and resume embeddings
            similarity = cosine_similarity(job_description_embeddings, resume_embeddings).item() * 100
            results.append((resume_file.name, similarity))

        except Exception as e:
            st.error(f"Error processing {resume_file.name}: Invalid or corrupted PDF file {e}")

    # Create a dataframe with the results
    df = pd.DataFrame(results, columns=["Resume", "Match Percentage"])
    df.sort_values("Match Percentage", ascending=False, inplace=True)
    df.reset_index(drop=True,inplace=True)

    # Display the dataframe
    st.dataframe(df)


# In[ ]:





Here is the README.md file in markdown format for the given code:

**ATS Keyword Scanner App**
==========================

**Overview**
-----------

This app is a keyword scanner for ATS (Applicant Tracking System) resumes. It uses the Google Generative AI model to generate keywords for a given job role and level, and then compares them with the keywords extracted from a uploaded PDF resume.

**Files**
--------

### app.py

This is the main application file. It imports the necessary libraries, sets up the Streamlit app, and defines the functions for extracting keywords from the uploaded PDF file and generating keywords for the job role and level using the Google Generative AI model.

### requirements.txt

This file lists the dependencies required to run the app. It includes the following packages:

* langchain_google_genai==1.0.6
* numpy==1.25.2
* pypdf==4.2.0
* streamlit==1.35.0

**How to Use**
--------------

1. Upload a PDF resume file using the file uploader.
2. Enter the job role and select the level (Internship or Entry Level) using the text input and selectbox.
3. Click the "Submit" button to start the keyword scanning process.
4. The app will display the ATS score based on the keyword analysis, as well as suggestions for missing keywords.

**Note**
-----

This app uses the Google Generative AI model to generate keywords, which may require a Google API key to function properly.

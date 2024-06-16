import numpy as np
import re
import json
import streamlit as st
from pypdf import PdfReader
from langchain_google_genai import GoogleGenerativeAI
# from st_circular_progress import CircularProgress
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets['GOOGLE_AI'])
st.header("ATS(keyword scanner)")
st.set_page_config(layout="wide")
file_upload = st.file_uploader("Upload a file", type=["pdf"])
def get_key_dict(words):
    w=re.findall('\{[^{}]*\}',words)
    key_data=json.loads(w[0])
    arr = list(key_data.values())
    n1 = np.array(arr, dtype=object)
    flat_array = np.concatenate(arr).flatten()
    final_set=[]
    for i in flat_array:
        if len(i)>0:
          arr=i.split(' ')
          # st.write(arr)
          for k in arr:
            if len(k)>0 and any(chr.isdigit() for chr in k)==False:
              final_set.append(k.lower().replace('(','').replace(')',''))
    no_count = [
        "about", "above", "across", "after", "against",
        "along", "amid", "among", "around", "at",
        "before", "behind", "below", "beneath", "beside",
        "between", "beyond", "by", "down", "during",
        "for", "from", "in", "inside", "into",
        "near", "of", "off", "on", "out",
        "outside", "over", "past", "through", "to",
        "toward", "under", "underneath", "until", "up",
        "upon", "with", "within","the", "an", "a", "and", "but", "or", "nor", "yet", "so",
        "although", "because", "since",
        "unless", "until","while"
    ]
    final_set=list(set(final_set))
    
    compare_dict=dict()
    for i in final_set:
      if i not in no_count:
        compare_dict[i]=compare_dict.get(i,0)+1
    # st.write(compare_dict)
    return compare_dict
# @st.experimental_fragment
def get_job_keywords(job,level_option):
  if level_option and level_option=="Internship" and job :
    #  words=llm.invoke(f"Give keywords for the resume for an {level_option} in {job} role in three section the response should be in json format 'Work experience',''projects','skills'")
     words=llm.invoke(f"Give keywords for the resume for an {level_option} in {job} role in three section the response should be in json format 'Work experience',''projects','skills'")
     compare_dict=get_key_dict(words)
     return compare_dict
  elif level_option and level_option=="Entry Level" and job:
    words=llm.invoke(f"Give keywords for the resume for an {level_option} in {job} role in three section the response should be in json format 'Work experience',''projects','skills'")
    compare_dict=get_key_dict(words)
    return compare_dict




if file_upload is not None:
    pdf_reader = PdfReader(file_upload)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    if len(text) >0:
      text_split=text.split('\n')
      user_words=[]
      for i in text_split:
        arr=i.split(' ')
        for j in arr:
          if len(j)>0:
            user_words.append(j.lower())
      if len(user_words)>0:
        user_words=list(set(user_words))
        job=st.text_input("Enter The Job Role : ")
        level_option=st.selectbox("Select the level of your role : ",("Internship","Entry Level"),index=None,
        placeholder="Select The Job Level...",)
        but=st.button("Submit")
        if but:
          with st.spinner("Scanning plz wait..."):
            ATS_score=0
            all_missing_words=''''''
            missing_words=[]
            for i in range(0,3):
              st.session_state.compare_dict=get_job_keywords(job,level_option)
              if "compare_dict" in st.session_state:
                compare_dict=st.session_state.compare_dict
                for i in user_words:
                  if i in compare_dict.keys():
                    compare_dict[i]=compare_dict.get(i)+1
                user_points=0

                for i in compare_dict.keys():
                  if compare_dict[i]>1:
                    user_points+=1
                  else:
                    missing_words.append(i)
                total_points=len(list(compare_dict.keys()))
                user_score=(user_points/total_points)*100
                ATS_score+=user_score

            st.session_state.net_score=ATS_score/3
            missing_words=list(set(missing_words))
            c=0;
            st.markdown("# ATS Score(based on keyword analysis)")
            if "net_score" in st.session_state:
              net_score=st.session_state.net_score
              st.markdown(f"## {net_score}/100")
            for i in missing_words:
              c+=1
              all_missing_words+=i+", "
              if c%4==0:
                all_missing_words+='\n'
            c1=st.columns(1)
            with c1[0]:
              c2=st.container(border=True)
              c2.header("Suggestions for Keywords")
              c2.code(all_missing_words,language='md')


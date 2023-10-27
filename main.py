import streamlit as st
from streamlit_option_menu import option_menu
import openai
import PyPDF2

openai.api_key = " " #yourkey

def generate_question(corpus,complexity,noq,type):
    prompt = f"""Generate {noq} questions from {corpus} with {complexity} level of complexity of {type} type"""
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3 engine
        prompt=prompt,
        max_tokens=1000  # Adjust based on desired question length
    )
    return response.choices[0].text.strip()

def generate_question1(corpus,type):
    prompt = f"""summarize the {corpus} and give output in {type} format"""
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3 engine
        prompt=prompt,
        max_tokens=1000  # Adjust based on desired question length
    )
    return response.choices[0].text.strip()


st.title("Question Wringer")

col1,col2,col3, col4,col5=st.columns(5)
pdf=col3.toggle("With PDF")

with st.sidebar:
    selected = option_menu(
        menu_title="Teacher Tools",
        options=['Question Generator',"Summarizer"],
        icons=['check-square-fill'],
    )
text=''
if selected=="Question Generator":

    if pdf:
        with st.form(key='my_form1'):
            upload_file=st.file_uploader("Upload PDF", type='pdf')
            text=''
            if upload_file:
                pdffile = open(f'C:/Users/pusal/Downloads/{str(upload_file.name)}', 'rb')
                pdfreader = PyPDF2.PdfReader(pdffile)
                pobj = len(pdfreader.pages)
                for i in range(pobj-2):
                    pageobj = pdfreader.pages[i]
                    text = text + pageobj.extract_text()

            diff=st.selectbox("Level of Difficulty",['Easy','Medium','Hard'])
            col1,col2=st.columns(2)
            type=col1.selectbox("Question Format",['Multiple Choice','True or False','Open Question'])
            noq=col2.slider("# Questions",1,50,25)
            button=st.form_submit_button("Generate")
        if button:
            st.write("Generated Questions")
            st.write(generate_question(text,diff,noq,type))


    else:

        with st.form(key='my_form'):
            text=st.text_area("Corpus Here")
            diff=st.selectbox("Level of Difficulty",['Easy','Medium','Hard'])
            col1,col2=st.columns(2)
            type=col1.selectbox("Question Format",['Multiple Choice','True or False','Open Question'])
            noq=col2.slider("# Questions",1,50,25)
            button=st.form_submit_button("Generate")
        if button:
            st.write("Generated Questions")
            st.write(generate_question(text,diff,noq,type))

if selected=='Summarizer':
    with st.form(key='my_form3'):
        text = st.text_area("Corpus Here")
        diff = st.selectbox("Output", ["paragraph",'Bullet Points'])
        button=st.form_submit_button("Summarize")
        if button:
            st.write(generate_question1(text,diff))

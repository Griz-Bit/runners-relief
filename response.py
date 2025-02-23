from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from global_vars import CHROMA_PATH, PROMPT_TEMPLATE_QUERY, PROMPT_TEMPLATE_DIAGNOSIS
from dotenv import load_dotenv
import argparse
import openai
import os

# load api key as environment variable
load_dotenv()

openai.api_key = os.environ['API_KEY']

def respond_query(query_text, chat_history):
    # load db of uploaded file
    embedding_function = OpenAIEmbeddings(api_key=os.environ['API_KEY'])
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # find relevant data in db
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print("No relevant data was found in the text.")
        return
    
    history = " ".join(chat_history).replace("/n", " ")
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_QUERY)
    prompt = prompt_template.format(context=context_text, query=query_text, history=history)
    print(prompt)

    model = ChatOpenAI(api_key=openai.api_key)
    response_text = model.predict(prompt)

    return response_text

def diagnose_injury(query_text, chat_history):
    # load db of uploaded file
    embedding_function = OpenAIEmbeddings(api_key=os.environ['API_KEY'])
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # find relevant data in db
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"No relevant data was found in the text.")
        return
    
    history = " ".join(chat_history).replace("/n", " ")

    print(history)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_DIAGNOSIS)
    prompt = prompt_template.format(context=context_text, query=query_text, history=history)
    print(prompt)

    model = ChatOpenAI(api_key=os.environ['API_KEY'])
    response_text = model.predict(prompt)

    # print(response_text)

    injury, accuracy = split_injury_percentage(response_text)

    return injury, accuracy

def split_injury_percentage(text):
    s = text.split('--')
    injuries = []
    accuracies = []
    for i in range(len(s)):
        splits = s[i].split('++')
        injuries.append(splits[0])
        accuracies.append(splits[1])
    return injuries, accuracies
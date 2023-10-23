# Student Financial Aid Chatbot
## Overview

This repository contains an AI Chatbot designed to assist students and parents in obtaining information on student financial aid, particularly focusing on the Free Application for Federal Student Aid (FAFSA). The chatbot has been developed to provide helpful answers to common student financial aid-related questions.
Features

* Data Collection: The chatbot collects documents from the official fafsa.gov and Department of Education websites.

* Document Splitting: The Langchain document splitter is used to process and split the collected documents into smaller, manageable pieces.

* Vector Store: Document embeddings are efficiently stored in Azure blob storage and seamlessly retrieved from the same location through the FAISS vector store.

* Document ChatApp: The chatbot utilizes the split documents to create a Document ChatApp. This is a user-friendly interface where students can seek information and answers related to student financial aid.

* LLM: The llm used for this project is the OpenAI gpt-3.5-turbo model.

* QA Retrieval: The Langchain library is leveraged for Question-Answer (QA) retrieval, enabling the chatbot to deliver precise responses to user inquiries. Through similarity search, the chatbot utilizes the top 2 most pertinent documents to generate the query output.

* Memory Enhancement: The chatbot incorporates memory to improve the speed and efficiency of answer retrieval. This memory feature helps maintain context during interactions.

* Streamlit-Powered: The chatbot is built using Streamlit, a popular Python library for creating web applications with minimal effort. The user interface is designed to be intuitive and accessible.

* Cloud Hosting: The chatbot is hosted on the Streamlit Community Cloud, ensuring its accessibility to a wider audience.

## How to Use

Please access chatbot via: https://fafsachatapp.streamlit.app/

## Deployment

You can deploy the chatbot locally by following these steps:

* Clone this repository to your local machine.

* Ensure you have the required Python packages and dependencies installed. You can use the provided requirements.txt file to set up the environment.

* Follow the instructions in create_embeddings.ipynb to generate the vector embeddings store. This store is used to serve vector embeddings via Azure blob storage using FAISS vector store.

* Run the chatbot script, which is typically a Python file using Streamlit.

* Open your web browser and navigate to the provided local URL to interact with the chatbot.


## Application Tutorial
![Image Description](https://github.com/saldanhad/fafsachatbot/blob/main/miscellaneous/app_tutorial.gif?raw=true)

## Application Architecture
![Image Description](https://github.com/saldanhad/fafsachatbot/blob/main/miscellaneous/app%20workflow.jpg?raw=true)

## Save chat history to preserve query context
![Image Description](https://github.com/saldanhad/fafsachatbot/blob/main/miscellaneous/conversional%20chain%20with%20memory.png)

## Framework for model fine tuning. 
We capture user feedback for each prompt with the goal of creating a dataset that can be employed for fine-tuning an open-source LLM model, thereby reducing reliance on the OpenAI LLM.

![Image Description](https://github.com/saldanhad/fafsachatbot/blob/main/miscellaneous/feedbacktodb.jpg?raw=true)


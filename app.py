import streamlit as st
import os
import openai
from auth.auth import login, logout, is_logged_in

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["default"]["openai_api_key"]

# Document directory
DOC_DIR = 'documents'

# Create the documents directory if it does not exist
if not os.path.exists(DOC_DIR):
    os.makedirs(DOC_DIR)

# Function to read documents
def read_documents():
    documents = {}
    for filename in os.listdir(DOC_DIR):
        filepath = os.path.join(DOC_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            documents[filename] = file.read()
    return documents

# Function to chat with documents
def chat_with_documents(question):
    documents = read_documents()
    context = "\n\n".join(documents.values())
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message['content']

# Authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def attempt_login():
    username = st.session_state.username_input
    password = st.session_state.password_input
    if login(username, password):
        st.success('Logged in successfully')
        st.experimental_rerun()
    else:
        st.error('Invalid credentials')

if not is_logged_in():
    st.title('Admin Login')
    username = st.text_input('Username', key='username_input')
    password = st.text_input('Password', type='password', key='password_input')
    if st.button('Login'):
        attempt_login()
else:
    st.sidebar.title('Admin')
    if st.sidebar.button('Logout'):
        logout()
        st.experimental_rerun()

    st.title('Document Management')

    # File upload
    uploaded_files = st.file_uploader("Upload Documents", type=['txt', 'pdf'], accept_multiple_files=True)
    if st.button('Add Documents'):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                with open(os.path.join(DOC_DIR, uploaded_file.name), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
            st.success('Files uploaded successfully')
            st.experimental_rerun()

    # List documents
    st.subheader('Documents in Storage')
    documents = os.listdir(DOC_DIR)
    if documents:
        for doc in documents:
            st.write(doc)
            if st.button(f'Remove {doc}', key=doc):
                os.remove(os.path.join(DOC_DIR, doc))
                st.success(f'{doc} removed successfully')
                st.experimental_rerun()
    else:
        st.write("No documents found.")

    # Train button (Placeholder for actual training function)
    if st.button('Train'):
        st.write('Training function called...')
        # Placeholder: Call your actual training function here
        st.success('Training completed')

    st.title('Chat with Documents')
    question = st.text_input('Ask a question about the documents:')
    if question:
        answer = chat_with_documents(question)
        st.write(f'Answer: {answer}')


# import streamlit as st
# import os
# import openai
# from auth.auth import login, logout, is_logged_in

# # Set your OpenAI API key from Streamlit secrets
# openai.api_key = st.secrets["default"]["openai_api_key"]

# # Document directory
# DOC_DIR = 'documents'

# # Create the documents directory if it does not exist
# if not os.path.exists(DOC_DIR):
#     os.makedirs(DOC_DIR)

# # Function to read documents
# def read_documents():
#     documents = {}
#     for filename in os.listdir(DOC_DIR):
#         filepath = os.path.join(DOC_DIR, filename)
#         with open(filepath, 'r', encoding='utf-8') as file:
#             documents[filename] = file.read()
#     return documents

# # Function to chat with documents
# def chat_with_documents(question):
#     documents = read_documents()
#     context = "\n\n".join(documents.values())
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
#         ]
#     )
#     return response.choices[0].message['content']

# # Authentication
# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False

# if not is_logged_in():
#     st.title('Admin Login')
#     username = st.text_input('Username')
#     password = st.text_input('Password', type='password')
#     if st.button('Login'):
#         if login(username, password):
#             st.success('Logged in successfully')
#         else:
#             st.error('Invalid credentials')
# else:
#     st.sidebar.title('Admin')
#     if st.sidebar.button('Logout'):
#         logout()

#     st.title('Document Management')

#     # File upload
#     uploaded_files = st.file_uploader("Upload Documents", type=['txt', 'pdf'], accept_multiple_files=True)
#     if st.button('Add Documents'):
#         if uploaded_files:
#             for uploaded_file in uploaded_files:
#                 with open(os.path.join(DOC_DIR, uploaded_file.name), 'wb') as f:
#                     f.write(uploaded_file.getbuffer())
#             st.success('Files uploaded successfully')
#             st.experimental_rerun()

#     # List documents
#     st.subheader('Documents in Storage')
#     documents = os.listdir(DOC_DIR)
#     if documents:
#         for doc in documents:
#             st.write(doc)
#             if st.button(f'Remove {doc}', key=doc):
#                 os.remove(os.path.join(DOC_DIR, doc))
#                 st.success(f'{doc} removed successfully')
#                 st.experimental_rerun()

#     # Train button (Placeholder for actual training function)
#     if st.button('Train'):
#         st.write('Training function called...')
#         # Call your training function here
#         st.success('Training completed')

#     st.title('Chat with Documents')
#     question = st.text_input('Ask a question about the documents:')
#     if question:
#         answer = chat_with_documents(question)
#         st.write(f'Answer: {answer}')

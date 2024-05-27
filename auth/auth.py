import streamlit as st

# Debug: Print the contents of st.secrets
st.write(st.secrets)

def login(username, password):
    st.write("Attempting login with:", username, password)
    st.write("Stored admin_username:", st.secrets["default"]["admin_username"])
    st.write("Stored admin_password:", st.secrets["default"]["admin_password"])
    if username == st.secrets["default"]["admin_username"] and password == st.secrets["default"]["admin_password"]:
        st.session_state['logged_in'] = True
        return True
    else:
        st.session_state['logged_in'] = False
        return False

def logout():
    st.session_state['logged_in'] = False

def is_logged_in():
    return st.session_state.get('logged_in', False)

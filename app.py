import streamlit as st
import os
import json
from functions import main,registered_admin_users,registered_non_admin_users,validate_password

def json_file_exists(file_path):
    return os.path.exists(file_path)

if json_file_exists("data.json") == False:
    with open("data.json", "w") as f:
        json.dump([], f)

st.title("Friends Money Pool - Badminators")
# Create an empty container
placeholder = st.empty()

if 'email' not in st.session_state:
    # Insert a form in the container

    with open("hashed_passwords.json", "r") as f:
        hashed_passwords = json.load(f)
    registered_admin_password = hashed_passwords['registered_admin_password']
    registered_non_admin_password = hashed_passwords['registered_non_admin_password']

    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        email = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if (email in registered_admin_users and validate_password(password, registered_admin_password)) or (email in registered_non_admin_users and validate_password(password, registered_non_admin_password)):
            # If the form is submitted and the email and password are correct,
            # clear the form/container and display a success message
            placeholder.empty()
            st.session_state.email = email
            st.session_state.password = password
            st.success(f"Welcome {st.session_state.email.capitalize()}")
            main()
        else:
            st.error("Username/Password Incorrect")         
else:
    main()









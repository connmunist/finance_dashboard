import streamlit as st
from database import initialize_database

initialize_database()
st.write("Database initialized")
import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Page setup
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")

# Load config for authentication
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Setup the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Login widget
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:

    authenticator.logout('Logout', 'sidebar')
    st.sidebar.success(f"Welcome, {name}!")

    # Sidebar menu
    with st.sidebar:
        selected = option_menu(
            'Disease Prediction System',
            ['Heart Disease Prediction'],
            menu_icon='hospital-fill',
            icons=['heart'],
            default_index=0
        )

    # Load ML model
    working_dir = os.path.dirname(os.path.abspath(__file__))
    heart_disease_model = pickle.load(open(os.path.join(working_dir, 'heart_disease_model.sav'), 'rb'))

    # Heart Disease Prediction Page
    if selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction using ML')

        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')
        with col2:
            sex = st.text_input('Sex')
        with col3:
            cp = st.text_input('Chest Pain types')
        with col1:
            trestbps = st.text_input('Resting Blood Pressure')
        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')
        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')
        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')
        with col3:
            exang = st.text_input('Exercise Induced Angina')
        with col1:
            oldpeak = st.text_input('ST depression induced by exercise')
        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')
        with col3:
            ca = st.text_input('Major vessels colored by flourosopy')
        with col1:
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

        heart_diagnosis = ''

        if st.button('Heart Disease Test Result'):
            try:
                user_input = [float(x) for x in [age, sex, cp, trestbps, chol, fbs, restecg,
                                                 thalach, exang, oldpeak, slope, ca, thal]]
                heart_prediction = heart_disease_model.predict([user_input])
                if heart_prediction[0] == 1:
                    heart_diagnosis = 'The person is having heart disease'
                else:
                    heart_diagnosis = 'The person does not have any heart disease'
            except ValueError:
                st.error("Please enter valid numeric inputs.")
        st.success(heart_diagnosis)

elif authentication_status is False:
    st.error("Username or password is incorrect.")
elif authentication_status is None:
    st.warning("Please enter your username and password.")

# Registration
try:
    if authenticator.register_user('Register', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)

# Forgot Password
try:
    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
    if username_forgot_pw:
        st.success(f"A new password was generated for {username_forgot_pw}: {random_password}")
        # Send it via secure channel in production
    else:
        st.error('Username not found')
except Exception as e:
    st.error(e)

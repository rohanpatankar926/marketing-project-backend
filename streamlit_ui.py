import streamlit as st
import requests

BASE_URL = "https://marketing-project-backend.onrender.com"

st.title("User Management System")

st.header("Health Check")
if st.button("Check Server Health"):
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        st.success(response.json())
    else:
        st.error("Failed to connect to the server.")

st.header("Sign Up")
signup_first_name = st.text_input("First Name")
signup_last_name = st.text_input("Last Name")
signup_email = st.text_input("Signup Email")
signup_password = st.text_input("Signup Password", type="password")
if st.button("Sign Up"):
    signup_payload = {
        "first_name": signup_first_name,
        "last_name": signup_last_name,
        "email_id": signup_email,
        "password": signup_password,
    }
    response = requests.post(f"{BASE_URL}/sign_up", json=signup_payload)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(response.json()["message"])

st.header("Verify OTP")
verify_email = st.text_input("Verify Email")
verify_otp = st.text_input("OTP Code")
verify_first_name = st.text_input("First Name", key="verify_fname")
verify_last_name = st.text_input("Last Name", key="verify_lname")
verify_password = st.text_input("Password", type="password", key="verify_password")
if st.button("Verify OTP"):
    verify_payload = {
        "first_name": verify_first_name,
        "last_name": verify_last_name,
        "email_id": verify_email,
        "password": verify_password,
        "otp": verify_otp,
    }
    response = requests.post(f"{BASE_URL}/verify_otp", json=verify_payload)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(response.json()["message"])

st.header("Login")
login_email = st.text_input("Email")
login_password = st.text_input("Password", type="password")
if st.button("Login"):
    login_payload = {
        "email_id": login_email,
        "password": login_password
    }
    response = requests.post(f"{BASE_URL}/login", json=login_payload)
    if response.status_code == 200:
        st.success({"user_id":response.json()["user_id"]})
    else:
        st.error(response.json()["message"])


st.header("Connect Sender Email")
connect_user_id = st.text_input("User ID", key="connect_user_id")
connect_sender_email = st.text_input("Sender Email")
connect_password = st.text_input("Sender Password", type="password")
if st.button("Connect Sender"):
    connect_payload = {
        "user_id": connect_user_id,
        "sender_email": connect_sender_email,
        "password": connect_password,
    }
    response = requests.post(f"{BASE_URL}/connect_sender", json=connect_payload)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(response.json()["message"])

st.header("Schedule Email")
schedule_user_id = st.text_input("User ID", key="schedule_user_id")
schedule_sender_email = st.text_input("Sender Email", key="schedule_sender_email")
schedule_subject = st.text_input("Email Subject")
schedule_body = st.text_area("Email Body")
schedule_doc_id = st.text_input("Document ID")
schedule_time = st.text_input("Send Time (HH:MM)")
schedule_days = st.multiselect("Days", options=["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
if st.button("Schedule Email"):
    schedule_payload = {
        "user_id": schedule_user_id,
        "sender_email": schedule_sender_email,
        "subject": schedule_subject,
        "body": schedule_body,
        "doc_id": schedule_doc_id,
        "time": schedule_time,
        "days": schedule_days,
    }
    response = requests.post(f"{BASE_URL}/schedule_email", json=schedule_payload)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(response.json()["message"])

st.header("Get Connected Emails")
get_emails_user_id = st.text_input("User ID", key="get_emails_user_id")
if st.button("Get Connected Emails"):
    response = requests.get(f"{BASE_URL}/get_connected_emails", params={"user_id": get_emails_user_id})
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("Failed to fetch connected emails")

st.header("Get Scheduled Email Jobs")
get_jobs_user_id = st.text_input("User ID", key="get_jobs_user_id")
if st.button("Get Email Jobs"):
    response = requests.get(f"{BASE_URL}/get_email_jobs", params={"user_id": get_jobs_user_id})
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("Failed to fetch email jobs")


st.header("Upload PPT and CSV Files")

user_id = st.text_input("User ID",key="user_id_upload")
csv_file = st.file_uploader("Upload CSV", type="csv")
pptx_file = st.file_uploader("Upload PPTX", type="pptx")
if st.button("Upload"):
    if user_id and csv_file and pptx_file:
        files = {
            'csv_file': csv_file,
            'pptx_file': pptx_file
        }
        response = requests.post(f"{BASE_URL}/upload_ppt_csv?user_id={user_id}", files=files)
        result = response.json()
        st.write(result)
        if result["status"] == "true":
            st.success(f"Document uploaded successfully! Download PPT Link: {result['ppt_link']}")
            st.write(f"Available Fields: {result['available_fields']}")
        else:
            st.error(result["message"])
    else:
        st.error("Please provide all required inputs.")

st.header("Process Data")
user_id = st.text_input("User ID",key="process_user_id")
doc_id = st.text_input("Document ID",key="process_doc_id")
openai_api_key = st.text_input("OpenAI API Key",key="openai_key")
gpt_model = st.text_input("GPT Model",key="model")
topic = st.text_input("Topic")
prompt_template = st.text_area("Prompt Template (Optional)")
if st.button("Process Data"):
    if user_id and doc_id and openai_api_key and gpt_model and topic:
        response = requests.post(
            f"{BASE_URL}/process_data?user_id={user_id}&doc_id={doc_id}&openai_api_key={openai_api_key}&gpt_model={gpt_model}&topic={topic}&prompt_template={prompt_template}",
        )
        result = response.json()
        st.write(result["status"])
        if result["status"] == "true":
            st.success(f"Processing completed successfully!")
            st.write(f"Download PPT Link: {result['download_ppt_link']}")
            st.write(f"Download CSV Link: {result['download_csv_link']}")
        else:
            st.error(result["message"])
    else:
        st.error("Please provide all required inputs.")

st.header("Get Existing Document")
user_id = st.text_input("User ID", key="user_id")
if st.button("Get documents"):
    if user_id:
        response = requests.get(f"{BASE_URL}/get_document", params={'user_id': user_id})
        result = response.json()
        st.write(result)
    else:
        st.error("Please provide User ID.")
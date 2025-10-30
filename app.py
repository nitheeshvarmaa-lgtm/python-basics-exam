import streamlit as st
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.title("Python Basics Exam Generator 🐍")
st.write("Upload a JSON file with your 50 questions to auto-create a Google Form exam.")

uploaded_file = st.file_uploader("Upload your python_basics_50_mcq.json", type="json")

if uploaded_file:
    data = json.load(uploaded_file)
    st.success(f"Loaded {len(data['questions'])} questions.")
    
    if st.button("Generate Google Form"):
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/forms.body"]
        )
        service = build("forms", "v1", credentials=creds)
        form = service.forms().create(body={
            "info": {
                "title": data["title"],
                "documentTitle": "Python Basics Exam",
                "description": data["description"]
            }
        }).execute()

        for q in data["questions"]:
            body = {
                "requests": [{
                    "createItem": {
                        "item": {
                            "title": q["question"],
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "choiceQuestion": {
                                        "type": "RADIO",
                                        "options": [{"value": o} for o in q["options"]],
                                        "shuffle": True
                                    }
                                }
                            }
                        },
                        "location": {"index": 0}
                    }
                }]
            }
            service.forms().batchUpdate(formId=form["formId"], body=body).execute()

        st.success("✅ Google Form created successfully!")
        st.markdown(f"[Open your Form here]({form['responderUri']})")

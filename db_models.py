import pymongo
from datetime import datetime
from pydantic import BaseModel, EmailStr
from builtins import str
import pytz
from datetime import timezone
from constants import MONGODB_URL

client = pymongo.MongoClient(MONGODB_URL)

db = client["marketing"]

users_collection = db["users"]
login_session_collection = db["login_sessions"]
email_scheduler_db = client["email_scheduler_db"]
users_collection_email_scheduler = email_scheduler_db["users_email_schedule"]
jobs_collection_email_schedule = email_scheduler_db["jobs"]


class LoginSession:
    def __init__(
        self, created_at=datetime.now(), status=1, email_id=None, user_id=None
    ):
        self.user_id = user_id
        self.created_at = created_at
        self.status = status
        self.email_id = email_id


class SignupOTP:
    def __init__(self) -> None:
        self.otp_data_col = db["otp_data"]

    def insert_otp_data(self, email_id, otp):
        otp_data = self.otp_data_col.find_one({"user_id": email_id})
        if otp_data is None:
            self.otp_data_col.insert_one(
                {"user_id": email_id, email_id: otp, "timestamp": datetime.now()}
            )
            return "Successful updated"
        return

    def update_otp_data(self, email_id, otp):
        otp_data = self.otp_data_col.find_one({"user_id": email_id})
        if otp_data is not None:
            self.delete_otp_data(email_id)
            self.otp_data_col.insert_one(
                {"user_id": email_id, email_id: otp, "timestamp": datetime.now()}
            )
            return "Successfully updated"
        return

    def get_otp_data(self, email_id):
        otp_data = self.otp_data_col.find_one({"user_id": email_id})
        return otp_data[email_id], otp_data["timestamp"]

    def is_in_otp_data(self, email_id):
        try:
            otp_data = self.otp_data_col.find_one({"user_id": email_id})
            if email_id in otp_data:
                return True
            return False
        except Exception:
            return False

    def delete_otp_data(self, email_id):
        otp_data = self.otp_data_col.find_one({"user_id": email_id})
        if email_id in otp_data:
            self.otp_data_col.delete_one({"user_id": email_id})
            return "OTP deleted successful"
        return "Something went wrong while deleting otp"

    def updatepwd_insert_otp_data(self, email_id, otp):
        otp_data = self.update_password_otp.find_one({"_id": email_id})
        if otp_data is None:
            self.update_password_otp.insert_one({"_id": email_id, email_id: otp})
            return "Successful updated"
        return

    def updatepwd_update_otp_data(self, email_id, otp):
        otp_data = self.otp_data_col.find_one({"user_id": email_id})
        if otp_data is not None:
            self.delete_otp_data(email_id)
            self.otp_data_col.insert_one({"user_id": email_id, email_id: otp})
            return "Successfully updated"
        return

    def updatepwd_otp_data(self, email_id, otp):
        otp_data = self.update_password_otp.find_one({"_id": email_id})
        if otp_data is not None:
            self.delete_otp_data(email_id)
            self.update_password_otp.insert_one({"_id": email_id, email_id: otp})
            return "Successfully updated"
        return

    def updatepwd_get_otp_data(self, email_id):
        otp_data = self.update_password_otp.find_one({"_id": email_id})
        return otp_data[email_id]

    def updatepwd_is_in_otp_data(self, email_id):
        try:
            otp_data = self.update_password_otp.find_one({"_id": email_id})
            if email_id in otp_data:
                return True
            return False
        except Exception:
            return False

    def updatepwd_delete_otp_data(self, email_id):
        otp_data = self.update_password_otp.find_one({"_id": email_id})
        if email_id in otp_data:
            self.update_password_otp.delete_one({"_id": email_id})
            return "OTP deleted successful"
        return "Something went wrong while deleting otp"


class UserDataManage:
    def __init__(self) -> None:
        self.global_metadata_col = db["user_documents"]

    def is_user_id_in_global_metadata(self, user_id):
        try:
            if (
                self.global_metadata_col.find_one({"user_id": user_id})["user_id"]
                == user_id
            ):
                return True
            else:
                return False
        except Exception:
            return False

    def insert_session_id(self, user_id):
        self.global_metadata_col.insert_one({"user_id": user_id, user_id: {}})
        return "success"

    def insert_documents(
        self,
        user_id,
        document_id,
        prompt_template,
        topics,
        template_name,
        df_name,
        ppt_link,
        dataframe,
        dataframe_fields,
    ):
        indian_timezone = pytz.timezone("Asia/Kolkata")
        utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
        indian_now = utc_now.astimezone(indian_timezone)
        formatted_time = indian_now.strftime("%d %b %Y at %I:%M %p")
        filter_query = {"user_id": user_id}
        update_query = {
            "$set": {
                f"{user_id}.{document_id}": {
                    "prompt_template": prompt_template,
                    "topics": topics,
                    "template_name": template_name,
                    "df_name": df_name,
                    "ppt_link": ppt_link,
                    "created_at": formatted_time,
                    "dataframe": dataframe,
                    "dataframe_fields": dataframe_fields,
                    "download_ppt_link": None,
                    "download_csv_link": None,
                }
            }
        }
        self.global_metadata_col.update_one(filter_query, update_query, upsert=True)
        return formatted_time

    def get_document(self, user_id, doc_id):
        document = self.global_metadata_col.find_one({"user_id": user_id})
        if document:
            return document[user_id][doc_id]
        return None

    def get_all_document(self, user_id):
        projection = {f"{user_id}": 1, "_id": 0}
        documents = self.global_metadata_col.find_one(
            {"user_id": user_id}, projection=projection
        )
        if documents:
            return documents
        return None

    def update_document_collection(
        self,
        user_id,
        document_id,
        prompt_template=None,
        topics=None,
        download_ppt=None,
        download_csv_link=None,
    ):
        filter_query = {f"{user_id}.{document_id}": {"$exists": True}}
        update_query = {"$set": {}}
        if prompt_template is not None:
            update_query["$set"][
                f"{user_id}.{document_id}.prompt_template"
            ] = prompt_template
        if topics is not None:
            update_query["$set"][f"{user_id}.{document_id}.topics"] = topics
        if download_ppt is not None:
            update_query["$set"][
                f"{user_id}.{document_id}.download_ppt_link"
            ] = download_ppt
        if download_csv_link is not None:
            update_query["$set"][
                f"{user_id}.{document_id}.download_csv_link"
            ] = download_csv_link
        if update_query["$set"]:
            self.global_metadata_col.update_one(filter_query, update_query)


class User:
    def __init__(
        self, first_name, last_name, email_id, password, salted_pwd, user_id="null"
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email_id = email_id
        self.password = password
        self.salted_pwd = salted_pwd
        self.last_login_time = datetime.now()
        self.user_id = user_id


class EmailRequest(BaseModel):
    sender_email: EmailStr
    receiver_email: EmailStr
    subject: str
    body: str
    send_at: datetime


class ConnectSenderRequest(BaseModel):
    user_id: str
    sender_email: EmailStr
    password: str

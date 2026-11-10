from pydantic import BaseModel

class Report_Schema(BaseModel):

    reported_user_email: str
    report_description: str
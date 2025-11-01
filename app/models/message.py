from pydantic import BaseModel, Field

class Message(BaseModel):
    sender: str = Field(default="", description="Who sent the email")
    date: str = Field(default="", description="The date the email was sent")
    subject: str = Field(default="", description="The subject of the email")
    text: str = Field(default="", description="The conctent of the email")

    def __repr__(self):
        return f"From: {self.sender} | Date: {self.date} | Subject: {self.subject} | Text: {self.text}"

    def get_sender(self):
        return self.sender
    
    def get_date(self):
        return self.date
    
    def get_subject(self):
        return self.subject
    
    def get_text(self):
        return self.text
    
    def set_sender(self, sender):
        self.sender = sender

    def set_date(self, date):
        self.date = date
    
    def set_subject(self, subject):
        self.subject = subject
    
    def set_text(self, text):
        self.text = text
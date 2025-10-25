class Message:
    def __init__(self):
        self.sender = ""
        self.date = ""
        self.subject = ""
        self.text = ""
    
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
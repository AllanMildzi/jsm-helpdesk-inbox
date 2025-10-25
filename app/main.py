import uvicorn
from fastapi import FastAPI

from imap_client import EmailListener
from core import Config

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI server running with IMAP listener"}

@app.on_event("startup")
def startup_event():
    print("Starting IMAP email listener...")
    print("Running in:", Config.ENV)
    print("Debug mode:", Config.DEBUG)

    listener = EmailListener(Config.HOST, Config.USERNAME, Config.APP_PASSWORD)
    listener.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
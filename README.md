# JSM Helpdesk Inbox

This project is a tool for help desk. It helps people work less.

Here is what it does essentially:
- **Checks Email**: It looks at Gmail all the time to see new messages.
- **Understands**: It reads the email to know what the problem is.
- **Makes Ticket**: It connects to Jira Service Management. It puts the problem there automatically.
- **Answers**: It sends email back to user to say "We received your problem".

It is written in Python. It uses AI to be smart and understand the text in the emails.

## How to Install (Setup)

This project needs Python and some secret keys.

#### 1. Secret Keys (Environment Variables)

You must make a file named `.env` in the main folder of this project. In this file, you write your secret keys.
Here are the keys you need:

*   `SERVER_HOST` (e.g., `127.0.0.1`)
*   `SERVER_PORT` (e.g., `8000`)
*   `IMAP_HOST` (e.g., `imap.gmail.com`)
*   `USERNAME` (your Gmail email address)
*   `APP_PASSWORD` (your Gmail App Password)
*   `GEMINI_API_KEY` (your Google Gemini API Key)
*   `JIRA_API_KEY` (your Jira API Token)
*   `JIRA_USERNAME` (your Jira email address)
*   `JIRA_DOMAIN` (your Jira Cloud domain)
*   `SERVICE_DESK_ID` (the ID number of your Service Desk)
*   `SERVICE_DESK_BASE_URL` (the base URL for your Jira Service Desk API)

Example `.env` file:
```
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
IMAP_HOST=imap.gmail.com
USERNAME=your-email@gmail.com
APP_PASSWORD=your-gmail-app-password
GEMINI_API_KEY=your-gemini-api-key
JIRA_API_KEY=your-jira-api-token
JIRA_USERNAME=your-jira-email@example.com
JIRA_DOMAIN=your-company.atlassian.net
SERVICE_DESK_ID=1
SERVICE_DESK_BASE_URL=https://your-company.atlassian.net/rest/servicedeskapi
```
*Remember to get an App Password for Gmail if you use 2-Factor Authentication.*
*And for Jira, make sure to create an API token.*

#### 2. Run with Docker Compose (Easy Way)

If you have Docker, this is fast:

1.  Make sure your `.env` file is ready.
2.  Open terminal in main folder.
3.  Run command: `docker-compose up --build`
4.  It will start the program for you.
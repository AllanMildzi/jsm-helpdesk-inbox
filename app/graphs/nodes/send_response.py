from langgraph.runtime import Runtime

from graphs.state import OverallState
from graphs.context import ContextSchema
from gmail import Gmail

def send_response(state: OverallState, runtime: Runtime[ContextSchema]) -> OverallState:
    input_email = state.email
    output = state.request_output

    message_content = f"""Hello,
    Your issue about {output.summary} has been created in Jira (Key {output.issueKey})
    You can find it here : {output.link}"""

    Gmail.send_message(service=runtime.context.gmail_service,
                       sender=input_email["To"],
                       recipient=input_email["From"],
                       subject=f"Follow up of you request: {input_email["Subject"]}",
                       content=message_content)

    return state
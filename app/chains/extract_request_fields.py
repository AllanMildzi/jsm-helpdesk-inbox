import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from core import Config
from chains.prompts import SYSTEM_PROMPTS

def extract_request_fields(email, fields):
    os.environ["GOOGLE_API_KEY"] = Config.GEMINI_API_KEY
    
    system_template = SYSTEM_PROMPTS.get("Determine request fields")

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{email}")]
    )

    prompt = prompt_template.invoke({"request_fields": fields, "email": email})
    
    request_fields_model = init_chat_model("gemini-2.5-flash-lite", model_provider="google_genai")
    response = request_fields_model.invoke(prompt)

    return response.content
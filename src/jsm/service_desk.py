import requests
import json
import base64

from core import Config
from models import RequestBody, RequestField, RequestType
from utils import get_logger

logger = get_logger(__name__)

class ServiceDesk:
    REST_CLIENT = None
    REQUEST_TYPES_LIST = None
    
    @classmethod
    def build_rest_client(cls):
        auth = f"{Config.JIRA_USERNAME}:{Config.JIRA_API_KEY}"
        return base64.b64encode(auth.encode()).decode()

    @classmethod
    def get_requests(cls):
        url = f"{Config.SERVICE_DESK_BASE_URL}/request"

        headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + cls.REST_CLIENT
        }

        response = requests.request(
            "GET",
            url,
            headers=headers
        )

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Failed to decode JSON response")

        if response.status_code != 200:
            raise RuntimeError(f"Error code {response.status_code}: {data.get('message', data)}")
        
        return data
    
    @classmethod
    def create_request(cls, request_body: RequestBody):
        url = f"{Config.SERVICE_DESK_BASE_URL}/request"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Basic " + cls.REST_CLIENT
        }

        payload = request_body.model_dump_json()

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers
        )

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Failed to decode JSON response")

        if response.status_code != 201:
            raise RuntimeError(f"Error code {response.status_code}: {data.get('message', data)}")

        return data
    
    @classmethod
    def get_request_types(cls):
        url = f"{Config.SERVICE_DESK_BASE_URL}/servicedesk/{Config.SERVICE_DESK_ID}/requesttype"

        headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + cls.REST_CLIENT
        }

        response = requests.request(
            "GET",
            url,
            headers=headers
        )

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Failed to decode JSON response")

        if response.status_code != 200:
            raise RuntimeError(f"Error code {response.status_code}: {data.get('message', data)}")

        values = data.get("values", [])
        
        return [
            RequestType.model_validate(val) 
            for val in values if "id" in val and "name" in val
        ]
    
    @classmethod
    def get_request_fields_names(cls, request_type_id):
        url = f"{Config.SERVICE_DESK_BASE_URL}/servicedesk/{Config.SERVICE_DESK_ID}/requesttype/{request_type_id}/field"

        headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + cls.REST_CLIENT
        }

        response = requests.request(
            "GET",
            url,
            headers=headers
        )

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Failed to decode JSON response")

        if response.status_code != 200:
            raise RuntimeError(f"Error code {response.status_code}: {data.get('message', data)}")

        request_type_fields = data.get("requestTypeFields", [])
        
        return [
            RequestField.model_validate(field) 
            for field in request_type_fields if "fieldId" in field and "name" in field and "validValues" in field
        ]

if ServiceDesk.REST_CLIENT is None:
    ServiceDesk.REST_CLIENT = ServiceDesk.build_rest_client()

if ServiceDesk.REQUEST_TYPES_LIST is None:
    ServiceDesk.REQUEST_TYPES_LIST = ServiceDesk.get_request_types()
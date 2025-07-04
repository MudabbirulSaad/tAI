# !gcloud auth application-default login - run this to add vertex credentials to your env
import litellm, os
from litellm import completion 
from pydantic import BaseModel 
from dotenv import load_dotenv
load_dotenv()



messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ]

litellm.enable_json_schema_validation = True
litellm.set_verbose = True # see the raw request made by litellm

class CalendarEvent(BaseModel):
  name: str
  date: str
  participants: list[str]

resp = completion(
    # model="openrouter/qwen/qwen3-32b-04-28:free",
    # model="gemini/gemini-2.0-flash",
    # model="openrouter/openai/gpt-4o-mini",
    messages=messages,
    response_format=CalendarEvent,
    api_key=os.getenv("GEMINI_API_KEY"),
)

# print("Received={}".format(resp))
print(type(resp))
print(resp.model_dump()['choices'][0]['message']['content'])
# print(resp.name)
# print(resp.date)
# print(resp.participants)
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import uuid7
from dotenv import load_dotenv
load_dotenv()
import os
api_key=os.getenv("GOOGLE_API_KEY")
model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

store={}

def get_session(session_id:str):
    if session_id not in store:
        store[session_id]=ChatMessageHistory()
    return store[session_id]

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","you are a helpful assistant"),
        MessagesPlaceholder(variable_name="history"),
        ("human","{input}")
    ]
)
chain=prompt  | model
with_msg=RunnableWithMessageHistory(
    chain,
    get_session,
    input_messages_key="input",
    history_messages_key="history"
)

id=uuid7()
while True:
    print("-"*50)
    user=input("enter : ")
    if user in["exit","quit"]:
        print("byee")
        break
    response : AIMessage=with_msg.invoke(
        {"input":user},
        config={"configurable":{"session_id":id}}
    )
    print(f"response: {response.content}")

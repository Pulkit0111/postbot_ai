import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_key = os.getenv("TAVILY_API_KEY")

if not tavily_key:
    raise EnvironmentError("Missing TAVILY_API_KEY in environment variables.")

tavily_client = TavilyClient(api_key=tavily_key)

def search_topic(topic):
    try:
        response = tavily_client.search(query=topic, max_results=20)
        content = "\n\n".join([item["content"] for item in response["results"]])
        return content
    except Exception as e:
        print(f"Error from Tavily: {e}")
        return ""

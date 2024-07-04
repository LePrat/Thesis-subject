import google.generativeai as genai
from os import environ

AI_MODEL = "gemini-1.5-flash"


def finder(content):
    google_api_key = environ.get("GOOGLE_API_KEY")
    print(f"API: {google_api_key}")
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(AI_MODEL)

    prompt = f"""
    You are a helpful assistant that can find information about the details of the fellowship that I am about to show you. 
    You need to find where the fellowship is located and from where the fellow must come from. You can only answer with this format:
    Location: location
    Nationality: nationality
    Don't put any other information in the answer. If you are not sure about the answer, write unknown for that field.
    If the answer is worldwide, write worldwide for the location.
    Here is the information about the fellowship:
    {content}
    """

    response = model.generate_content(prompt)
    return response.text


def run_finder_for_fund(fund):
    return finder(fund.eligibility_text)

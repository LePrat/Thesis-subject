import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

AI_MODEL = "gemini-1.5-flash"


def finder(content):
    genai.configure()
    model = genai.GenerativeModel(AI_MODEL)

    prompt = f"""
    You are a helpful assistant that can find information about the details of the fellowship that I am about to show you. 
    You need to find where the fellow needs to go and from where the fellow must come from or live in the last years. You can only answer with this format:
    location;nationality
    where the location is where the fellow needs to go (the country only) and the nationality is from where the fellow must come from or live in the last years.
    Don't put any other information in the answer. If you are not sure about the answer, write unknown for that field.
    If the answer is anywhere in the world, write worldwide for the location.
    Here is the information about the fellowship:
    {content}
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0)
        )
    except ResourceExhausted as e:
        return e
    return response.text


def run_finder_for_fund(fund):
    return finder(fund.eligibility_text)

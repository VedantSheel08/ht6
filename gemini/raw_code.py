import google.generativeai as genai
from dotenv import load_dotenv
import os

# Set up the Gemini model
load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv("GEMINI_API_KEY")  # Gemini API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def national_animal(country: str) -> str:
    """Returns the national animal of a given country."""
    prompt = (
        f"What is the national animal of {country}? "
        "Answer with only the animal’s common English name."
    )
    res = model.generate_content(prompt)
    return res.text.strip()

if __name__ == "__main__":
    # Simple test example
    country = input("Enter a country: ")
    print("National Animal:", national_animal(country))

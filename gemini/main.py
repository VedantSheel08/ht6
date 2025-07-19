from mcp.server.fastmcp import FastMCP
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Set up the Gemini model
API_KEY = os.getenv("GEMINI_API_KEY")  # Gemini API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up the MCP server
mcp = FastMCP("Gemini MCP Server")

@mcp.tool()
def national_animal(country: str) -> str:
    """Returns the national animal of a given country."""
    prompt = (
        f"What is the national animal of {country}? "
        "Answer with only the animal’s common English name."
    )
    res = model.generate_content(prompt)
    return res.text.strip()

if __name__ == "__main__":
    mcp.run(transport="stdio")  # You can change to 'http' or other supported transports


"""from mcp.server.fastmcp import FastMCP
import google.generativeai as genai

# set up the Gemini model
API_KEY = os.getenv("GEMINI_API_KEY")  # the Gemini API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# set up the server
mcp = FastMCP("Gemini MCP Server")

@mcp.tool()
def national_animal(country: str) -> str:
    prompt = (
        f"What is the national animal of {country}? "
        "Answer with only the animal’s common English name."
    )
    res = model.generate_content(prompt)
    return res.text.strip()


if __name__ == "__main__":
    mcp.run(transport="stdio")
"""
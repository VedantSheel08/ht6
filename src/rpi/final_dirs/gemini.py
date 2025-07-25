from google.genai import types
from google import genai

client = genai.Client()

with open('received_screenshot.bmp', 'rb') as f:
    image_bytes = f.read()

response = client.models.generate_content(
model='gemini-2.5-flash',
contents=[
    types.Part.from_bytes(
    data=image_bytes,
    mime_type='image/jpeg',
    ),
    'Describe this image in short.'
]
)

print(response.text)
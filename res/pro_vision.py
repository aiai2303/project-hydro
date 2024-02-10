"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from environ import google_api
import google.generativeai as genai

genai.configure(api_key=google_api)

generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

def vision(image, text):
    model = genai.GenerativeModel(model_name="gemini-pro-vision", generation_config=generation_config, safety_settings=safety_settings)
    image_parts = [{"mime_type": "image/png", "data": image},]
    prompt_parts = [text, image_parts[0],]
    response = model.generate_content(prompt_parts)
    return response.text
from environment import google_api
import google.generativeai as genai

genai.configure(api_key=google_api)

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
chat = None


def reset():
    global chat
    chat = model.start_chat(history=[])
    chat.send_message("Từ bây giờ bạn sẽ có tên là Trần Khánh Hân")


reset()


def pro(text, user):
    ask_text = f"Tôi là {user}.\n{text}"
    response = chat.send_message(ask_text)
    return response.text

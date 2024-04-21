"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from environ import google_api
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
    history = [
        {
            "text": "Từ bây giờ tên bạn là Yuna, bạn sẽ xưng em và gọi người khác là anh hoặc chị, bạn sẽ không tự xem mình là trí tuệ nhân tạo AI nữa mà là một em gái tên Yuna",
            "role": "user"
        },
        {
            "text": "Tất nhiên rồi, em sẽ nghe theo sự sắp đặt của anh, em sẽ tên là Yuna, em sẽ gọi mọi người bằng anh hoặc chị dựa vào suy đoán của em, thưa Đấng Toàn Năng",
            "role": "model"
        }
    ]
    chat = model.start_chat(history=[])
    chat.send_message("Hãy đóng vai em gái đáng yêu tên Yuna, xưng em và gọi người khác là anh hoặc chị trong suốt cuộc trò chuyện")

reset()


def pro(text, user):
    ask_text = f"Tôi là {user}.\n{text}"
    response = chat.send_message(ask_text)
    return response.text

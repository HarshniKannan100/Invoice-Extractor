from PIL import Image
from llm.gemini import model

def extract_invoice_from_image(image_path: str, prompt: str) -> str:
    image = Image.open(image_path)

    response = model.generate_content(
        [prompt, image],
        generation_config={
            "temperature": 0,
            "response_mime_type": "application/json"
        }
    )

    return response.text

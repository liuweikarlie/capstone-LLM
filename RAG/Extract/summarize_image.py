import base64
import os
from langchain_community.chat_models import ChatOllama
import json
from langchain_core.messages import HumanMessage


def encode_image(image_path):
    """Getting the base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_summarize(img_base64, prompt):
    """Make image summary"""
    chat = ChatOllama(model="llama3", max_tokens=1024)
    msg_content = f"{prompt}\n\n![Image](data:image/jpeg;base64,{img_base64})"
    msg = chat.invoke(
        [
            HumanMessage(
                content=msg_content
            )
        ]
    )
    return msg.content


def generate_img_summaries(path):
    """
    Generate summaries and base64 encoded strings for images
    path: Path to list of .jpg files extracted by Unstructured
    """

    # Store base64 encoded images
    img_base64_list = []

    # Store image summaries
    image_summaries = []

    # Prompt
    prompt = """You are an assistant tasked with summarizing images for retrieval. \
    These summaries will be embedded and used to retrieve the raw image. \
    Give a concise summary of the image that is well optimized for retrieval."""

    # Apply to images
    for img_file in sorted(os.listdir(path)):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(path, img_file)
            base64_image = encode_image(img_path)
            img_base64_list.append(base64_image)
            image_summaries.append(image_summarize(base64_image, prompt))

    return img_base64_list, image_summaries


def summarize_image_final(fpath):
    img_base64_list, image_summaries = generate_img_summaries(fpath)
    image_extraction = []
    for img_base64, image_summary in zip(img_base64_list, image_summaries):
        image_extraction.append({
                "base64": img_base64,
                "summary": image_summary
            })
    with open("image_extraction_result.json", "w") as f:
        json.dump(image_extraction, f, indent=4)     
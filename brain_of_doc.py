# step 1: setup GROQ API KEY
import os
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

# step 2: convert image to required format
import base64
# Add this function to your existing brain_of_doc.py file

import base64

def encode_image(image_path):
    """
    Encode an image file to base64 string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_image_with_query(query, encoded_image, model="llama-3.2-90b-vision-preview"):
    """
    Analyze an image with a text query using Groq API
    """
    import os
    from groq import Groq
    
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=GROQ_API_KEY)
    
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )
    
    return chat_completion.choices[0].message.content
'''image_path="acne.jpg"
image_file=open(image_path,"rb")#rb read binary format
encoded_image=base64.b64encode(image_file.read()).decode("utf-8")


# step 3: setup Multimodel LLM
from groq import Groq
client =Groq(api_key=GROQ_API_KEY)
query="is there something wrong with my face"
model="llama-3.2-90b-vision-preview"
messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
chat_completion=client.chat.completions.create(messages=messages,model=model)
print(chat_completion.choices[0].message.content)'''
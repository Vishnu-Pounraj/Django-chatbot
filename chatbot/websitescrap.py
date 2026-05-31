import requests
from bs4 import BeautifulSoup
import ollama


def get_website_text(url):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)



def chat_bot(context, question):
    prompt = f"""
Answer ONLY using website content.

Website:
{context[:8000]}

Question:
{question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
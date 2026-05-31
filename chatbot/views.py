from django.shortcuts import render , redirect
from .models import Document, ChatQuery
from .rag import create_vectorstore, ask_question
from django.contrib import messages
from .websitescrap import get_website_text, chat_bot




def userlogin(request):
    return render(request,'login.html')

# something new to watch

VECTOR_DB = {}

def home(request):
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        doc = Document.objects.create(file=file)
        file_path = doc.file.path

        vectorstore = create_vectorstore(file_path)

        VECTOR_DB[doc.id] = vectorstore
        request.session['doc_id'] = doc.id

        messages.success(request, "Uploaded & processed!")
        print("uploaded")
        return redirect('chat')

    return render(request, "home.html")


def ask_bot(request):

    doc_id = request.session.get('doc_id')
    vectorstore = VECTOR_DB.get(doc_id)

    if not vectorstore:
        return render(request, "chatbot.html", {
            "error": "Document not processed"
        })

    chat_ids = request.session.get('chat_ids', [])

    if request.method == "POST":
        query = request.POST.get("question")

        if not query:
            answer = "Please enter a question."
        else:
            clean_query = query.strip().lower()

            if clean_query in ["hi", "hello", "hey"]:
                answer = "Hello! How can I help you?"
            else:
                print("Calling Ollama model...")
                answer = ask_question(vectorstore, query)

        chat = ChatQuery.objects.create(
            question=query,
            answer=answer
        )

        chat_ids.append(chat.id)
        request.session['chat_ids'] = chat_ids

    chats = ChatQuery.objects.filter(id__in=chat_ids).order_by('-id')

    return render(request, "chatbot.html", {
        "chats": chats
    })


# website scrap


website_cache = {}  # simple memory (no JS, no DB)

def ask_website(request):
    answer = None
    website_status = None

    if request.method == "POST":

        url = request.POST.get("url")
        question = request.POST.get("question")


        if url and not question:
            text = get_website_text(url)
            website_cache["data"] = text
            website_status = "Website loaded successfully"

        elif question:
            context = website_cache.get("data", "")
            answer = chat_bot(context, question)

    return render(request, "website.html", {
        "answer": answer,
        "status": website_status
    })
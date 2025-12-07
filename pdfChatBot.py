import os
from groq import Groq
from pypdf import PdfReader

# ========= 1. CONFIG =========

# 🔴 Put your working Groq API key here (the one you used before)
GROQ_API_KEY = "****"

client = Groq(api_key=GROQ_API_KEY)

# Groq model to use
GROQ_MODEL = "llama-3.3-70b-versatile"

# To avoid sending extremely huge text in one go
MAX_DOC_CHARS = 12000  # you can increase later if needed


# ========= 2. LOAD & EXTRACT TEXT FROM PDF =========

def extract_text_from_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns all text as a single string.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        reader = PdfReader(file_path)
    except Exception as e:
        raise RuntimeError(f"Error opening PDF: {e}")

    pages_text = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            print(f"[Warning] Could not read page {i}: {e}")
            text = ""
        pages_text.append(text)

    full_text = "\n\n".join(pages_text).strip()
    return full_text


# ========= 3. ASK GROQ ABOUT THE DOCUMENT =========

def ask_groq_about_document(doc_text: str, user_request: str) -> str:
    """
    Sends the document content + your question to the Groq model,
    and returns the model's answer.
    """

    # Limit the doc size so we don't overflow the model context
    truncated_doc = doc_text[:MAX_DOC_CHARS]

    system_message = (
        "You are an AI assistant that helps the user understand a document. "
        "You must answer based ONLY on the document text provided. "
        "If the document does not contain the answer, say you cannot find it "
        "in the document."
    )

    user_message = (
        "Here is the document content:\n\n"
        f"{truncated_doc}\n\n"
        "User request:\n"
        f"{user_request}\n\n"
        "Respond clearly, step by step if needed."
    )

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
        )
        answer = completion.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"[Groq API error: {e}]"


# ========= 4. MAIN FLOW: LOAD PDF, THEN CHAT =========

def main():
    if GROQ_API_KEY == "gsk_your_real_key_here":
        print("⚠ Please put your real Groq API key in GROQ_API_KEY first.")
        return

    print("=== PDF Chat Bot (Groq, no UI) ===")
    print("You will give me a PDF file, I'll read it, and then you can ask questions about it.\n")

    file_path = input("Enter the full path to your PDF file: ").strip().strip('"')

    if not file_path.lower().endswith(".pdf"):
        print("⚠ This script currently supports only .pdf files.")
        return

    print("\nLoading and reading the PDF, please wait...\n")

    try:
        doc_text = extract_text_from_pdf(file_path)
    except Exception as e:
        print("Error reading PDF:", e)
        return

    if not doc_text:
        print("⚠ No text found in this PDF (maybe it's scanned images).")
        return

    print(f"✅ Loaded document. Approx characters: {len(doc_text)}")
    if len(doc_text) > MAX_DOC_CHARS:
        print(f"ℹ Note: Document is long; only the first {MAX_DOC_CHARS} characters are sent to the model each time.\n")

    print("You can now ask questions about this document.")
    print("Examples:")
    print("  - Give me a summary of the document.")
    print("  - Explain section 2 in simple words.")
    print("  - What are the key points?")
    print("Type 'quit' to exit.\n")

    while True:
        user_request = input("You: ").strip()
        if user_request.lower() in {"quit", "exit"}:
            print("PDF Chat Bot: Goodbye! 👋")
            break

        if not user_request:
            continue

        print("PDF Chat Bot: Thinking...\n")

        answer = ask_groq_about_document(doc_text, user_request)

        print("PDF Chat Bot:", answer)
        print()


if __name__ == "__main__":
    main()

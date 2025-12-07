from groq import Groq

# 🔴 1) PUT YOUR REAL GROQ KEY HERE (starts with gsk_)
GROQ_API_KEY = "***"

client = Groq(api_key=GROQ_API_KEY)

def main():
    print("Groq Chat Bot: type 'quit' to exit.\n")

    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            print("Groq Chat Bot: Goodbye! 👋")
            break

        try:
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user},
                ],
                temperature=0.4,
            )
            answer = resp.choices[0].message.content.strip()
        except Exception as e:
            print("Groq Chat Bot ERROR:", e)
            continue

        print("\nGroq Chat Bot:", answer, "\n")

if __name__ == "__main__":
    main()

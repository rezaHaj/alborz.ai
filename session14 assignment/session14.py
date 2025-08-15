from openai import OpenAI

OPENAI_API_KEY = "aa-VIYcdCWFZTHh6GlKSVnyDRmOEjiJWfhDGb6HtCOSTEdQDGVP"
AVALAI_BASE_URL = "https://api.avalai.ir/v1"

client = OpenAI(api_key=OPENAI_API_KEY, base_url=AVALAI_BASE_URL)

tone = input("Enter the tone for the conversation (e.g., sarcastically, cheerfully, angrily): ")

if not tone.strip():
    print("Error: Tone cannot be empty. Exiting program.")
    exit()

prompts = [
    {"role": "system", "content": f"Respond {tone}!"}
]

EXIT_WORDS = {"quit", "exit", "stop"}

while True:
    user_message = input("\nEnter your message (or 'quit', 'exit', or 'stop' to end): ")
    
    if user_message.lower() in EXIT_WORDS:
        print("Ending conversation.")
        break
    
    if not user_message.strip():
        print("Error: Message cannot be empty.")
        continue

    prompts.append({"role": "user", "content": user_message})

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=prompts
        )


        response = completion.choices[0].message.content

        print(f"\nAI Response ({tone}): {response}")

        prompts.append({"role": "assistant", "content": response})

        print("\n--- Conversation History ---")
        for msg in prompts:
            print(f"{msg['role'].capitalize()}: {msg['content']}")

    except Exception as e:
        print(f"An error occurred: {e}")

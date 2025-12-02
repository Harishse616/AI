import tkinter as tk
from tkinter import scrolledtext
import ollama
import threading

client = ollama.Client()

# Function that calls Ollama
def ask_ollama(prompt, chat_window):
    chat_window.insert(tk.END, "\nAI: ")
    chat_window.see(tk.END)

    # Stream response
    for chunk in client.generate(model="llama2", prompt=prompt, stream=True):
        part = chunk.get("response", "")
        chat_window.insert(tk.END, part)
        chat_window.see(tk.END)

# Handle send button
def send_message():
    user_message = entry.get()
    if not user_message.strip():
        return

    chat_window.insert(tk.END, f"\nYou: {user_message}")
    chat_window.see(tk.END)
    entry.delete(0, tk.END)

    # Run the model in a separate thread so UI doesn't freeze
    threading.Thread(target=ask_ollama, args=(user_message, chat_window)).start()


# ---------------- GUI ------------------

root = tk.Tk()
root.title("Harish's personal AI")
root.geometry("500x600")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", 12))
chat_window.pack(padx=10, pady=10, fill="both", expand=True)

entry = tk.Entry(root, font=("Segoe UI", 14))
entry.pack(padx=10, pady=5, fill="x")

send_button = tk.Button(root, text="Send", font=("Segoe UI", 12), command=send_message)
send_button.pack(padx=10, pady=10)

root.mainloop()

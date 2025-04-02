import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu
from datetime import datetime
import pyttsx3
import threading
import json
import random

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(True, True)
        self.root.minsize(600, 400)
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Load responses from JSON
        self.load_responses()
        
        self.create_menu()
        self.create_widgets()
        self.is_speech_enabled = True

    def load_responses(self):
        self.responses = {
            "hello": ["Hello there! How can I help you today?", "Hi! How are you doing?", "Hey! Nice to see you!"],
            "hi": ["Hi! Nice to meet you!", "Hello! How can I assist you?", "Hey there! What's up?"],
            "hey": ["Hey! What's on your mind?", "Hello! How can I help?", "Hi there! What can I do for you?"],
            "how are you": ["I'm doing great, thanks for asking! How about you?", "I'm excellent! How are you today?"],
            "weather": ["I don't have live weather info, but I hope it's sunny where you are!", "Sorry, I can't check the weather right now."],
            "bye": ["Goodbye! Have a great day!", "See you later! Take care!", "Bye! Come back soon!"],
            "goodbye": ["Take care! Come back soon!", "Goodbye! Have a wonderful time!", "See you next time!"],
            "name": ["I'm AI Assistant, your friendly virtual helper!", "You can call me AI Assistant!"],
            "help": ["I can help you with various topics. Try asking about:\n- My name\n- How I'm doing\n- The time\n- Tell a joke"],
            "joke": ["Why don't programmers like nature? It has too many bugs!", 
                    "What do you call a bear with no teeth? A gummy bear!",
                    "Why did the scarecrow win an award? He was outstanding in his field!"],
            "time": [f"The current time is {datetime.now().strftime('%H:%M')}"],
            "thanks": ["You're welcome! Need anything else?", "Glad I could help!", "Anytime!"],
            "thank you": ["You're welcome! Need anything else?", "Happy to help!", "My pleasure!"]
        }

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Chat", command=self.save_chat)
        file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Options Menu
        options_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_checkbutton(label="Text-to-Speech", 
                                   command=self.toggle_speech,
                                   variable=tk.BooleanVar(value=True))

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(
            main_frame,
            state="disabled",
            wrap=tk.WORD,
            font=("Helvetica", 12),
            bg="#ECF0F1",
            fg="#2C3E50",
            width=50,
            height=20
        )
        self.chat_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(main_frame, bg="#2C3E50")
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # User input field
        self.user_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bg="#ECF0F1",
            fg="#2C3E50",
            width=40
        )
        self.user_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.user_entry.bind("<Return>", self.send_message)

        # Buttons frame
        button_frame = tk.Frame(input_frame, bg="#2C3E50")
        button_frame.pack(side=tk.RIGHT)

        # Send button
        send_button = tk.Button(
            button_frame,
            text="Send",
            font=("Helvetica", 12, "bold"),
            command=self.send_message,
            bg="#3498DB",
            fg="white",
            activebackground="#2980B9"
        )
        send_button.pack(side=tk.LEFT, padx=5)

        # Welcome message
        self.root.after(100, lambda: self.update_chat("Assistant", "Hello! How can I assist you today?"))

    def get_bot_response(self, user_input):
        user_input = user_input.lower().strip()
        
        for key in self.responses:
            if key in user_input:
                return random.choice(self.responses[key])
        
        return "I'm not sure I understand. Could you please rephrase that?"

    def speak(self, text):
        if self.is_speech_enabled:
            threading.Thread(target=self.engine.say, args=(text,), daemon=True).start()
            threading.Thread(target=self.engine.runAndWait, daemon=True).start()

    def send_message(self, event=None):
        user_message = self.user_entry.get().strip()
        if user_message:
            self.update_chat("You", user_message)
            response = self.get_bot_response(user_message)
            self.update_chat("Assistant", response)
            self.speak(response)
            self.user_entry.delete(0, tk.END)

    def update_chat(self, sender, message):
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_area.config(state="normal")
        
        # Format message with different colors for sender and message
        if sender == "You":
            sender_color = "#3498DB"
        else:
            sender_color = "#27AE60"
            
        self.chat_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_area.insert(tk.END, f"{sender}: ", "sender")
        self.chat_area.insert(tk.END, f"{message}\n", "message")
        
        self.chat_area.tag_config("timestamp", foreground="#7F8C8D")
        self.chat_area.tag_config("sender", foreground=sender_color, font=("Helvetica", 12, "bold"))
        self.chat_area.tag_config("message", foreground="#2C3E50")
        
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

    def clear_chat(self):
        self.chat_area.config(state="normal")
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state="disabled")
        self.update_chat("Assistant", "Chat history cleared. How can I help you?")

    def save_chat(self):
        try:
            with open("chat_history.txt", "w", encoding="utf-8") as f:
                f.write(self.chat_area.get(1.0, tk.END))
            messagebox.showinfo("Success", "Chat history saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save chat history: {str(e)}")

    def toggle_speech(self):
        self.is_speech_enabled = not self.is_speech_enabled

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
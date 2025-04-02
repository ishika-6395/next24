import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import lyricsgenius
import os
import json
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from fpdf import FPDF
import webbrowser
from PIL import Image, ImageTk

class LyricsExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Multilingual Lyrics Extractor")
        self.root.geometry("800x600")
        
        # Load settings and favorites
        self.load_settings()
        self.load_favorites()
        
        # Language options
        self.languages = {
            'English': 'en',
            'Hindi': 'hi',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Chinese': 'zh-cn'
        }
        
        # Theme colors
        self.themes = {
            'light': {
                'bg': "#f0f0f0",
                'fg': "#333333",
                'button': "#4CAF50",
                'button_hover': "#45a049",
                'text_bg': "white"
            },
            'dark': {
                'bg': "#2c2c2c",
                'fg': "#ffffff",
                'button': "#5c6bc0",
                'button_hover': "#3f51b5",
                'text_bg': "#363636"
            }
        }
        
        # Initialize theme
        self.current_theme = self.settings.get('theme', 'light')
        self.apply_theme()
                # Initialize Genius API
        load_dotenv()  # Add this line to ensure .env is loaded
        token = os.getenv('GENIUS_ACCESS_TOKEN')
        if not token:
            print("Debug: Current working directory:", os.getcwd())
            print("Debug: Looking for .env file in:", os.path.abspath('.'))
            messagebox.showerror("Error", "Genius API token not found. Please check your .env file.")
            root.destroy()
            return   
        self.genius = lyricsgenius.Genius(token)
        self.create_widgets()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 11))
        style.configure('TButton', font=('Helvetica', 11, 'bold'))
        style.configure('TLabelframe', background="#f0f0f0")
        style.configure('TLabelframe.Label', font=('Helvetica', 12, 'bold'))
        style.configure('TCombobox', font=('Helvetica', 11))
    
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Top Frame
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill="x", pady=5)
        
        # Theme toggle button
        theme_btn = tk.Button(
            top_frame,
            text="🌓 Toggle Theme",
            command=self.toggle_theme,
            bg=self.themes[self.current_theme]['button'],
            fg="white",
            font=('Helvetica', 10),
            cursor="hand2"
        )
        theme_btn.pack(side="right", padx=5)
        
        # Title Label
        title_label = tk.Label(
            main_container,
            text="Multilingual Lyrics Finder",
            font=('Helvetica', 24, 'bold'),
            bg=self.themes[self.current_theme]['bg'],
            fg=self.themes[self.current_theme]['fg']
        )
        title_label.pack(pady=20)
        
        # Search Frame
        search_frame = ttk.LabelFrame(main_container, text="Search Details", padding="20")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        # Song entry
        ttk.Label(search_frame, text="Song Title:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.song_entry = ttk.Entry(search_frame, width=40)
        self.song_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Artist entry
        ttk.Label(search_frame, text="Artist Name:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.artist_entry = ttk.Entry(search_frame, width=40)
        self.artist_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Language selection
        ttk.Label(search_frame, text="Translate to:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(
            search_frame,
            textvariable=self.language_var,
            values=list(self.languages.keys()),
            state='readonly',
            width=37
        )
        self.language_combo.set('English')
        self.language_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(search_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Search button
        search_btn = tk.Button(
            buttons_frame,
            text="🔍 Search Lyrics",
            command=self.search_lyrics,
            bg=self.themes[self.current_theme]['button'],
            fg="white",
            font=('Helvetica', 11, 'bold'),
            cursor="hand2"
        )
        search_btn.pack(side="left", padx=5)
        
        # Add to Favorites button
        fav_btn = tk.Button(
            buttons_frame,
            text="❤ Save to Favorites",
            command=self.save_to_favorites,
            bg=self.themes[self.current_theme]['button'],
            fg="white",
            font=('Helvetica', 11),
            cursor="hand2"
        )
        fav_btn.pack(side="left", padx=5)
        
        # Favorites Frame
        favorites_frame = ttk.LabelFrame(main_container, text="Favorites", padding="10")
        favorites_frame.pack(fill="x", padx=20, pady=5)
        
        # Favorites Dropdown
        self.favorites_var = tk.StringVar()
        self.favorites_combo = ttk.Combobox(
            favorites_frame,
            textvariable=self.favorites_var,
            values=list(self.favorites.keys()),
            state='readonly',
            width=50
        )
        self.favorites_combo.pack(side="left", padx=5, pady=5)
        self.favorites_combo.bind('<<ComboboxSelected>>', self.load_favorite_song)
        
        # Export Frame
        export_frame = ttk.Frame(favorites_frame)
        export_frame.pack(side="right", padx=5)
        
        # Export buttons
        ttk.Button(export_frame, text="📄 Export TXT", command=self.export_txt).pack(side="left", padx=2)
        ttk.Button(export_frame, text="📑 Export PDF", command=self.export_pdf).pack(side="left", padx=2)
        ttk.Button(export_frame, text="▶ Play on YouTube", command=self.play_on_youtube).pack(side="left", padx=2)
        
        # Lyrics Display
        lyrics_frame = ttk.LabelFrame(main_container, text="Song Lyrics", padding="20")
        lyrics_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Lyrics text widget
        self.lyrics_text = tk.Text(
            lyrics_frame,
            wrap=tk.WORD,
            font=('Helvetica', 11),
            bg=self.themes[self.current_theme]['text_bg'],
            fg=self.themes[self.current_theme]['fg'],
            padx=10,
            pady=10
        )
        self.lyrics_text.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(lyrics_frame, orient="vertical", command=self.lyrics_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.lyrics_text.configure(yscrollcommand=scrollbar.set)

    def translate_text(self, text, target_lang):
        try:
            if target_lang == 'en':
                return text
            translator = GoogleTranslator(source='auto', target=target_lang)
            max_length = 5000
            if len(text) > max_length:
                chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
                translated_chunks = [translator.translate(chunk) for chunk in chunks]
                return ' '.join(translated_chunks)
            return translator.translate(text)
        except Exception as e:
            return f"Translation Error: {str(e)}"

    def search_lyrics(self):
        song = self.song_entry.get().strip()
        artist = self.artist_entry.get().strip()
        target_language = self.languages[self.language_var.get()]
        
        if not song or not artist:
            messagebox.showerror("Error", "Please enter both song and artist names")
            return
        
        self.lyrics_text.delete(1.0, tk.END)
        self.lyrics_text.insert(tk.END, "Searching and translating lyrics...")
        self.root.update()
        
        try:
            song = self.genius.search_song(song, artist)
            self.lyrics_text.delete(1.0, tk.END)
            
            if song:
                translated_title = self.translate_text(song.title, target_language)
                translated_artist = self.translate_text(song.artist, target_language)
                translated_lyrics = self.translate_text(song.lyrics, target_language)
                
                formatted_lyrics = f"🎵 {translated_title} - {translated_artist}\n"
                formatted_lyrics += "=" * 50 + "\n\n"
                formatted_lyrics += translated_lyrics
                
                self.lyrics_text.insert(tk.END, formatted_lyrics)
            else:
                self.lyrics_text.insert(tk.END, "Lyrics not found for the specified song")
        except Exception as e:
            self.lyrics_text.delete(1.0, tk.END)
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme['bg'])
        
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Frame, ttk.Frame)):
                widget.configure(bg=theme['bg'])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=theme['bg'], fg=theme['fg'])
            elif isinstance(widget, tk.Text):
                widget.configure(bg=theme['text_bg'], fg=theme['fg'])
                
        self.settings['theme'] = self.current_theme
        self.save_settings()

    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()

    def save_to_favorites(self):
        current_song = self.song_entry.get().strip()
        current_artist = self.artist_entry.get().strip()
        
        if not current_song or not current_artist:
            messagebox.showwarning("Warning", "Please enter song and artist first")
            return
            
        key = f"{current_song} - {current_artist}"
        self.favorites[key] = {
            'song': current_song,
            'artist': current_artist
        }
        self.save_favorites()
        self.update_favorites_list()
        messagebox.showinfo("Success", "Song added to favorites!")

    def load_favorite_song(self, event=None):
        selected = self.favorites_var.get()
        if selected in self.favorites:
            song_data = self.favorites[selected]
            self.song_entry.delete(0, tk.END)
            self.song_entry.insert(0, song_data['song'])
            self.artist_entry.delete(0, tk.END)
            self.artist_entry.insert(0, song_data['artist'])
            self.search_lyrics()

    def export_txt(self):
        if not self.lyrics_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No lyrics to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialdir=os.path.expanduser("~\\Documents")
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.lyrics_text.get(1.0, tk.END))
            messagebox.showinfo("Success", "Lyrics exported successfully!")

    def export_pdf(self):
        if not self.lyrics_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No lyrics to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialdir=os.path.expanduser("~\\Documents")
        )
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            lyrics = self.lyrics_text.get(1.0, tk.END).split('\n')
            for line in lyrics:
                pdf.cell(0, 10, txt=line, ln=True)
            
            pdf.output(file_path)
            messagebox.showinfo("Success", "Lyrics exported to PDF!")

    def play_on_youtube(self):
        song = self.song_entry.get().strip()
        artist = self.artist_entry.get().strip()
        if song and artist:
            query = f"{song} {artist}".replace(" ", "+")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            self.settings = {'theme': 'light'}

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)

    def load_favorites(self):
        try:
            with open('favorites.json', 'r') as f:
                self.favorites = json.load(f)
        except:
            self.favorites = {}

    def save_favorites(self):
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites, f)

    def update_favorites_list(self):
        self.favorites_combo['values'] = list(self.favorites.keys())

# ... previous code remains the same ...

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricsExtractorGUI(root)
    root.mainloop()
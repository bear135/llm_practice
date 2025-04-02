import tkinter as tk
from tkinter import filedialog
import pyttsx3
from tkinter import ttk  # Import Combobox

# Global variables
file_path = ""
sentences = []
current_sentence_index = 0
engine = pyttsx3.init()
sentence_number_combo = None  # Declare Combobox
progress_label = None

def select_file():
    global file_path, sentences, current_sentence_index, sentence_number_combo, progress_label
    file_path = filedialog.askopenfilename(initialdir="./script", title="Select a Text File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            sentences = text.splitlines()  # Split into sentences
            current_sentence_index = 0
            text_area.delete("1.0", tk.END)  # Clear the text area

            # Populate sentence number dropdown
            sentence_numbers = [str(i + 1) for i in range(len(sentences))]
            sentence_number_combo['values'] = sentence_numbers
            sentence_number_combo.set(sentence_numbers[0])  # Set initial value
            current_sentence_index = int(sentence_number_combo.get()) - 1

            # Initialize progress label
            progress_label.config(text=f"Progress (1/{len(sentences)})")
            current_sentence_index = int(sentence_number_combo.get()) - 1

            display_next_sentence()

def display_next_sentence():
    global current_sentence_index, progress_label
    try:
        current_sentence_index = int(sentence_number_combo.get()) - 1
    except:
        current_sentence_index = 0

    if file_path and current_sentence_index < len(sentences):
        sentence = sentences[current_sentence_index].strip()
        if sentence:
            text_area.insert(tk.END, sentence + '\n\n')
            speak_sentence(sentence)
            if current_sentence_index < len(sentences) - 1:
                current_sentence_index += 1
                sentence_number_combo.set(str(current_sentence_index + 1))
                progress_label.config(text=f"Progress ({current_sentence_index + 1}/{len(sentences)})")
            else:
                text_area.insert(tk.END, "End of file.\n")
    elif current_sentence_index >= len(sentences):
        text_area.insert(tk.END, "End of file.\n")

def speak_sentence(sentence):
    voices = engine.getProperty('voices')
    david_voice = None
    for voice in voices:
        if "david" in voice.name.lower():
            david_voice = voice.id
            break

    if david_voice:
        engine.setProperty('voice', david_voice)
    else:
        engine.setProperty('voice', voices[0].id)
        text_area.insert(tk.END, "David voice not found, using default voice.\n")

    engine.say(sentence)
    engine.runAndWait()

# Main window
root = tk.Tk()
root.title("English Learning Program")

# Text area and Scrollbar
text_frame = tk.Frame(root)
text_frame.pack(pady=10)

text_scrollbar = tk.Scrollbar(text_frame)
text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_area = tk.Text(text_frame, height=20, width=70, font=("Arial", 13), yscrollcommand=text_scrollbar.set)
text_area.pack(side=tk.LEFT)

text_scrollbar.config(command=text_area.yview)

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

# Progress Label
progress_label = tk.Label(button_frame, text="Progress (0/0)", font=("Arial", 12))
progress_label.pack(side=tk.LEFT, padx=10)

# Sentence Number Combobox
sentence_number_combo = ttk.Combobox(button_frame, width=5, font=("Arial", 12))
sentence_number_combo.pack(side=tk.LEFT, padx=10)

# Select File button
select_button = tk.Button(button_frame, text="Select Text File", command=select_file, font=("Arial", 12))
select_button.pack(side=tk.LEFT, padx=10)

# Run button
run_button = tk.Button(button_frame, text="RUN", command=display_next_sentence, font=("Arial", 12))
run_button.pack(side=tk.LEFT, padx=10)

# End button
end_button = tk.Button(button_frame, text="End", command=root.destroy, font=("Arial", 12))
end_button.pack(side=tk.LEFT, padx=10)

root.mainloop()

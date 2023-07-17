import requests
import json
import tkinter as tk
from api_keys import MY_API_KEY

DETECT_LANGUAGE_API_ENDPOINT = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"
SUPPORTED_LANGUAGES_API_ENDPOINT = "https://google-translate1.p.rapidapi.com/language/translate/v2/languages"
TRANSLATE_API_ENDPOINT = "https://google-translate1.p.rapidapi.com/language/translate/v2"

RAPID_API_KEY = MY_API_KEY

def detect_language():
    text = input_text.get("1.0", "end-1c")

    detect_query_params = {"q": text}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }
    response = requests.post(DETECT_LANGUAGE_API_ENDPOINT, data=detect_query_params, headers=headers)
    detected_language = response.json()['data']['detections'][0][0]['language']
   
    translate_from_var.set(detected_language)

def get_supported_languages():
    query_params = {"target": "en"}

    headers = {
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }
    response = requests.get(SUPPORTED_LANGUAGES_API_ENDPOINT, headers=headers, params=query_params)
    supported_languages = response.json()['data']['languages']
    return {language['language']: language['name'] for language in supported_languages}

def translate_text():
    text = input_text.get("1.0", "end-1c")  # Get input from text widget
    translate_from = translate_from_var.get()
    translate_to = translate_to_var.get()
    
    translate_query_params = {
        "q": text,
        "target": translate_to,
        "source": translate_from
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }
    response = requests.post(TRANSLATE_API_ENDPOINT, data=translate_query_params, headers=headers)
    translated = response.json()['data']['translations'][0]['translatedText']

    output_text.delete("1.0", "end")  # Clear previous output
    output_text.insert("1.0", translated)  # Display the translated text


root = tk.Tk()
root.title("Language Translator")
root.geometry("500x500")

# Input and Output frames
input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, padx=10, pady=10)

output_frame = tk.Frame(root)
output_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# From language dropdown
from_lang_label = tk.Label(input_frame, text="Translate from:")
from_lang_label.pack()
supported_languages = get_supported_languages()
translate_from_var = tk.StringVar(root)
translate_from_var.set("Select a language")
from_lang_dropdown = tk.OptionMenu(input_frame, translate_from_var, *supported_languages.keys())
from_lang_dropdown.pack()

# Detect language button
detect_button = tk.Button(input_frame, text="Detect Language", command=detect_language)
detect_button.pack()

# Input text box
input_text = tk.Text(input_frame, height=12, width=25)
input_text.pack()

# To language dropdown
to_lang_label = tk.Label(output_frame, text="Translate to:")
to_lang_label.pack()
translate_to_var = tk.StringVar(root)
translate_to_var.set("Select a language")
to_lang_dropdown = tk.OptionMenu(output_frame, translate_to_var, *supported_languages.keys())
to_lang_dropdown.pack()

# Translate button
translate_button = tk.Button(root, text="Translate", command=translate_text)
translate_button.pack(pady=10)

# Output text box
output_text = tk.Text(output_frame, height=14.5, width=25)
output_text.pack()

root.mainloop()
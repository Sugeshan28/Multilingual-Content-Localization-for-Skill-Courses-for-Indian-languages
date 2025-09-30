# ==============================================================================
# Step 1: Install All Necessary Libraries
# ==============================================================================
print("Installing libraries...")
# We need transformers for the captioning model and google-generativeai for translation.
# !pip install -q transformers torch pillow google-generativeai
print("Installation complete.")

# ==============================================================================
# Step 2: Imports and Setup
# ==============================================================================
from transformers import pipeline
from PIL import Image
import google.generativeai as genai
import torch
import sys

# --- Configure your Gemini API Key ---
# IMPORTANT: Replace the placeholder text with your actual key.
try:
    my_api_key = "AIzaSyC8ZPUoo4ONU9XAZReN8mletAYjP6FL8C4"
    if "PASTE_YOUR_API_KEY_HERE" in my_api_key:
      print("Please replace 'PASTE_YOUR_API_KEY_HERE' with your actual Gemini API key.", file=sys.stderr)
    genai.configure(api_key=my_api_key)
except Exception as e:
    print(e, file=sys.stderr)
    print("\nThere might be an issue with your API key configuration.", file=sys.stderr)

# --- Define the path to your image ---
# IMPORTANT: Replace this with the correct path to an image on your system.
# If using Google Colab, upload the image first.
image_path = r"C:\Users\Sugeshan\Pictures\1663518.jpg"

# ==============================================================================
# Step 3: Initialize Both Models
# ==============================================================================
try:
    print("Initializing models...")
    # Initialize the Hugging Face model for image captioning
    captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

    # Initialize the Gemini model for translation
    translator_model = genai.GenerativeModel('gemini-2.5-flash')
    print("Models initialized successfully.")
except Exception as e:
    print(f"Error during model initialization: {e}", file=sys.stderr)
    captioner = None
    translator_model = None

# ==============================================================================
# Step 4: Run the Full Workflow
# ==============================================================================
if captioner and translator_model:
    try:
        print("\n--- Starting Workflow ---")
        # --- Part 1: Generate the English Caption ---
        print(f"Loading image: {image_path}")
        image = Image.open(image_path)
        
        print("Generating caption for the image...")
        caption_result = captioner(image)
        english_caption = caption_result[0]['generated_text']
        print(f"Generated English Caption: '{english_caption}'")

        # --- Part 2: Translate the Caption to Casual Tamil ---
        print("Translating the caption to Tamil...")
        # The caption now becomes the input for our translation prompt
        prompt = f"""Translate the English sentence into a single line of casual, spoken Tamil, written in the Tamil script. Provide only the direct translation.

English: "Hey bro, what are you doing?"
Casual Tamil: "ஏய் மச்சான், என்ன பண்ற?"

English: "{english_caption}"
Casual Tamil:
"""
        
        response = translator_model.generate_content(prompt)
        tamil_translation = response.text.strip()

        # --- Part 3: Display the Final Result ---
        print("\n--- Final Result ---")
        print(f"Image Source: {image_path}")
        print(f"English Description: {english_caption}")
        print(f"Casual Tamil Translation: {tamil_translation}")

    except FileNotFoundError:
        print(f"\nERROR: The image file was not found at '{image_path}'. Please check the path and try again.", file=sys.stderr)
    except Exception as e:
        print(f"\nAn error occurred during the workflow: {e}", file=sys.stderr)
else:
    print("Workflow could not start due to model initialization errors.", file=sys.stderr)
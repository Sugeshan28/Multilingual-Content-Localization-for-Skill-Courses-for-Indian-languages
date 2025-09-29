import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer


device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

local_model_path = r"D:\Hugging_face_models\models--ai4bharat--indic-parler-tts\snapshots\7b527af5ee8ed1f9a28d80b19703ed9bb8ba10ca" # <--- MAKE SURE THIS PATH IS CORRECT
print(f"Loading model and tokenizer from local path: {local_model_path}...")

try:
    model = ParlerTTSForConditionalGeneration.from_pretrained(local_model_path).to(device)
    tokenizer = AutoTokenizer.from_pretrained(local_model_path)
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model from local path: {e}")
    exit()

with open('db/multmedia/text/nextext.txt') as op:
    result = op.read()

tamil_text = result
description = "A male speaker reciting a sentence in Tamil with clear natural looking voice."

print("Preparing input text...")


tokenized_description = tokenizer(description, return_tensors="pt").to(device) 

prompt_input_ids = tokenizer(tamil_text, return_tensors="pt").input_ids.to(device)


print("Generating audio... (This may take a moment)")
try:

    generation = model.generate(
        **tokenized_description,
        prompt_input_ids=prompt_input_ids,
        do_sample=False,
        temperature=0.6,
        top_k=5,
        repetition_penalty=1.2
    ).to(torch.float32)

    audio_arr = generation.cpu().numpy().squeeze()

    # 5. Save the Audio
    sf.write(
        "tamil_output_final.wav",
        audio_arr,
        model.config.sampling_rate
    )
    print("Audio generation complete! Saved as tamil_output_final.wav")

except Exception as e:
    print(f"An error occurred during audio generation: {e}")
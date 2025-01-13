from TTS.api import TTS
import re

def preprocess_text(text):
    """
    Preprocess the input text by replacing unsupported characters and cleaning up.
    """
    ipa_to_text = {
        "æ": "a",
        "θ": "th",
        "ɪ": "i",
        "ð": "th",
        "ɚ": "er",
        "ʒ": "zh",
        "ʃ": "sh",
        "ŋ": "ng",
        "oʊ": "o",
        "͡": "",  # Unsupported character
    }

    # Replace IPA symbols and unsupported characters
    for ipa, replacement in ipa_to_text.items():
        text = text.replace(ipa, replacement)

    # Remove any remaining unsupported non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    return text

def ensure_minimum_text_length(text, min_length=100):
    """
    Ensures the input text is long enough for the TTS model.
    Adds placeholder text if needed.
    """
    if len(text.strip()) < min_length:
        print(f"Warning: Input text is too short. Padding it to meet minimum length of {min_length}.")
        text += " This is additional placeholder text added to meet the input requirements for the TTS model."
    return text

def generate_audio_with_coqui(input_file, output_audio_file):
    """
    Generates audio from a text file using Coqui TTS.
    """
    try:
        # Use a stable pre-trained model
        tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", gpu=False)

        # Read the narration script
        with open(input_file, 'r', encoding='utf-8') as file:
            narration_script = file.read()

        # Preprocess and validate the text
        narration_script = ensure_minimum_text_length(preprocess_text(narration_script))

        # Debug the processed text
        print(f"Processed text length: {len(narration_script)}")
        print(f"Processed text preview: {narration_script[:100]}...")

        # Generate and save the audio
        tts.tts_to_file(text=narration_script, file_path=output_audio_file)
        print(f"Audio file has been generated and saved to: {output_audio_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "chapters_output/1_narration.txt"
    output_audio_file = "chapters_output/1_narration.wav"

    print("Generating audio from narration script...")
    generate_audio_with_coqui(input_file, output_audio_file)

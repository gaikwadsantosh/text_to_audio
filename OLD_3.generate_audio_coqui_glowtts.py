from TTS.api import TTS
import re

def clean_hidden_characters(text):
    """
    Removes hidden or invisible characters from the text.
    """
    return ''.join(char for char in text if char.isprintable())

def preprocess_text(text):
    """
    Preprocesses text for TTS compatibility by normalizing quotes and removing non-ASCII characters.
    """
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')  # Normalize quotes
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove any remaining non-ASCII characters
    return text

def ensure_minimum_text_length(text, min_length=100):
    """
    Ensures the input text meets the minimum length for TTS models.
    Adds placeholder text if it is too short.
    """
    if len(text.strip()) < min_length:
        print(f"Warning: Input text is too short. Padding it to meet minimum length of {min_length}.")
        text += " This is additional placeholder text added to meet input size requirements."
    return text

def generate_audio_with_coqui(input_file, output_audio_file):
    """
    Reads a text file, cleans, preprocesses, validates, and generates audio using Coqui TTS.
    """
    try:
        # Step 1: Read the text file
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        # Step 2: Remove hidden characters
        text = clean_hidden_characters(text)

        # Step 3: Preprocess the text
        text = preprocess_text(text)

        # Step 4: Validate text length
        text = ensure_minimum_text_length(text)

        # Step 5: Generate audio using Coqui TTS
        tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", gpu=False)
        tts.tts_to_file(text=text, file_path=output_audio_file)

        print(f"Audio file has been generated and saved to: {output_audio_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "chapters_output/1_narration.txt"  # Replace with your input file path
    output_audio_file = "1_narration_output.wav"  # Replace with your desired output file path

    print("Processing text and generating audio...")
    generate_audio_with_coqui(input_file, output_audio_file)

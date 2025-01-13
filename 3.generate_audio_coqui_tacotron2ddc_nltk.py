from TTS.api import TTS
import re
from nltk.tokenize import sent_tokenize
import nltk

nltk.data.path.append(r"C:\Users\gaikw\AppData\Roaming\nltk_data")
# Ensure NLTK punkt tokenizer resource is downloaded
nltk.download('punkt')


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


def split_text_into_sentence_chunks(text, max_chunk_length=300):
    """
    Splits the text into chunks based on sentences, ensuring each chunk does not exceed the max_chunk_length.
    """
    sentences = sent_tokenize(text)  # Split text into sentences
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_length:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:  # Add the last chunk if it exists
        chunks.append(current_chunk.strip())

    return chunks


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

        # Step 5: Split the text into sentence-based chunks
        chunks = split_text_into_sentence_chunks(text, max_chunk_length=300)

        # Initialize TTS model
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=False)

        # Step 6: Process each chunk and save the audio
        for i, chunk in enumerate(chunks):
            chunk_output_file = f"{output_audio_file.replace('.wav', '')}_part{i+1}.wav"
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            tts.tts_to_file(text=chunk, file_path=chunk_output_file)
            print(f"Chunk {i+1} audio saved to: {chunk_output_file}")

        print("Audio generation completed for all chunks.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    input_file = "chapters_output/1DeedsCharacterandDestiny_narration.txt"  # Replace with your input file path
    output_audio_file = "chapters_output/1DeedsCharacterandDestiny_narration.wav"  # Replace with your desired output file path

    print("Processing text and generating audio...")
    generate_audio_with_coqui(input_file, output_audio_file)

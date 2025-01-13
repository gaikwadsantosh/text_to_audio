from gtts import gTTS
import os

def generate_audio_with_gtts(input_file, output_audio_file, language='en'):
    """
    Generates audio from a text file using gTTS (Google Text-to-Speech).

    Args:
        input_file (str): Path to the input text file.
        output_audio_file (str): Path to save the generated audio file.
        language (str): Language code for the voice (default: 'en').
    """
    try:
        # Read the narration script from the file
        with open(input_file, 'r', encoding='utf-8') as file:
            narration_script = file.read()

        # Generate audio with gTTS
        tts = gTTS(text=narration_script, lang=language, slow=False)
        
        # Save the audio to the output file
        tts.save(output_audio_file)
        print(f"Audio file has been generated and saved to: {output_audio_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "chapters_output/1_narration.txt"
    output_audio_file = "chapters_output/1_narration.mp3"

    print("Generating audio from narration script...")
    generate_audio_with_gtts(input_file, output_audio_file)

from pydub import AudioSegment
from pydub import effects
import os

# Load the WAV file
input_file = "audio_process_acx_ffmpeg/combined.wav"  # Replace with your file path
output_file = "audio_process_acx_ffmpeg/combined_acx_compliant.wav"

# Check if the file exists
if not os.path.exists(input_file):
    print(f"The file {input_file} does not exist.")
else:
    # Load the audio file
    try:
        audio = AudioSegment.from_file(input_file)
        print(f"Loaded audio file: {input_file}, Duration: {len(audio) / 1000} seconds")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        exit(1)

    # **Step 1: Set sample rate to 44100 Hz**
    if audio.frame_rate != 44100:
        audio = audio.set_frame_rate(44100)
        print("Sample rate set to 44100 Hz.")

    # **Step 2: Normalize the audio**
    normalized_audio = effects.normalize(audio)
    print("Audio normalized.")

    # **Step 3: Apply a fade-in and fade-out effect**
    faded_audio = normalized_audio.fade_in(2000).fade_out(2000)  # 2 seconds fade
    print("Fade in and fade out applied.")

    # **Step 4: Adjust peak level**
    peak_level = faded_audio.max_dBFS
    if peak_level > -3.0:
        reduction_db = peak_level + 3.0  # Reduce to -3 dB
        adjusted_audio = faded_audio - reduction_db
        print(f"Peak level adjusted by {reduction_db:.2f} dB.")
    else:
        adjusted_audio = faded_audio

    # **Step 5: Adjust RMS level**
    rms_level = adjusted_audio.rms
    target_rms_min = -23.0 * (2**15)  # Convert dB to linear scale for comparison

    if rms_level < target_rms_min:
        gain_needed = (target_rms_min - rms_level) / (2**15)  # Calculate gain needed in dB
        adjusted_audio += gain_needed
        print(f"Applied gain of {gain_needed:.2f} dB to raise RMS level.")

    # **Step 6: Ensure noise floor is acceptable**
    if adjusted_audio.dBFS < -60.0:
        silence = AudioSegment.silent(duration=500)  # Add silence to raise noise floor
        adjusted_audio += silence
        print("Added silence to raise noise floor.")

    # **Step 7: Export the processed audio**
    try:
        adjusted_audio.export(output_file, format="wav")
        print(f"ACX compliant audio exported as {output_file}")
    except Exception as e:
        print(f"Error exporting audio file: {e}")

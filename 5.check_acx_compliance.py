from pydub import AudioSegment
import numpy as np

def analyze_audio(file_path):
    """
    Analyze audio file for ACX compliance.
    """
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Convert to mono for consistent analysis
    if audio.channels > 1:
        audio = audio.set_channels(1)

    # Check bitrate, sample rate, and channels
    sample_rate = audio.frame_rate
    channels = audio.channels
    duration = len(audio) / 1000  # Duration in seconds

    print(f"Sample Rate: {sample_rate} Hz")
    print(f"Channels: {channels}")
    print(f"Duration: {duration} seconds")

    # Extract raw audio data
    samples = np.array(audio.get_array_of_samples())

    # Compute RMS (Root Mean Square)
    rms = np.sqrt(np.mean(samples ** 2))
    rms_db = 20 * np.log10(rms)

    # Compute peak level
    peak = np.max(np.abs(samples))
    peak_db = 20 * np.log10(peak)

    print(f"RMS: {rms_db:.2f} dB (Target: -18 to -23 dB)")
    print(f"Peak Level: {peak_db:.2f} dB (Target: <= -3 dB)")

    # Estimate noise floor (RMS of quietest sections)
    quietest_rms = np.sqrt(np.mean(samples[samples < 0.1 * peak] ** 2))
    noise_floor_db = 20 * np.log10(quietest_rms)
    print(f"Noise Floor: {noise_floor_db:.2f} dB (Target: <= -60 dB)")

    # Check compliance
    print("\nACX Compliance:")
    if -23 <= rms_db <= -18:
        print("✔ RMS is within ACX range.")
    else:
        print("✘ RMS is out of ACX range.")

    if peak_db <= -3:
        print("✔ Peak level is within ACX range.")
    else:
        print("✘ Peak level exceeds ACX range.")

    if noise_floor_db <= -60:
        print("✔ Noise floor is within ACX range.")
    else:
        print("✘ Noise floor exceeds ACX range.")

# Path to your audio file
audio_file = "audio_process_acx_ffmpeg/fixed_rms_normalized.mp3"  # Replace with your file path

# Analyze audio
analyze_audio(audio_file)

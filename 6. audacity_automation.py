import os
import time
import sys

# Define pipe paths for Audacity communication
PIPE_TO_AUDACITY = r"\\.\pipe\ToSrvPipe"
PIPE_FROM_AUDACITY = r"\\.\pipe\FromSrvPipe"

def send_command(command):
    """Send a validated command to Audacity."""
    try:
        if not isinstance(command, str):
            raise ValueError("Command must be a string.")
        if not command.endswith("\n"):
            command += "\n"

        with open(r"\\.\pipe\ToSrvPipe", "w") as pipe_out:
            pipe_out.write("Help:\n")
            #pipe.write(command)
            #pipe.flush()  # Ensure the command is sent immediately
        print(f"Command sent: {command.strip()}")

    except FileNotFoundError:
        print("Error: Audacity pipe not found. Ensure Audacity is running with mod-script-pipe enabled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error writing to ToSrvPipe: {e}")

def read_response():
    """Read the response from Audacity."""
    try:
        with open(PIPE_FROM_AUDACITY, 'r') as pipe:
            response = pipe.read()
        print(f"Response from Audacity: {response.strip()}")
        return response.strip()
    except Exception as e:
        print(f"Error reading from FromSrvPipe: {e}")

def apply_loudness_normalization_and_limiter(input_file, output_file):
    """Automates loudness normalization and limiting in Audacity."""
    try:
        print("Starting Audacity automation...")

        if not os.path.isfile(input_file):
            print(f"Error: Input file '{input_file}' does not exist. Please check the path.")
            sys.exit(1)

        # Step 1: Import the audio file
        abs_input_file = os.path.abspath(input_file)
        print(f"Importing audio file: {abs_input_file}")
        send_command(f'Import2: Filename="{abs_input_file}"')
        time.sleep(3)

        # Step 2: Select all audio
        send_command("SelectAll:")
        time.sleep(1)

        # Step 3: Apply loudness normalization to -18 dB
        send_command('LoudnessNormalization: RmsLevel=-18 Perceived=False')
        time.sleep(3)

        # Step 4: Apply limiter with a soft limit at -3 dB
        send_command('Limiter: Threshold=-3 Type=SoftLimit MakeupGain=No')
        time.sleep(3)

        # Step 5: Export the processed file
        abs_output_file = os.path.abspath(output_file)
        send_command(f'Export2: Filename="{abs_output_file}" NumChannels=1 SampleRate=44100 Format=WAV')
        time.sleep(5)

        # Step 6: Close the project
        send_command("CloseProject:")
        time.sleep(2)

        print(f"Processing complete. File saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Input and output file paths
    input_audio = "audio_process_acx_ffmpeg/combined.wav"
    output_audio = "audio_process_acx_ffmpeg/combined_audacity_normalized.wav"

    input_file = os.path.abspath(input_audio)
    output_file = os.path.abspath(output_audio)

    apply_loudness_normalization_and_limiter(input_file, output_file)

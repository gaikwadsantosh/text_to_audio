Create Environment
----------------------
python -m venv myenv
.\myenv\Scripts\activate

Install ffmpeg For audio processing and check version
----------------------
download ffmpeg and add path in environment variables
ffmpeg --version


Install Dependencies
-----------------------
pip install -r .\requirements.txt

install torch
------------
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


Audio Process
---------------
1. Concatenate and normalize
ffmpeg -f concat -safe 0 -i file_list.txt -af "loudnorm=I=-19:LRA=11:TP=-2" normalized.wav
ffmpeg -i normalized.wav -af "loudnorm=I=-21:LRA=11:TP=-2" normalized_v1.wav

2. Add 1sec silence to both the ends
ffmpeg -i normalized.wav -af "adelay=1000|1000,apad=pad_dur=1" final_with_silence.wav

3. reduce peak levels
ffmpeg -i normalized_v1.wav -af "acompressor=threshold=0.707:ratio=4:attack=5:release=50" peak_reduced.wav

4. reduce noise
ffmpeg -i normalized_v1.wav -af "acompressor=threshold=0.707:ratio=4:attack=5:release=50" peak_reduced.wav

5. Convert to MP3
ffmpeg -i peak_reduced.wav -codec:a libmp3lame -b:a 192k final_output.mp3

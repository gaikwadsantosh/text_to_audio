import streamlit as st
from pathlib import Path
import sounddevice as sd
import soundfile as sf
from New_generate_audio_coqui_tacotron2ddc_nltk import (
    generate_audio_with_coqui_single_chunk,
    split_text_into_sentence_chunks,
)
import asyncio
import warnings

warnings.filterwarnings("ignore", message="Tried to instantiate class '__path__._path'")


async def play_audio_async(file_path: str):
    """Play a single audio file asynchronously."""
    try:
        data, samplerate = sf.read(file_path)
        sd.play(data, samplerate)
        # Wait for the playback duration asynchronously
        await asyncio.sleep(len(data) / samplerate)
    except Exception as e:
        st.error(f"Error during audio playback: {e}")


async def process_and_play_chunks_concurrently(chunks, output_dir):
    """Process and play each chunk concurrently."""
    for i, chunk in enumerate(chunks):
        chunk_output_file = output_dir / f"generated_audio_part{i+1}.wav"
        try:
            # Start processing the chunk asynchronously
            processing_task = asyncio.to_thread(
                generate_audio_with_coqui_single_chunk, chunk, str(chunk_output_file)
            )
            st.info(f"Processing chunk {i+1}/{len(chunks)}...")

            # Start playing the previously processed chunk, if available
            if i > 0:
                previous_chunk_file = output_dir / f"generated_audio_part{i}.wav"
                st.info(f"Playing chunk {i}...")
                await play_audio_async(str(previous_chunk_file))

            # Wait for processing to complete
            await processing_task
            st.success(f"Chunk {i+1} processed: {chunk_output_file}")

        except Exception as e:
            st.error(f"An error occurred while processing chunk {i+1}: {e}")

    # Play the last chunk after all processing is done
    st.info(f"Playing final chunk...")
    final_chunk_file = output_dir / f"generated_audio_part{len(chunks)}.wav"
    await play_audio_async(str(final_chunk_file))


def main():
    st.title("Text-to-Speech Audio Generator with Real-Time Playback")

    uploaded_file = st.file_uploader("Upload a Text File", type=["txt"])

    if uploaded_file is not None:
        input_file = Path("uploaded_text.txt")
        with open(input_file, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"File uploaded: {input_file}")

        with open(input_file, "r", encoding="utf-8") as f:
            text_content = f.read()
        st.text_area("Text File Content", text_content, height=200)

        output_dir = Path("output_audio")
        output_dir.mkdir(exist_ok=True)

        chunks = split_text_into_sentence_chunks(text_content, max_chunk_length=300)

        if st.button("Generate Audio and Play"):
            asyncio.run(process_and_play_chunks_concurrently(chunks, output_dir))


if __name__ == "__main__":
    main()

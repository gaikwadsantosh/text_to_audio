from openai import OpenAI

# Set your OpenAI API key
api_key = "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"


def generate_narration_script(input_text):
    """
    Generates a narratable script from input text using OpenAI API.
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Prompt for generating the narration script
    prompt = f"""
    You are a professional script formatter specializing in creating text-to-speech narration scripts. Your task is to refine the given input text into a clean, narratable script that adheres to the following guidelines:
    - Remove unnecessary elements such as page numbers, special characters, and irrelevant symbols that are not suitable for narration.
    - Maintain the original wording of the text without introducing any new words or changing the meaning of existing content.
    - Structure the output for natural-sounding narration, ensuring clarity, flow, and engagement.
    - Ensure the final output is formatted to be directly fed into a text-to-speech generator for high-quality audio production.

    ### Input Text:
    {input_text}

    ### Output Requirements:
    Provide the formatted script as plain text, structured in a way that is easy to narrate, with proper line breaks, spacing, and flow. Avoid including any unnecessary metadata or instructions.
    """

    try:
        # Use OpenAI API to generate the formatted script
        response_obj = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that formats text for narration."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=3000
        )

        narration_script = response_obj.choices[0].message.content.strip()

        # Validate response
        if not narration_script:
            return "Error: Failed to generate the narration script. The response was empty."

        return narration_script

    except Exception as e:
        print(f"An error occurred while generating the narration script: {e}")
        return None

def main():
    # Prompt user for input file and output file
    input_file = "chapters_output/1DeedsCharacterandDestiny.txt"
    output_file = "chapters_output/1DeedsCharacterandDestiny_narration.txt"

    try:
        # Read the input text file
        with open(input_file, 'r', encoding='utf-8') as file:
            input_text = file.read()

        print("Generating narration script...")
        narration_script = generate_narration_script(input_text)

        if narration_script:
            # Save the generated narration script to the output file
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(narration_script)
            print(f"Narration script has been saved to {output_file}.")
        else:
            print("Failed to generate the narration script.")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

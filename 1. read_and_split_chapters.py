import fitz  # PyMuPDF
import os
import re

def extract_toc_and_chapters(pdf_file, output_dir):
    """
    Extract TOC and chapter contents from a PDF file with TOC having links to chapters.

    Args:
        pdf_file (str): Path to the PDF file.
        output_dir (str): Directory to save chapter files.

    Returns:
        list: A list of TOC entries.
    """
    # Open the PDF
    pdf = fitz.open(pdf_file)

    # Get the TOC
    toc = pdf.get_toc()  # Returns a list of TOC entries
    if not toc:
        raise ValueError("No Table of Contents found in the PDF.")

    print("Extracted TOC:", toc)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each TOC entry
    chapters = []
    for entry in toc:
        level, title, page = entry
        chapters.append((title, page))

    # Extract content for each chapter
    for i, (title, page) in enumerate(chapters):
        # Get the start page
        start_page = page - 1  # PyMuPDF uses zero-based indexing for pages

        # Determine the end page
        end_page = chapters[i + 1][1] - 1 if i + 1 < len(chapters) else pdf.page_count

        # Extract text for the chapter
        chapter_text = ""
        for p in range(start_page, end_page):
            chapter_text += pdf.load_page(p).get_text()

        # Skip saving if there's no content
        if not chapter_text.strip():
            print(f"Skipping empty chapter: {title}")
            continue

        # Remove special characters from the title to create a safe filename
        filename = f"{re.sub(r'[^a-zA-Z0-9]', '', title)}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(chapter_text.strip())

        print(f"Saved chapter: {title} to {filepath}")

    # Save the TOC to a text file
    toc_filepath = os.path.join(output_dir, "table_of_contents.txt")
    with open(toc_filepath, "w", encoding="utf-8") as file:
        for i, (title, page) in enumerate(chapters, start=1):
            file.write(f"{i}. {title} (Page {page})\n")

    print("TOC and chapters have been extracted and saved.")
    return chapters

# Example usage
if __name__ == "__main__":
    pdf_file = "Manuscript.pdf"  # Path to your PDF file
    output_dir = "chapters_output"  # Directory to save extracted chapters

    try:
        # Extract TOC and chapters
        toc = extract_toc_and_chapters(pdf_file, output_dir)
        print("TOC and chapter extraction complete.")
    except Exception as e:
        print(f"An error occurred: {e}")

import PyPDF2

def concatenate_pdfs(input_paths, output_path):
    """
    Concatenates multiple PDF files into a single PDF file.
    
    Args:
        input_paths (list): List of paths to the input PDF files.
        output_path (str): Path for the output concatenated PDF file.
    
    Returns:
        None
    """
    writer = PyPDF2.PdfWriter()
    
    for path in input_paths:
        try:
            with open(path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)
        except FileNotFoundError:
            print(f"Error: File '{path}' not found. Skipping.")
        except Exception as e:
            print(f"An error occurred while processing '{path}': {e}")
    
    if len(writer.pages) == 0:
        print("No pages were added to the output. Output file not created.")
        return
    
    try:
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        print(f"Successfully concatenated {len(input_paths)} files into '{output_path}'")
    except Exception as e:
        print(f"Failed to write output file: {e}")

if __name__ == "__main__":
    output_file = "114.pdf"
    input_files = [f"{i}.pdf" for i in range(0, 6)] +[f"f{i}.pdf" for i in range(6, 10)] 
    concatenate_pdfs(input_files, output_file)
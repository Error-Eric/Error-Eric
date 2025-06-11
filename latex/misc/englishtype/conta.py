import PyPDF2

def extract_pages(input_path, output_path):
    try:
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            
            if len(reader.pages) < 4:
                print(f"Error: The PDF must have at least 4 pages. It has {len(reader.pages)} pages.")
                return
            
            writer = PyPDF2.PdfWriter()
            # Add third page (index 2)
            writer.add_page(reader.pages[2])
            # Add fourth page (index 3)
            writer.add_page(reader.pages[3])
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
                
            print(f"Successfully extracted pages 3 and 4 to {output_path}")
    
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    for i in range(1, 10):
        filename = f"{i}.pdf"
        try: extract_pages(filename, f"f{i}.pdf")
        except: pass
    #input_pdf = input("Enter the path of the input PDF file: ").strip()
    #output_pdf = input("Enter the path for the output PDF file: ").strip()
    #extract_pages(input_pdf, output_pdf)
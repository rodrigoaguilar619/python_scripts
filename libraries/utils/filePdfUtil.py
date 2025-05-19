import os
from pypdf import PdfReader, PdfWriter

def remove_pdf_password_file(input_path: str, output_path: str, password: str) -> bool:
    """
    Removes password from a single PDF and saves the unprotected file.

    Args:
        input_path (str): Path to the password-protected PDF.
        output_path (str): Path to save the unprotected PDF.
        password (str): Password used to unlock the PDF.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        reader = PdfReader(input_path)
        print(f"reader.is_encrypted: {reader.is_encrypted} password: {password}") # print(reader.is_encrypted, password)
        if reader.is_encrypted:
            reader.decrypt(password)

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, 'wb') as f:
            writer.write(f)

        print(f"Unprotected: {os.path.basename(input_path)}")
        return True
    except Exception as e:
        print(f"Failed to process {os.path.basename(input_path)}: {e}")
        return False


def remove_pdf_passwords_folder(input_folder: str, output_subfolder: str, password: str):
    """
    Removes password protection from all PDFs in a folder and saves unprotected versions to a subfolder.

    Args:
        input_folder (str): Folder containing the PDFs.
        password (str): Password for unlocking the PDFs.
        output_subfolder (str): Name of subfolder to store unprotected PDFs.
    """
    output_folder = os.path.join(input_folder, output_subfolder)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            remove_pdf_password_file(input_path, output_path, password)
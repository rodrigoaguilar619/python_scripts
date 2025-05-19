import os

from utils.filePdfUtil import remove_pdf_passwords_folder

# Set the path to your folder and the password used on PDFs
input_folder = 'C:/Users/rodri/Downloads/afore'
output_folder = os.path.join(input_folder, 'unprotected_pdfs')
pdf_password = '7xGVMfe55NB7'  # Replace with actual password

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

remove_pdf_passwords_folder(input_folder, output_folder, pdf_password)
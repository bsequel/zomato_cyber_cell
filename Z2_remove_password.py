from pypdf import PdfReader, PdfWriter

def remove_pdf_password(input_pdf_path, output_pdf_path, password):
    """
    Removes password protection from a PDF and saves the unprotected version.

    Args:
        input_pdf_path (str): Full path to the encrypted PDF.
        output_pdf_path (str): Path where the unprotected PDF will be saved.
        password (str): Password for the encrypted PDF.

    Returns:
        bool: True if successful, False if failed.
    """
    try:
        reader = PdfReader(input_pdf_path)

        if reader.is_encrypted:
            result = reader.decrypt(password)
            if result == 0:
                print("❌ Incorrect password or decryption failed.")
                return False

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_pdf_path, "wb") as f_out:
            writer.write(f_out)

        print(f"✅ Password removed. PDF saved as: {output_pdf_path}")
        return True

    except Exception as e:
        print(f"❌ Failed to remove password: {e}")
        return False




# input_pdf = r"C:\Users\bheem\Desktop\sequelstring_zomato\code\cyber_cell_notices\downloads_20250724_080435\[ENCRYPTED] message.pdf"
# output_pdf = r"C:\Users\bheem\Desktop\sequelstring_zomato\code\cyber_cell_notices\downloads_20250724_080435\unprotected.pdf"
# password = "Zomato@123"
# remove_pdf_password(input_pdf, output_pdf, password)

# input_pdf = r"C:\Users\bheem\Desktop\sequelstring_zomato\code\cyber_cell_notices\CYBER_Attachment\20250725_102616_[ENCRYPTED] message.pdf"
# output_pdf = r"C:\Users\bheem\Desktop\sequelstring_zomato\code\cyber_cell_notices\CYBER_Attachment\20250725_102616_[ENCRYPTED] message_un.pdf"
# password = "Zomato@123"
# remove_pdf_password(input_pdf, output_pdf, password)












































# from pypdf import PdfReader, PdfWriter

# # Input password-protected PDF
# input_pdf_path = r"C:\Users\bheem\Desktop\sequelstring_zomato\code\cyber_cell_notices\downloads_20250724_080435\[ENCRYPTED] message.pdf"
# output_pdf_path = r"C:\Users\bheem\Desktop\sequelstring_zomato\code\cyber_cell_notices\downloads_20250724_080435\unprotected.pdf"
# password = "Zomato@123"

# try:
#     # Load the encrypted PDF
#     reader = PdfReader(input_pdf_path)

#     # Decrypt the PDF
#     if reader.is_encrypted:
#         reader.decrypt(password)

#     # Create a new PDF writer (unprotected)
#     writer = PdfWriter()

#     # Add all pages
#     for page in reader.pages:
#         writer.add_page(page)

#     # Write the new PDF without encryption
#     with open(output_pdf_path, "wb") as f_out:
#         writer.write(f_out)

#     print(f"Password removed. Unprotected PDF saved as: {output_pdf_path}")

# except Exception as e:
#     print(f"Failed to remove password: {e}")

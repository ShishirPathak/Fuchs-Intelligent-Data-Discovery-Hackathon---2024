import os
import pandas as pd
from docx import Document
import camelot



def convert_pdf_to_text(file_path):
    filename = os.path.basename(file_path)
    tables = camelot.read_pdf(file_path, pages='all')
    return tables.export("./texts/" + filename + ".csv", "csv")


def convert_excel_to_text(file_path):
    file = pd.ExcelFile(file_path)
    filename = os.path.basename(file_path)
    
    
    for sheet in file.sheet_names:
        if "table" in sheet.lower():
            df = pd.read_excel(file, sheet_name=sheet)
            df.to_csv("./texts/" + filename + "_" + sheet + ".csv", index=False)

    return None


def convert_word_to_text(file_path):
    doc = Document(file_path)
    tables = doc.tables
    data = []
    filename = os.path.basename(file_path)
    
    for table in tables:
        keys = None
        for i, row in enumerate(table.rows):
            text = (cell.text for cell in row.cells)

            if i == 0:
                keys = tuple(text)
            else:
                row_data = dict(zip(keys, text))
                data.append(row_data)

    df = pd.DataFrame(data)
    
    df.to_csv("./texts/" + filename + ".csv", index=False)
    return df


def convert_files_to_text(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()


            if file_extension == ".pdf":
                content = convert_pdf_to_text(file_path)
                continue
            elif file_extension in [".xls", ".xlsx"]:
                content = convert_excel_to_text(file_path)
                continue
            elif file_extension == ".docx":
                content = convert_word_to_text(file_path)
                continue
            elif file_extension == ".txt":
                with open(file_path, "r") as f:
                    content = f.read()
            else:
                print(f"Skipping unsupported file type: {file_path}")
                continue

            # Define the output path for the text file in the output folder
            relative_path = os.path.relpath(root, input_folder)
            output_dir = os.path.join(output_folder, relative_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_file_path = os.path.join(
                output_dir, f"{os.path.splitext(file)[0]}.txt"
            )
            with open(output_file_path, "w") as f:
                f.write(content)
            print(f"Converted {file_path} to {output_file_path}")


# Define the path to the folder containing the documents
input_folder = "startup_packet/synthetic_files/reports_2024-09-26_00-39-17"
output_folder = "./texts"
convert_files_to_text(input_folder, output_folder)

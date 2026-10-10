import cv2
import pytesseract
import pandas as pd
import numpy as np
from PIL import Image
from openpyxl import Workbook
from tkinter import Tk, filedialog


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def process_image_to_excel(image_path: str, output_excel: str = "output_table.xlsx"):
    try:

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image could not be loaded. Please check the file path.")


        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)


        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(morphed, config=custom_config)


        rows = extracted_text.split('\n')
        table_data = []

        for row in rows:
            if row.strip():

                columns = row.split()
                table_data.append(columns)


        if not table_data or all(len(row) != len(table_data[0]) for row in table_data):
            raise ValueError("The image does not contain a recognizable table structure.")


        df = pd.DataFrame(table_data)


        df.to_excel(output_excel, index=False, header=False)
        print(f"Table successfully converted to Excel file: {output_excel}")

    except Exception as e:
        print(f"Error: {e}")


def select_image_and_process():

    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )

    if file_path:
        process_image_to_excel(file_path)
    else:
        print("No file selected.")

select_image_and_process()

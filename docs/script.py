import pdfplumber
import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def clean_number(value: str) -> int:
    """Remove thousands separators and convert to integer."""
    return int(re.sub(r"\.", "", value))

def extract_data_from_pdf(pdf_path: str) -> pd.DataFrame:
    """Extract tabular data from a PDF and structure it in a DataFrame."""
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5 and parts[0] == "D":  # Identifies date rows
                        try:
                            date = parts[1]
                            qty = clean_number(parts[2])
                            change = clean_number(parts[3])
                            cum_qty = clean_number(parts[4])
                            data.append([date, qty, change, cum_qty])
                        except ValueError:
                            continue  # Skip malformed lines
    
    return pd.DataFrame(data, columns=["Delivery Date", "Quantity", "Change", "Cumulative Quantity"])

def compare_pdfs(old_pdf: str, new_pdf: str) -> pd.DataFrame:
    """Compare two PDFs and return a DataFrame with the differences."""
    df_old = extract_data_from_pdf(old_pdf)
    df_new = extract_data_from_pdf(new_pdf)
    
    df_comparison = pd.merge(df_old, df_new, on="Delivery Date", how="outer", suffixes=("_old", "_new"))
    df_comparison.fillna(0, inplace=True)
    
    df_comparison["Quantity Diff"] = df_comparison["Quantity_new"] - df_comparison["Quantity_old"]
    df_comparison["Change Diff"] = df_comparison["Change_new"] - df_comparison["Change_old"]
    df_comparison["Cumulative Quantity Diff"] = df_comparison["Cumulative Quantity_new"] - df_comparison["Cumulative Quantity_old"]
    
    return df_comparison

def select_files() -> None:
    """Opens a GUI for file selection."""
    root = tk.Tk()
    root.withdraw()
    
    old_pdf = filedialog.askopenfilename(title="Select Old PDF", filetypes=[("PDF files", "*.pdf")])
    new_pdf = filedialog.askopenfilename(title="Select New PDF", filetypes=[("PDF files", "*.pdf")])
    
    if old_pdf and new_pdf:
        differences = compare_pdfs(old_pdf, new_pdf)
        print("Differences detected:")
        print(differences)

def main() -> None:
    """Creates the main GUI window."""
    window = tk.Tk()
    window.title("PDF Comparator")
    window.geometry("400x200")
    window.resizable(False, False)
    
    tk.Label(
        window, text="Select the PDFs to compare", padx=10, pady=10
    ).pack()
    
    tk.Button(
        window, text="Select Files", command=select_files, padx=10, pady=5
    ).pack()
    
    window.mainloop()

if __name__ == "__main__":
    main()

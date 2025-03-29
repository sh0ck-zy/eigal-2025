import pandas as pd
import os
import sys
from flask import Flask
from app import db, create_app
from app.models.quantities import Quantity

def import_excel_data(excel_file_path, sheet_name='QUANTIDADES'):
    """
    Import waste calculation data from Excel file into SQLite database
    
    Args:
        excel_file_path: Path to the Excel file
        sheet_name: Name of the sheet containing quantities data (default: 'QUANTIDADES')
    """
    if not os.path.exists(excel_file_path):
        print(f"Error: File {excel_file_path} not found.")
        return False
    
    try:
        # Read the Excel file
        print(f"Reading data from {excel_file_path}, sheet: {sheet_name}...")
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        
        # Display the first few rows to verify
        print("\nPreview of data to be imported:")
        print(df.head())
        
        # Count of records to be imported
        record_count = len(df)
        print(f"\nFound {record_count} records to import.")
        
        # Get column names to map to our database model
        columns = list(df.columns)
        print(f"\nColumns found: {columns}")
        
        # Initialize Flask app to use database
        app = create_app()
        with app.app_context():
            # Clear existing data if needed
            db.session.query(Quantity).delete()
            db.session.commit()
            print("\nCleared existing data from the database.")
            
            # Prompt for confirmation before import
            confirmation = input("\nReady to import data. Continue? (y/n): ")
            if confirmation.lower() != 'y':
                print("Import cancelled.")
                return False
            
            # Import the data
            records_imported = 0
            for index, row in df.iterrows():
                try:
                    # Check if this row has valid data
                    if pd.isna(row.iloc[0]) or pd.isna(row.iloc[1]) or pd.isna(row.iloc[2]):
                        continue
                    
                    # Identify columns - this needs to be adjusted based on your Excel structure
                    print_type = str(row.iloc[0])  # First column - print type
                    print_run = int(row.iloc[1])   # Second column - quantity
                    waste = int(row.iloc[2])       # Third column - waste amount
                    
                    # Optional columns
                    adjustment = int(row.iloc[3]) if len(row) > 3 and not pd.isna(row.iloc[3]) else None
                    
                    # Check if this is a special case row
                    is_special = False
                    if len(row) > 4 and not pd.isna(row.iloc[4]):
                        special_marker = str(row.iloc[4]).lower()
                        is_special = special_marker in ['yes', 'true', '1', 'sim', 'special']
                    
                    # Create and add the record
                    quantity = Quantity(
                        print_type=print_type,
                        print_run=print_run,
                        waste_amount=waste,
                        adjustment=adjustment,
                        is_special_case=is_special
                    )
                    db.session.add(quantity)
                    records_imported += 1
                    
                    # Commit every 100 records to avoid large transactions
                    if records_imported % 100 == 0:
                        db.session.commit()
                        print(f"Imported {records_imported} records...")
                
                except Exception as row_error:
                    print(f"Error importing row {index}: {str(row_error)}")
                    print(f"Row data: {row.values}")
                    continue
            
            # Final commit
            db.session.commit()
            print(f"\nSuccessfully imported {records_imported} records into the database.")
            return True
            
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_data.py <path_to_excel_file> [sheet_name]")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    sheet = sys.argv[2] if len(sys.argv) > 2 else 'QUANTIDADES'
    
    success = import_excel_data(excel_file, sheet)
    if success:
        print("\nData import completed successfully.")
    else:
        print("\nData import failed.")

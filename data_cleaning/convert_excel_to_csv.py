import pandas as pd

def convert_excel_to_csv():
    # Read the Excel file, skipping the first 2 rows
    df = pd.read_excel('illinois.xlsx', skiprows=2)
    
    # Rename the first column to 'county'
    df = df.rename(columns={df.columns[0]: 'county'})
    
    # Clean up county names
    df['county'] = df['county'].str.replace('.', '', regex=False)  # Remove dots
    df['county'] = df['county'].str.replace(', Illinois', '', regex=False)  # Remove ', Illinois'
    
    # Skip the state total row, empty rows, and metadata/footnotes
    df = df[df['county'].notna() & 
            (df['county'] != 'Illinois') & 
            (~df['county'].str.contains('Note:|Source:|Release Date:|Suggested Citation:|Annual Estimates|The Census Bureau', na=False))]
    
    # Extract years 2020-2024
    years_data = df.iloc[:, [0, 2, 3, 4, 5, 6]]  # Select columns for county and years 2020-2024
    
    # Rename the columns
    years_data.columns = ['county', '2020', '2021', '2022', '2023', '2024']
    
    # Save to CSV file
    years_data.to_csv('cleaned_data.csv', index=False)
    print("Conversion completed successfully!")

if __name__ == "__main__":
    convert_excel_to_csv()

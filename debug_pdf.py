import pdfplumber
import matplotlib.pyplot as plt
import traceback
import re 

# It's good practice to define clean_text if it's implicitly needed for understanding text in debug,
# though debug_tablefinder primarily focuses on table structure lines.
def clean_text(text):
    if text is None:
        return ""
    text = ' '.join(text.split())
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    text = re.sub(r'\b(LATAM|SHY|PLATAM)\b', '', text, flags=re.IGNORECASE)
    text = text.replace(',', '')
    return text.strip()


filepath = "uploads/Itinerario Vigente del 14 al 20 JUL.pdf" 
# IMPORTANT: Update this filepath to the actual name of your PDF in the 'uploads' folder
# e.g., "uploads/20250721_122404_Itinerario Vigente del 14 al 20 JUL.pdf"
# Or just "uploads/Itinerario Vigente del 14 al 20 JUL.pdf" if you put the original file there.

# Define your desired table settings for extraction
# These are the settings you want to test and eventually put into app.py
table_settings = {
    "vertical_strategy": "text",  
    "horizontal_strategy": "text", 
    "snap_tolerance": 5,          
    "text_tolerance": 1,          
    "min_words_horizontal": 1,    
    "min_words_vertical": 1,      
    "intersection_tolerance": 2,   
    "join_tolerance": 1 
}

try:
    with pdfplumber.open(filepath) as pdf:
        page = pdf.pages[0]

        print(f"Original Page Dimensions: width={page.width}, height={page.height}")
        
        # Use the exact crop coordinates from your app.py that you want to debug.
        cropped_page = page.crop((20, 160, 580, 705)) # Based on last app.py update

        # Generate the PageImage first from the cropped page
        im = cropped_page.to_image(resolution=200) 
        
        # Now, create a TableFinder object using the page and your settings.
        # This is the object that performs the table detection with your specific settings.
        table_finder = pdfplumber.table.TableFinder(cropped_page, table_settings)
        
        # Pass the TableFinder object to the PageImage.debug_tablefinder() method.
        # This method is designed to accept a TableFinder instance for visualization.
        im.debug_tablefinder(table_finder) 
        
        im.show() # Display the image with debug lines!

        # To also print the extracted tables in the console for review:
        tables = cropped_page.extract_tables(table_settings=table_settings)

        if tables:
            print("\nExtracted Tables:")
            for i, table in enumerate(tables):
                print(f"\nTable {i+1} Raw Data (from cropped area):")
                cleaned_table_data = []
                for row in table:
                    cleaned_row = [clean_text(cell) for cell in row]
                    if any(cell.strip() for cell in cleaned_row):
                        cleaned_table_data.append(cleaned_row)
                
                for row_data in cleaned_table_data:
                    # Print up to 14 columns as expected for the flight data, or fewer if the row is shorter
                    print(row_data[:min(len(row_data), 14)]) 
        else:
            print("\nNo tables extracted with current settings and crop. Try adjusting crop and/or settings.")

except FileNotFoundError:
    print(f"Error: The file '{filepath}' was not found. Please ensure the PDF is in the 'uploads' folder and the filename is correct.")
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
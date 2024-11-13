# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:28:50 2024

@author: Shane
"""

from PIL import Image
import os

def convert_png_to_jpg(quality=85):
    current_directory = os.getcwd()  # Get the current directory where the script is running
    
    # Go through all files in the current directory and subdirectories
    for root, _, files in os.walk(current_directory):
        for file_name in files:
            if file_name.lower().endswith(".png"):
                base_name = os.path.splitext(file_name)[0]  # Get the base name without extension
                input_path = os.path.join(root, file_name)  # Full path to the PNG file
                output_file_name = f"{base_name}.jpg"  # Initial JPG file name
                output_path = os.path.join(root, output_file_name)  # Full path to the output JPG file
                counter = 1  # Initialize the counter

                # Load the PNG image
                try:
                    img = Image.open(input_path)
                    img = img.convert("RGB")  # Convert to RGB (because JPG doesn't support transparency)
                    
                    # Temporarily save the new JPG to a unique name for comparison purposes
                    temp_output_file = os.path.join(root, f"{base_name}_temp.jpg")
                    img.save(temp_output_file, "JPEG", quality=quality)

                    # Check if the target JPG already exists
                    if os.path.exists(output_path):
                        # Compare file sizes
                        existing_jpg_size = os.path.getsize(output_path)
                        new_jpg_size = os.path.getsize(temp_output_file)

                        if new_jpg_size == existing_jpg_size:
                            print(f"{output_file_name} already exists with identical size in {root}, skipping...")
                            os.remove(temp_output_file)  # Remove temporary JPG
                            continue  # Skip this file
                        else:
                            # If sizes differ, proceed to rename with a suffix
                            while os.path.exists(output_path):
                                output_file_name = f"{base_name}_{counter}.jpg"
                                output_path = os.path.join(root, output_file_name)
                                counter += 1
                                # Avoid infinite loops
                                if counter > 100:
                                    print(f"Unable to rename {file_name} in {root}, skipping after 100 attempts.")
                                    os.remove(temp_output_file)  # Clean up temp file
                                    break

                    # If we are not skipping, move the temp file to the correct name
                    if counter <= 100:
                        os.rename(temp_output_file, output_path)  # Rename the temp file
                        print(f"Converted and saved: {file_name} to {output_path} with quality: {quality}")
                        
                        # Delete the original PNG file after successful conversion
                        os.remove(input_path)
                        print(f"Deleted original PNG file: {input_path}")
                    else:
                        os.remove(temp_output_file)  # Clean up if renaming failed

                except Exception as e:
                    print(f"Error converting {file_name} in {root}: {e}")

# Call the function
convert_png_to_jpg(quality=85)

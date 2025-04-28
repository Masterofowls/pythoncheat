import os
import shutil
from pathlib import Path

def create_folders(directory):
    """Create folders for different file types"""
    folders = ['Images', 'Documents', 'Videos', 'Music', 'Others']
    for folder in folders:
        if not os.path.exists(os.path.join(directory, folder)):
            os.makedirs(os.path.join(directory, folder))

def get_file_type(file_extension):
    """Determine the type of file based on its extension"""
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.csv'],
        'Videos': ['.mp4', '.avi', '.mov', '.wmv'],
        'Music': ['.mp3', '.wav', '.flac']
    }
    
    for category, extensions in file_types.items():
        if file_extension.lower() in extensions:
            return category
    return 'Others'

def organize_files(directory):
    """Organize files into appropriate folders"""
    create_folders(directory)
    
    # Iterate through all files in the directory
    for item in os.scandir(directory):
        if item.is_file():
            # Get file extension and determine its type
            file_extension = Path(item.name).suffix
            file_type = get_file_type(file_extension)
            
            # Create source and destination paths
            source = item.path
            destination = os.path.join(directory, file_type, item.name)
            
            # Move file to appropriate folder
            try:
                shutil.move(source, destination)
                print(f"Moved {item.name} to {file_type} folder")
            except Exception as e:
                print(f"Error moving {item.name}: {str(e)}")

if __name__ == "__main__":
    # Get the directory to organize
    target_dir = input("Enter the directory path to organize: ")
    if os.path.exists(target_dir):
        organize_files(target_dir)
        print("Organization complete!")
    else:
        print("Directory does not exist!")
import os
from config import MAX_FILE_CONTENT_LENGTH as max
def get_file_content(working_directory: str, file_path:str) -> str:
    try:

        # Get the absolute path of the working directory
        abs_working_dir = os.path.abspath(working_directory)
        # Get the absolute path of the target file by combining the working directory and the file path
        target_path = os.path.abspath(os.path.join(working_directory, file_path)) 

        #check if file is within the working directory
        if os.path.normpath(os.path.commonpath([abs_working_dir, target_path])) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        #checking if file exists and is a regular file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        #open file for reading
        f = open(os.path.abspath(target_path), 'r')
        content = f.read(max)  # Read up to MAX_FILE_CONTENT_LENGTH characters

        if f.read(1):  # Check if there's more content beyond the limit
            content += f'[...File "{file_path}" truncated at {max} characters]'
        return content

    except Exception as e:
        return f'Error: {str(e)}'


# Schema for get_file_content function for openai function calling
schema_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "gets content from a file, upto a fixed max limit (10000 characters here)",
        "parameters": {
            "type": "object",
            "properties": {
              
                "file_path": {
                    "type": "string",
                    "description": "path of file to read content from, relative to the working directory",
                },
            },
        },
    },
}
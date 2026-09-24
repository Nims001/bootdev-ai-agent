import os

def write_file(working_directory: str, file_path: str, content: str) -> str:


    try:
        abs_working_dir = os.path.abspath(working_directory)
        
        target_path = os.path.abspath(os.path.join(working_directory, file_path)) 
        if os.path.normpath(os.path.commonpath([abs_working_dir, target_path])) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path} as it is a directory"'


        os.makedirs(os.path.dirname(target_path),exist_ok=True)

        f = open(os.path.abspath(target_path), 'w')
        f.write(content)
        f.close()
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f'Error: {str(e)}'


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes content to a file",
        "parameters": {
            "type": "object",
            "properties": {

                "file_path": {
                    "type": "string",
                    "description": "path of file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "content to write to the file"
                },
                 
            },
        },
    },
}
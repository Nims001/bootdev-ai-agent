import os
import subprocess
def run_python_file( working_directory: str, file_path: str, args: list[str] = None) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        
        target_path = os.path.abspath(os.path.join(working_directory, file_path)) 
        if os.path.normpath(os.path.commonpath([abs_working_dir, target_path])) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        # prep the command to run the Python file
        command = ["python3", target_path]
        # add any extra arguments to the command
        if args:
            command.extend(args)

        # run the command and capture the output
       
        result = subprocess.run(command, timeout=30, capture_output=True, text=True,)
        
        return_string = list()
        if result.returncode != 0:
            return_string.append(f'Process exited with code {result.returncode}')
        if result.stderr == ' ' and result.stdout == ' ':
            return_string.append(f'No output produced')
        else:
            if result.stdout:
                return_string.append(f'STDOUT:\n{result.stdout}')
            if result.stderr:
                return_string.append(f'STDERR:\n{result.stderr}')

        return '\n'.join(return_string)

    except Exception as e:
        return f'Error: executing Python file: {str(e)}'


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "executes a Python file with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {

                "file_path": {
                    "type": "string",
                    "description": "path of python file to execute or run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional list of arguments to pass to the Python script"
                }
            },
        },
    },
}
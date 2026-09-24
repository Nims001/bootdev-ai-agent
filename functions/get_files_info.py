from typing import List, Dict   
import os
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str = ".") -> str:
    # get absolute path of working directory
    absolute_path = os.path.abspath(working_directory)
    #print(absolute_path) #checked works
    #directory = os.path.normcase(directory)
    #joining absolute path with directory to get full path of the target directory
    full_path_target = os.path.normpath(os.path.join(absolute_path, directory))

    # checking if our working directory is a parent of the target directory or not if not then raise an exception
    valid_target_dir = os.path.commonpath([absolute_path, full_path_target]) == absolute_path #checks if the target directory is within the working directory
    
    return_list = list()

    
    if not valid_target_dir:
        return_list.append(f'Result for \'{directory}\' directory:')
        return_list.append(f'    Error: Cannot list "{directory}" as it is outside the permitted working directory')
    elif not os.path.isdir(full_path_target):
        return_list.append(f'Result for \'{directory}\' directory:')
        return_list.append(f'    Error: "{directory}" is not a directory')

    else:
        contents = os.listdir(full_path_target)
        
        return_list.append(f'Result for \'{directory}\' directory:')

        for c in contents:
            if (full_path := os.path.join(full_path_target, c)) and os.path.isdir(full_path): 
                is_dir = True
            else:
                is_dir = False
            return_list.append(f' - {c}: file_size={os.path.getsize(os.path.join(full_path_target, c))} bytes, is_dir={is_dir}')

    # now that the path is valid we can get record for each item
    # final return join all elements of return_list with new line and return it
    return "\n".join(return_list)   



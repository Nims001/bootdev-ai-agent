from functions.get_file_content import schema_get_files_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from functions.get_files_info import schema_get_files_info, get_files_info


import json
from collections.abc import Callable

available_functions = [
    schema_get_files_content,
    schema_run_python_file,
    schema_write_file,
    schema_get_files_info,

]


# tool_call is one of the tool call objects in response.choices[0].message.tool_calls
def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    

# defining mapping of function names to their corresponding implementations

    function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
    "get_files_info": get_files_info,
    }
    
    function_args["working_directory"] = "./calculator" # add working_directory to function_args
    return_dict = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": function_map[function_name](**function_args),
   }
    
    return return_dict

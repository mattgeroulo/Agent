import os
from google import genai
from google.genai import types

def get_files_info(working_directory,directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        
        target_dir= os.path.normpath(os.path.join(abs_path,directory))
        #boolean value below
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        dir_contents = os.listdir(target_dir)
        output_string=""
        for data in dir_contents:
            path = os.path.normpath(os.path.join(target_dir,data))
            output_string+=f'- {data}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)} \n'
        print(f"   - get_files_info.py :target dir {target_dir}")
        return output_string
    except:
       return f'Error: get_files_info function call'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
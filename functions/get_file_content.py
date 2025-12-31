import os
MAX_CHARS=10000

from google import genai
from google.genai import types
def get_file_content(working_directory,file_path):
    try:
        try:
            abs_path = os.path.abspath(working_directory)
            
            target_file= os.path.normpath(os.path.join(abs_path,file_path))
            #boolean value below
            valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        

            if not valid_target_file:
                return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(target_file):
                return f'Error: "{target_file}" is not a file'
        except Exception as e:
            return f"Error: os functions {e}"
        try:
            with open(target_file,"r") as f:
                file_content_string = f.read(MAX_CHARS)
        
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            print(f"   - get_file_content.py :target file {target_file}")
            return file_content_string
        except (OSError,UnicodeError) as e:
            return f"Error: reading file path: {file_path}: {e}"
        
    except Exception as e:
        return f"Error: Get file content function {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="lists the characters of a file, up to 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file",
            ),
        },
    ),
)
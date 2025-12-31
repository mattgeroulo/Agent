import os
import subprocess

from google import genai
from google.genai import types

def run_python_file(working_directory,file_path,args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        
        target_file= os.path.normpath(os.path.join(abs_path,file_path))
        
        #boolean value below
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist'
        if not target_file.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
    except Exception as e:
        return f"Error: {e}"
    
    try:
        command =["python",target_file]
        if args:
            command.extend(args)
        process = subprocess.run(command,cwd=abs_path,capture_output=True,text=True,timeout=30)
        output=""
        if process.returncode:
            output+= f"Process exited with code {process.returncode}\n"
        if process.stdout:
            output+=f"STDOUT: {process.stdout} "
        if process.stderr:
            output+=f"STDERR: {process.stderr}"
        if not process.stdout and not process.stderr:
             output+= f"No output produced"
        print(f"  -  run_python_file.py . Target file: {target_file}")
        return output
    except Exception as e:
        return f"Error: {e}"
    
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file, with optional arguments (default is None)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments passed to the Python script",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command-line argument",
                    
                )
            )
        },
    ),
)
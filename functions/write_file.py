import os

def write_file(working_directory,file_path,content):
    try:
        abs_path = os.path.abspath(working_directory)
        
        target_file= os.path.normpath(os.path.join(abs_path,file_path))
        #boolean value below
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{target_file}" as it is a directory'
       
        
        #make sure all parent directories exist:
        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir,exist_ok=True)
            
    except Exception as e:
        return f"Error: os functions {e}"
    
    
    #writing try block
    try:
        with open(target_file,"w") as f:
            f.write(content)
        return f'Successfully wrote to "{target_file}" ({len(content)} characters written)'
            
            
    except Exception as e:
        return f"Error: writing error {e}"
    
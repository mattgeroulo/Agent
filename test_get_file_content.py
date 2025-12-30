from functions.get_file_content import get_file_content

def test_get_files_info():
    print("Lorem Ipsum test:")
    print(get_file_content("calculator","lorem.txt"))
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    
   

if __name__ == "__main__":
    test_get_files_info()
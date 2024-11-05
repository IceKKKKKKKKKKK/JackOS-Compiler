import JackToken
import XMLFormatter
import JackToken
import sys
import os



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_jack_file_or_directory>")
        sys.exit(1)
    path = sys.argv[1] 
    
    # file or directory
    
    XML = XMLFormatter.XMLFormatter(path)
    if os.path.isdir(path):
        # if it is a directory, process all .jack files in the directory
        for file_name in os.listdir(path):
            if file_name.endswith('.jack'):
                file_path = os.path.join(path, file_name)
                XML.process_file(file_path)
    elif os.path.isfile(path) and path.endswith('.jack'):
        # if  it is a .jack file, process the file
        XML.process_file(path)
    else:
        print("Error: The provided path is neither a directory nor a .jack file.")
        sys.exit(1)

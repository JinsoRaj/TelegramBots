import os

def in_file(filename: str, data: str):
    """Check if the data is in the file

    Args:
        filename (str): The file to check
        data (str): The data to check

    Returns:
        bool: True if the data is in the file, False otherwise
    
    NOTE:
        This function will check the file present in the /db directory relative to the current working directory
    """
    with open(f'{os.getcwd()}/db/{filename}', 'r') as f:
        for line in f.read().splitlines():
            if line == data:
                return True
        
        return False
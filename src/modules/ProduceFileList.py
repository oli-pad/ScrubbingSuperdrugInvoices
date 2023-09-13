import os

def ProduceFileList(directory):
    files = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)) and file.endswith('.pdf'):
            files.append(file)
    return files
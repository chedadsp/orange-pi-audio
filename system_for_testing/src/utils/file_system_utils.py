import os


class FileSystemUtils():

    def __init__(self):
        pass


    def get_list_of_file_names_in_directory(self, directory_name, extension=''):
        list_of_file_names = []
        # Read all files from directory (doesn't go into child folders)
        for file in os.listdir(directory_name):
            if extension == '' or file.endswith(extension):
                list_of_file_names.append(file)

        list_of_file_names.sort()
        
        return list_of_file_names


    def make_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    def check_if_exist(self, list_of_directory_paths):
        for directory_path in list_of_directory_paths:
            if not os.path.exists(directory_path):
                return False
        return True
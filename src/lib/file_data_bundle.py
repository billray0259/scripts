from lib.util import find_files


class FileDataBundle(dict):
    def __init__(self, bundle):
        # data is a dictionary of file paths to file contents
        super().__init__(bundle)


    # static method to load from a file
    @staticmethod
    def load(input_file):
        bundle = {}
        with open(input_file, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 3):
                file_path = lines[i].strip()
                bundle[file_path] = lines[i+2].strip()
        return FileDataBundle(bundle)
    

    @staticmethod
    def bundle_directory(directory):
        bundle = {}
        for file in find_files(directory, relative_path=False):
            try:
                with open(file, "r") as f:
                    bundle[file] = f.read()
            except UnicodeDecodeError:
                # count how many bytes are in the file
                with open(file, "rb") as f:
                    f.seek(0, 2)
                    num_bytes = f.tell()
                    bundle[file] = f"Binary file with {num_bytes} bytes"
        return FileDataBundle(bundle)


    def save(self, output_file):
        with open(output_file, "w") as f:
            f.write(str(self))
    

    def __str__(self):
        string = ""
        for file_path, contents in self.items():
            string += f"{file_path}\n"
            string += "```\n"
            string += contents
            string += "\n```\n\n"
        return string

import sys
import tiktoken

from lib.file_data_bundle import FileDataBundle


def prompt_gen(directory, ignore=None):
    """Generates a string with the file structure of the specified directory, and all of the file contents in the format:
    <file_structure>
    
    <file_path>
    ```
    <file_contents>
    ```

    <file_path>
    ```
    <file_contents>
    ```
    ...
    """

    file_bundle = FileDataBundle.bundle_directory(directory)

    if ignore is not None:
        file_bundle.pop(ignore, None)
    
    files = list(file_bundle.keys())
    files.sort()
    files_str = "\n".join(files)
    return f"File Structure:\n{files_str}\n\n{str(file_bundle)}"


def main(source_dir, target_file):
    prompt = prompt_gen(source_dir, ignore=target_file)
    with open(target_file, "w") as f:
        f.write(prompt)
    
    gpt4_encoding = tiktoken.encoding_for_model("gpt-4")
    print(f"GPT-4 prompt length: {len(gpt4_encoding.encode(prompt))}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python prompt.py <source_dir> <target_file>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
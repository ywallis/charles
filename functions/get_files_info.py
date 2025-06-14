import os


def get_files_info(working_directory: str, directory: str | None = None) -> str:
    working_directory_path = os.path.abspath(working_directory)

    if directory is None:
        directory = ""
    directory_path = os.path.join(working_directory_path, directory)
    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'

    if not os.path.abspath(directory_path).startswith(
        os.path.abspath(working_directory_path)
    ):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    output_string = ""

    try:
        files = os.listdir(directory_path)
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            output_string += (
                f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n"
            )

    except Exception as e:
        return f"Error encountered: {e}"

    return output_string

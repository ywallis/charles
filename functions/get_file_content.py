import os

from google.genai import types


def get_file_content(working_directory: str, file_path: str) -> str:
    MAX_LENGTH = 10000

    try:
        working_directory_absolute_path = os.path.abspath(working_directory)
        file_absolute_path = os.path.abspath(
            os.path.join(working_directory_absolute_path, file_path)
        )

        if not file_absolute_path.startswith(working_directory_absolute_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_absolute_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content: str = ""

        with open(file_absolute_path, "r") as file:
            file_content = file.read(MAX_LENGTH)
            if len(file_content) == MAX_LENGTH:
                file_content += (
                    f"[File {file_absolute_path} truncated at {MAX_LENGTH} characters]"
                )

    except Exception as e:
        return f"Error encountered: {e}"

    return file_content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file, limited to the first 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for the file that should be read.",
            ),
        },
    ),
)

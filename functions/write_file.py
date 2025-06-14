import os

from google.genai import types


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_absolute_path = os.path.abspath(working_directory)
        file_absolute_path = os.path.abspath(
            os.path.join(working_directory_absolute_path, file_path)
        )

        if not file_absolute_path.startswith(working_directory_absolute_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file_absolute_path):
            os.makedirs(os.path.split(file_absolute_path)[0], exist_ok=True)

        with open(file_absolute_path, "w") as file:
            file.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes data to a file. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for the file that should be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file.",
            ),
        },
    ),
)

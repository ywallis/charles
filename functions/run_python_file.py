import os
import subprocess

from google.genai import types


def run_python_file(working_directory: str, file_path: str) -> str:
    try:
        working_directory_absolute_path = os.path.abspath(working_directory)
        file_absolute_path = os.path.abspath(
            os.path.join(working_directory_absolute_path, file_path)
        )

        if not file_absolute_path.startswith(working_directory_absolute_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(file_absolute_path):
            return f'Error: File "{file_path}" not found.'

        if os.path.splitext(file_absolute_path)[1] != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        output = subprocess.run(
            ["python3", file_absolute_path],
            cwd=working_directory,
            timeout=30,
            capture_output=True,
            text=True,
        )

    except Exception as e:
        return f"Error: executing Python file: {e}"

    if not output.stdout and not output.stderr:
        return "No output produced"

    if output.returncode != 0:
        return f"STDOUT: {output.stdout}, STDERR: {output.stderr}, Process exited with code {output.returncode}"
    else:
        return f"STDOUT: {output.stdout}, STDERR: {output.stderr}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file. Returns an error if the file doesn't exist or doesn't have a .py extension.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path for the file that should be executed.",
            ),
        },
    ),
)

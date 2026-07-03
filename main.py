import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

tools: Any = [
    {
        "type": "function",
        "name": "get_desktop_files",
        "description": "Get a list of all files on the user's desktop (full paths)",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "type": "function",
        "name": "put_into_folders",
        "description": "Move a list of files (given as full paths) into a category folder on the desktop",
        "parameters": {
            "type": "object",
            "properties": {
                "cat": {
                    "type": "string",
                    "description": "The category/folder name to put the files into, e.g. 'Images', 'Documents'",
                },
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Full paths of the files to move into the folder",
                },
            },
            "required": ["cat", "files"],
        },
    },
]


def get_desktop_files():
    """Return full paths of every file (not folder) sitting directly on the desktop."""
    return [
        os.path.join(DESKTOP_PATH, f)
        for f in os.listdir(DESKTOP_PATH)
        if os.path.isfile(os.path.join(DESKTOP_PATH, f))
    ]


def put_into_folders(cat: str, files: list[str]):
    # Create (or reuse) a category folder on the desktop and move the given files into it
    folder_path = os.path.join(DESKTOP_PATH, cat)
    perm = input(f"Moving {len(files)} files to '{cat}'. Continue? (y/n): ")

    if perm.lower() != "y":
        return []
    os.makedirs(folder_path, exist_ok=True)

    moved = []
    for file_path in files:
        if not os.path.isfile(file_path):
            print(f"Skipping missing file: {file_path}")
            continue
        filename = os.path.basename(file_path)
        destination = os.path.join(folder_path, filename)
        perm2 = input(f"Moving '{filename}' to '{cat}/{filename}'. Continue? (y/n): ")
        if perm2.lower() != "y":
            continue
        else:
            os.rename(file_path, destination)
            moved.append(destination)
            print(f"Moved '{filename}' -> '{cat}/'")

    return moved


available_functions = {
    "get_desktop_files": get_desktop_files,
    "put_into_folders": put_into_folders,
}


def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    input_list: list[Any] = [
        {
            "role": "system",
            "content": (
                "You organize a user's desktop files into category folders. "
                "First call get_desktop_files to see what's there. "
                "Then group the files by category (e.g. Images, Documents, Videos, "
                "Audio, Archives, Installers, Others) based on their file extensions "
                "and names, and call put_into_folders once per category with the full "
                "file paths. When finished, briefly summarize what you did."
            ),
        },
        {"role": "user", "content": "Please organize my desktop files."},
    ]

    while True:
        res = client.responses.create(
            model="gpt-4.1-mini",
            tools=tools,
            input=input_list,
        )

        input_list += res.output

        function_calls = [item for item in res.output if item.type == "function_call"]

        if not function_calls:
            print(res.output_text)
            break

        for item in function_calls:
            func = available_functions.get(item.name)
            if func is None:
                output = f"Unknown function: {item.name}"
            else:
                args = json.loads(item.arguments) if item.arguments else {}
                try:
                    output = func(**args)
                except Exception as e:
                    output = f"Error running {item.name}: {e}"

            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(output),
                }
            )


if __name__ == "__main__":
    main()

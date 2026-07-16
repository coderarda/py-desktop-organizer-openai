# Desktop Organizer

A small AI-powered script that organizes the files on your Desktop into
category folders (e.g. Images, Documents, Videos, Archives) using OpenAI
function calling.

## How it works

1. The script asks an OpenAI model to organize your desktop.
2. The model calls `get_desktop_files` to see what files exist.
3. The model groups the files by category and calls `put_into_folders`
   for each category.
4. The script executes those calls locally, moving the real files into
   folders on your Desktop, and prints a summary when done.

## Requirements

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. Create and activate a virtual environment (already scaffolded in this
   repo under `Lib`/`Scripts`), or create your own:

   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```sh
   pip install openai python-dotenv
   ```

3. Create a `.env` file in the project root with your API key:

   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

```sh
python main.py
```

The script will list your desktop files, ask the model to categorize
them, and move them into matching folders (e.g. `Desktop/Images`,
`Desktop/Documents`) on your Desktop.

> ⚠️ **Warning:** This script moves real files on your Desktop. Back up
> important files or test in a scratch folder before running it on files
> you care about.

## Project Structure

- `main.py` – entry point; defines the OpenAI tools, the file-organizing
  functions, and the agent loop that ties them together.

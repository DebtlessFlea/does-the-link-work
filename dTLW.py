import os
import requests
import subprocess
import platform

def open_text_editor(filename):
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["notepad.exe", filename])
        elif system == "Darwin":
            subprocess.call(["open", filename])
        else:
            subprocess.call(["xdg-open", filename])
    except Exception as e:
        print(f"Failed to open file: {e}")

def create_or_open_input_file(filepath):
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write("# Add one URL per line below this line\n")
        print(f"Created '{filepath}'. Please add your links and save the file.")
    else:
        print(f"Opening existing '{filepath}' for editing...")

    open_text_editor(filepath)
    input("Press Enter when you are done editing the file...")
    print("Please wait...")

def check_links(input_path, output_path, timeout=5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = []

    with open(input_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                results.append(stripped)
            else:
                try:
                    response = requests.head(stripped, allow_redirects=True, timeout=timeout, headers=headers)
                    if response.status_code < 400:
                        results.append(f"(+) {stripped} -> Link works (Status {response.status_code})")
                    else:
                        results.append(f"(-) {stripped} -> Link broken (Status {response.status_code})")
                except requests.exceptions.RequestException as e:
                    results.append(f"(-) {stripped} -> Error: {type(e).__name__}")

    with open(output_path, "w") as f:
        for line in results:
            f.write(line + "\n")

    print(f"Done. Results saved to '{output_path}'.")

    open_text_editor(output_path)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "links.txt")
    output_file = os.path.join(script_dir, "results.txt")

    create_or_open_input_file(input_file)
    check_links(input_file, output_file)

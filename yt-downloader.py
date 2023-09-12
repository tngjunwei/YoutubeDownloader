from pytube import YouTube
import os
import sys
from tqdm import tqdm
from pathvalidate import sanitize_filename
import subprocess

def get_input(num_of_options):
    while True:
        choice = input(f"Select choice (up to {num_of_options})")
        if not choice.isdigit():
            print("Enter a valid number!")
            continue
        
        res = int(choice)-1
        if res < 0 or res >= num_of_options:
            print("Enter a valid number!")
            continue
        
        print()
        return res

def print_divider(length):
    x = "-" * (length + 10)
    print(x)

def get_update_func():
    progress_bar = tqdm(desc="Downloading file: ")
    def update(stream, chunk, bytes_remaining):
        progress_bar.total = stream.filesize
        progress_bar.update(len(chunk))

    return update, progress_bar


def download(url, filename=""):
    DOWNLOAD_DIR = "./downloads"

    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        name = yt.title
    except Exception as e:
        print(e)
        exit(1)

    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    pieces = yt.streams.filter(only_audio=True)
    print(f"Download {name}")
    print_divider(len(name))

    for i, piece in enumerate(pieces):
        print(f"No. {i+1}: {piece}")

    choice = get_input(len(pieces))
    selected = pieces[choice]
    ext = selected.mime_type.split("/")[1]
    print(f"Selected {selected.mime_type}, {selected.abr}")

    name = name if not filename else filename
    name = sanitize_filename(name)
    out_filename = f"{name}.{ext}"
    final_filename = os.path.join(DOWNLOAD_DIR, f"{name}.mp3") if len(filename) == 0 else filename

    update_func, t = get_update_func()
    yt.stream_monostate.on_progress = update_func
    out_file = selected.download(output_path=DOWNLOAD_DIR, filename=out_filename)
    t.close()

    print("Converting file to mp3 format")
    print(final_filename)
    instance = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", '-i', out_file, final_filename])
    if instance.returncode == 0:
        os.remove(out_file)
        print("Done")
    else:
        print("Error converting to mp3")

def run():
    num_of_arguments = len(sys.argv)
    if not (2 <= num_of_arguments <= 3):
        print("USAGE: ./downloader [URL] [optional OUTPUT]")
        exit(1)

    url = sys.argv[1]
    output_name = sys.argv[2] if num_of_arguments == 3 else ""
    download(url, output_name)
    exit(0)

if __name__ == "__main__":
    run()
    
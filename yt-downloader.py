from pytube import YouTube
import os
import sys
from tqdm import tqdm
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


def download(url):
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        name = yt.title
    except Exception as e:
        print(e)
        exit(1)

    pieces = yt.streams.filter(only_audio=True)
    print(f"Download {name}")
    print_divider(len(name))

    for i, piece in enumerate(pieces):
        print(f"No. {i+1}: {piece}")

    choice = get_input(len(pieces))
    selected = pieces[choice]
    print(f"Selected {selected.mime_type}, {selected.abr}")

    filename = f"{name}.mp3"

    update_func, t = get_update_func()
    yt.stream_monostate.on_progress = update_func
    out_file = selected.download(output_path=".")
    t.close()

    dir, base = os.path.split(out_file)

    print(os.path.join(".", base))
    print("Converting file to mp3 format")
    subprocess.run(['ffmpeg', '-i', base, filename])
    print("Done")

def run():
    if len(sys.argv) != 2:
        print("USAGE: ./downloader [URL]")
        exit(1)
    url = sys.argv[1]
    download(url)
    exit(0)

if __name__ == "__main__":
    run()
    
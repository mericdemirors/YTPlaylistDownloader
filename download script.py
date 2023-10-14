from pytube import YouTube, Playlist
import os
import moviepy.editor as mp
import re
from datetime import datetime
from pydub import AudioSegment


def download_playlist(playlist_url, output_folder):
    playlist = Playlist(playlist_url)
    os.makedirs(output_folder, exist_ok=True)
    
    for url in playlist:
        video = YouTube(url)
        stream = video.streams.filter(file_extension="mp4", only_audio=True).first()
        if stream:
            print(f"Downloading: {video.title}")
            stream.download(output_folder)


playlist_url = input("Enter the YouTube playlist URL: ")
current_time = datetime.now().strftime("%H_%M_%S")
output_folder = f"new_down_{current_time}"


download_playlist(playlist_url, output_folder)


def convert_to_mp3(folder):
    current_directory = os.getcwd()
    subfolder_path = os.path.join(current_directory, output_folder)
    subfolder_items = os.listdir(subfolder_path)

    files_sorted_by_creation = sorted(
        [item for item in subfolder_items if os.path.isfile(os.path.join(subfolder_path, item))],
        key=lambda item: os.path.getctime(os.path.join(subfolder_path, item))
    )

    mp3s_subfolder_path = os.path.join(subfolder_path, "mp3s")
    os.makedirs(mp3s_subfolder_path, exist_ok=True)

    for file in files_sorted_by_creation:
        if re.search('.mp4', file):
            mp4_path = os.path.join(folder, file)
            mp3_filename = os.path.splitext(file)[0] + '.mp3'
            mp3_path = os.path.join(mp3s_subfolder_path, mp3_filename)
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)


convert_to_mp3(output_folder)
print("Playlist downloaded and converted to MP3 successfully.")


def merge_mp3_files(input_folder, output_file):
    input_folder = input_folder + "/mp3s"
    subfolder_items = os.listdir(input_folder)
    files_sorted_by_creation = sorted(
        [item for item in subfolder_items if os.path.isfile(os.path.join(input_folder, item))],
        key=lambda item: os.path.getctime(os.path.join(input_folder, item))
    )

    merged_audio = AudioSegment.silent(duration=0)

    for idx, file in enumerate(files_sorted_by_creation):
        print("merging", file)
        audio = AudioSegment.from_mp3(os.path.join(input_folder, file))
        if idx > 0:
            silence = AudioSegment.silent(duration=1000)  # 1 second silence
            merged_audio += silence
        merged_audio += audio

    merged_audio.export(os.path.join(input_folder, output_file), format='mp3')


merged_output_file = "merged_playlist.mp3"
merge_mp3_files(output_folder, merged_output_file)    
print("MP3 files merged successfully.")

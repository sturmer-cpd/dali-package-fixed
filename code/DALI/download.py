from . import utilities as ut
import os
import yt_dlp as youtube_dl

base_url = 'http://www.youtube.com/watch?v='

# Read environment variables
ffmpeg_path = os.getenv('FFMPEG_BINARY', "/home/sagemaker-user/.conda/envs/conda_env/bin/ffmpeg")
ffprobe_path = os.getenv('FFPROBE_BINARY', "/home/sagemaker-user/.conda/envs/conda_env/bin/ffprobe")


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')



def get_my_ydl(directory, name):
    if ut.check_directory(directory):
        outtmpl = os.path.join(directory, f'{name}.%(ext)s')  # Use name here
        ydl_opts = {
            'ffmpeg_location': ffmpeg_path,
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
            'outtmpl': outtmpl,
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'verbose': False,  # Set to True if you want verbose output
            'ignoreerrors': False,
            'external_downloader': 'ffmpeg',
            'nocheckcertificate': True
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ydl.cache.remove()
        return ydl



def audio_from_url(url, name, path_output, errors=[]):
    error = None
    filename = os.path.join(path_output, f'{name}.mp3')  # Assuming the files are saved as .mp3

    # Check if the file already exists
    if os.path.exists(filename):
        print(f"File {filename} already exists. Skipping download.")
        return
    
    print(f"filename: {filename} does NOT exist yet, so will be downloaded now.")
    
    ydl = get_my_ydl(path_output, name)  # Pass name here

    if ydl:
        print("Downloading " + url)
        try:
            ydl.download([base_url + url])
        except Exception as e:
            print("Error downloading {}: {}".format(url, e))
            error = str(e)

    if error:
        errors.append([name, url, error])

    return

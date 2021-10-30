from pytube import YouTube, Playlist
import ffmpeg, os
from pathvalidate import sanitize_filename

def await_user_input(options, allowed_values):
    """
    Waits for valid user input and returns the input.
    """
    
    while True:
        print("Please choose one of the following:")
        for option in options:
            print(f"- {option}")
        user_input = input("Your choice: ").lower()
        if allowed_values.get(user_input, False):
            return allowed_values.get(user_input)
        if user_input in [i.lower() for i in options]:
            return user_input  
        print("Invalid input. Please try again.")


folder = sanitize_filename(input("Folder location: "))
os.system(f"md \"{folder}\"")

url = input("Please enter the url of the video: ")

#url = "https://www.youtube.com/watch?v=Y9nDagqKL7Q&ab_channel=ProZD"
#url = "https://www.youtube.com/playlist?list=PLUkVlwCUGEJ8NaBS64DZrmFFd63RkcKzK"

if "playlist" in url:
    playlist = Playlist(url)
    print(playlist.title)
    choice = await_user_input(["Audio", "Video"], {"a": "audio", "v": "video"})

    if choice == "audio":
        print("Downloading audio...")
        for urli in playlist:
            try:
                yt = YouTube(urli)
                streams = yt.streams.filter(only_audio=True, file_extension='mp4')
                streams.first().download(filename = os.path.join(folder, sanitize_filename(yt.title) + ".mp3") + ".mp3")
                print('Download complete! File saved as ' + os.path.join(folder, sanitize_filename(yt.title) + ".mp3"))
            except Exception:
                print(f'''There was an issue while downloading {yt.title}. This video has been skipped''')

    if choice == "video":
        for urli in playlist:
            try:
                yt = YouTube(urli)
                streams = yt.streams.filter(progressive=True, file_extension='mp4')
                # Remove duplicate resolutions
                newStreams = []
                for i in range(len(streams)):
                    if streams[i].resolution != streams[i-1].resolution:
                        newStreams.append(streams[i])
                streams = newStreams

                #res_choice = await_user_input([str(i.resolution) for i in streams], {str(i.resolution) : i for i in streams})
                streams[0].download(filename = "video.mp4")
                print(f'Download complete! File saved as "{os.path.join(folder, sanitize_filename(yt.title) + ".mp4")}"')
            except Exception:
                print(f'''There was an issue while downloading {yt.title}. This video has been skipped''')
else:
    # Creates Youtube object
    yt = YouTube(url)

    # Gets the video datag
    streams = yt.streams.filter(file_extension='mp4')

    print(f"Video Title: {yt.title}\n")
    choice = await_user_input(["Audio", "Video"], {"a": "audio", "v": "video"})

    if choice == "audio":
        streams = streams.filter(only_audio=True)
        abr_choice = await_user_input([str(i.abr) for i in streams], {str(i.abr) : i for i in streams})
        print("Downloading audio...")
        abr_choice.download(filename = os.path.join(folder, sanitize_filename(yt.title) + ".mp3"))
        print(f'Download complete! File saved as "{os.path.join(folder, sanitize_filename(yt.title) + ".mp3")}"')

    if choice == "video":
        streams = streams.filter(only_video=True)
        # Remove duplicate resolutions
        newStreams = []
        for i in range(len(streams)):
            if streams[i].resolution != streams[i-1].resolution:
                newStreams.append(streams[i])
        streams = newStreams

        res_choice = await_user_input([str(i.resolution) for i in streams], {str(i.resolution) : i for i in streams})

        print("Downloading Video...")
        res_choice.download(filename = "video.mp4")
        print("Download Complete!")
        #print(f'Download complete! File saved as "{os.path.join(folder, yt.title)}.mp4"')

        print("Downloading Audio...")
        yt.streams.filter(file_extension='mp4', only_audio=True).first().download(filename = "audio.mp3")
        print("Download Complete!")
        
        input_audio = ffmpeg.input("audio.mp3")
        input_video = ffmpeg.input("video.mp4")
        
        print("Combining Audio and Video...")
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(os.path.join(folder, sanitize_filename(yt.title) + ".mp4")).run()
        print(f'Combination Complete! File saved as "{os.path.join(folder, yt.title)}.mp4"')
        os.system("rm audio.mp3")
        os.system("rm video.mp4")

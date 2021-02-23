from pytube import YouTube, Playlist
import os
while True:
    url = input("Enter your playlist or video URL: ").strip()
    if url == '' or ' ' in url or 'youtube' not in url:
        print('Please enter a proper Youtube URL\n')
    else: break
url_type = ''
if 'watch' in url: url_type = 'video'
else: url_type = 'playlist'
download_type = input('\nWhat would you like it downloaded as? (audio or video): ')
if any(i in download_type for i in ('video', 'v', 'vid', 'picture', 'movie')):
    download_type = False
else: download_type = True
if url_type == "playlist":
    counter = 0
    pl = Playlist(url)
    for link in pl:
        try:
            video = YouTube(link)
            name = video.streams.filter(only_audio=download_type)[0].download()
            if download_type: os.rename(name, str(name)[:-1] + '3')
            counter += 1
            print(counter)
        except Exception as e:
            print('Error occurred with ' + link, e)
            pass
    print('Download finished')
if url_type == "video":
    try:
        video = YouTube(url)
        name = video.streams.filter(only_audio=download_type)[0].download()
        if download_type: os.rename(name, str(name)[:-1] + '3')
    except Exception as e:
        print('Error occurred with ' + url, e)
    print('Download finished')


    

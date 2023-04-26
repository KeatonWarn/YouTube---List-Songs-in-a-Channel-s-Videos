import os
import googleapiclient.discovery
import googleapiclient.errors
import re

def get_channel_videos(channel_url):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="YOUTUBE_API_KEY_HERE")
    
    channel_id = channel_url.split("/")[-1]
    
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    
    videos = []
    next_page_token = None

    while True:
        playlist_response = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        videos += playlist_response["items"]
        
        next_page_token = playlist_response.get("nextPageToken")

        if next_page_token is None:
            break

    return videos

def parse_video_description(description):
    song_list = []
    pattern = re.compile(r"(?i)(song|music|track):\s*(.*)")
    
    for line in description.splitlines():
        match = pattern.search(line)
        if match:
            song_list.append(match.group(2).strip())
            
    return song_list

def save_videos_to_txt_file(videos, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for video in videos:
            title = video["snippet"]["title"]
            upload_date = video["snippet"]["publishedAt"]
            description = video["snippet"]["description"]
            song_list = parse_video_description(description)

            f.write(f"Title: {title}\n")
            f.write(f"Upload Date: {upload_date}\n")
            f.write("Songs:\n")

            for song in song_list:
                f.write(f"- {song}\n")

            f.write("\n")

if __name__ == "__main__":
    channel_url = input("Enter the YouTube channel URL: ")
    output_file = "video_details.txt"
    
    videos = get_channel_videos(channel_url)
    save_videos_to_txt_file(videos, output_file)
    
    print(f"Video details have been saved to {output_file}")

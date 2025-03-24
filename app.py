import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable

def extract_video_id(url):
    # Regular expression to match YouTube video URLs and extract the video ID
    regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    
    if match:
        return match.group(1)  # Return the video ID
    else:
        return None  # Return None if no match is found

def format_time(seconds):
    # Convert seconds to HH:MM:SS format
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

def get_youtube_transcript(video_input):
    video_id = extract_video_id(video_input)
    
    if video_id:
        try:
            # Generate the iframe HTML code for the video
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            embed_html = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" title="YouTube video" frameborder="0" allowfullscreen></iframe>'
            
            # Fetch the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # Format the transcript into a more readable format with formatted timestamps
            formatted_transcript = "\n".join([f"{format_time(entry['start'])} - {entry['text']}" for entry in transcript])
            
            return embed_html, formatted_transcript
        except VideoUnavailable:
            return None, "Error: This video is unavailable or restricted in your region."
        except TranscriptsDisabled:
            return None, "Error: No transcript is available for this video."
        except Exception as e:
            return None, f"Error: {str(e)}"
    else:
        return None, "Invalid YouTube URL or ID. Please try again with a valid link."

# Streamlit layout
st.title("YouTube Video Transcript Generator")

# Input for YouTube URL
video_url_input = st.text_input("Enter YouTube Video URL", placeholder="Paste YouTube URL here")

if video_url_input:
    # Get the YouTube video transcript
    video_preview, transcript = get_youtube_transcript(video_url_input)
    
    if video_preview:
        st.markdown("### Video Preview")
        st.markdown(video_preview, unsafe_allow_html=True)  # Embed the YouTube video iframe
    
    st.markdown("### Transcript")
    st.text_area("Transcript", transcript, height=300)


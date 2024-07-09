import requests
import csv
import tkinter as tk
import webbrowser
import os

def read_last_emotion_from_csv(csv_file_path):
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = list(csv_reader)
            if rows:
                return rows[-1]['Emotion']
    except FileNotFoundError:
        pass  # Handle the case when the file is not found
    return None

def recommend_music_genre_based_on_emotion(emotion):
    if emotion == 'angry':
        return 'rock'
    elif emotion == 'disgust':
        return 'heavy metal'
    elif emotion == 'scared':
        return 'rap'
    elif emotion == 'happy':
        return 'dance'
    elif emotion == 'sad':
        return 'blues'
    elif emotion == 'surprised':
        return 'dance'
    else:
        return 'unknown'

def get_song_recommendations(api_key, genre):
    url = f'http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={genre}&api_key={api_key}&format=json&limit=10'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', {}).get('track', [])
        return [(track['name'], track['artist']['name'], track['url']) for track in tracks]
    else:
        return []

def open_youtube(video_url):
    webbrowser.open(video_url)

def open_gui():
    root = tk.Tk()
    root.title("Music Recommendation Chatbot")
    root.geometry("600x500")  # Set the dimensions of the GUI

   

    last_emotion = read_last_emotion_from_csv('emotionsave.csv')

    if last_emotion:
        recommended_genre = recommend_music_genre_based_on_emotion(last_emotion)

        if recommended_genre != 'unknown':
            lastfm_api_key = '59cbd71b0011ebff0a3f88de8c96ef6e'  # Replace with your Last.fm API key
            song_recommendations = get_song_recommendations(lastfm_api_key, recommended_genre)

            if song_recommendations:
                tk.Label(root, text=f"Your last emotion was {last_emotion}.", font=("Helvetica", 14), bg="white").pack(pady=10)
                tk.Label(root, text=f"I recommend listening to these {recommended_genre} songs:", font=("Helvetica", 14), bg="white").pack(pady=10)

                for i, (song, artist, video_url) in enumerate(song_recommendations, 1):
                    song_label = tk.Label(root, text=f"{i}. {song} by {artist}", font=("Helvetica", 12), justify="left", fg="blue", cursor="hand2", bg="white")
                    song_label.pack(pady=5)
                    song_label.bind("<Button-1>", lambda event, url=video_url: open_youtube(url))  # type: ignore


            else:
                tk.Label(root, text="Sorry, I couldn't fetch song recommendations.", font=("Helvetica", 14), bg="white").pack(pady=10)
        else:
            tk.Label(root, text="I couldn't determine a genre based on your last emotion.", font=("Helvetica", 14), bg="white").pack(pady=10)
    else:
        tk.Label(root, text="No previous emotion found in the CSV file.", font=("Helvetica", 14), bg="white").pack(pady=10)

    root.mainloop()

    # Delete the CSV file after the GUI is closed
    try:
        os.remove('emotionsave.csv')
        print("CSV file deleted successfully.")
    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print(f"Error deleting CSV file: {e}")

if __name__ == "__main__":
    open_gui()

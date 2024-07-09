import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import tkinter as tk
import webbrowser
import os

# Hardcoded Spotify API credentials
SPOTIFY_CLIENT_ID = 'ad8d1d96c43247a78a4f2a5db3f8f4c8'
SPOTIFY_CLIENT_SECRET = 'f723420ce12f43cd8237e9353df04589'

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
    # Map emotions to Spotify genres (adjust as needed)
    genre_mapping = {
        'angry': 'rock',
        'disgust': 'heavy metal',
        'scared': 'rap',
        'happy': 'happy hits',
        'sad': 'sad bops',
        'surprised': 'dance',
    }
    return genre_mapping.get(emotion, 'unknown')

def get_song_recommendations(genre):
    auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.search(q=f'genre:{genre}', type='track', limit=15)
    
    tracks = results.get('tracks', {}).get('items', [])

    return [(track['name'], track['artists'][0]['name'], track['external_urls']['spotify']) for track in tracks]

def open_spotify(url):
    webbrowser.open(url)

def open_gui():
    root = tk.Tk()
    root.title("Music Recommendation Chatbot")
    root.geometry("600x700")  # Set the dimensions of the GUI

    last_emotion = read_last_emotion_from_csv('emotionsave.csv')

    if last_emotion:
        recommended_genre = recommend_music_genre_based_on_emotion(last_emotion)

        if recommended_genre != 'unknown':
            song_recommendations = get_song_recommendations(recommended_genre)

            if song_recommendations:
                tk.Label(root, text=f"Your last emotion was {last_emotion}.", font=("Helvetica", 14), bg="white").pack(pady=10)
                tk.Label(root, text=f"I recommend listening to these {recommended_genre} songs:", font=("Helvetica", 14), bg="white").pack(pady=10)

                for i, (song, artist, spotify_url) in enumerate(song_recommendations, 1):
                    song_label = tk.Label(root, text=f"{i}. {song} by {artist}", font=("Helvetica", 12), justify="left", fg="blue", cursor="hand2", bg="white")
                    song_label.pack(pady=5)
                    song_label.bind("<Button-1>", lambda event, url=spotify_url: open_spotify(url))

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

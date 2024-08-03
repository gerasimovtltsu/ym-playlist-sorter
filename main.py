from yandex_music import Client
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Токен доступа к яндекс музыке
TOKEN = os.getenv('TOKEN')

# Идентификаторы пользователя и плейлиста для получения треков
USER_ID = os.getenv('USER_ID') # здесь Ваш логин от яндекса
PLAYLIST_ID = os.getenv('PLAYLIST_ID') # ID плейлиста -> узнается в адресной строке при открытии плейлиста "мне нравится"

def main():
    print("Инициализация клиента Яндекс Музыки...")
    client = Client(TOKEN).init()

    # Получение плейлиста с треками
    print(f"Получение треков из плейлиста пользователя {USER_ID} с ID {PLAYLIST_ID}...")
    playlist = client.users_playlists(kind=PLAYLIST_ID, user_id=USER_ID)
    playlist.fetch_tracks()  # Синхронно загружаем треки в плейлист
    tracks = playlist.tracks

    # Словарь для сортировки треков по жанрам
    playlists_by_genre = {}

    # Обработка треков и распределение по жанрам
    total_tracks = len(tracks)
    print(f"Сортировка {total_tracks} треков по жанрам...")

    # Обработка каждого трека
    for i, track in enumerate(tracks, start=1):
        process_track(i, total_tracks, track, playlists_by_genre)

    # Создание нового плейлиста для каждого жанра и добавление треков
    created_playlists = []

    for genre, genre_tracks in playlists_by_genre.items():
        # Создание нового плейлиста
        print(f"\nСоздание нового плейлиста для жанра: {genre}...")
        new_playlist = client.users_playlists_create(title=f"{genre}", visibility='private')
        playlist_id = new_playlist.kind

        # Формирование списка треков для добавления
        tracks_to_add = [{'id': track.id, 'album_id': track.albums[0].id} for track in genre_tracks if track.albums]

        # Проверка на наличие треков с валидными идентификаторами альбомов
        if not tracks_to_add:
            print(f"Нет треков для добавления в плейлист '{genre}' (возможно, у некоторых треков отсутствует информация о альбоме).")
            continue

        # Добавление треков в новый плейлист
        for track in tracks_to_add:
            # Получение актуальной ревизии плейлиста перед каждым добавлением трека
            playlist_info = client.users_playlists(kind=playlist_id, user_id=USER_ID)
            current_revision = playlist_info.revision

            print(f"Добавление трека {track['id']} в плейлист '{genre}' с ревизией {current_revision}...")
            client.users_playlists_insert_track(
                kind=playlist_id,
                track_id=track['id'],
                album_id=track['album_id'],
                at=0,
                revision=current_revision,
                user_id=USER_ID
            )
        
        created_playlists.append(f"Плейлист '{genre}' создан с ID: {playlist_id}")

    # Вывод информации о созданных плейлистах
    print("\nСоздание плейлистов завершено. Информация о созданных плейлистах:")
    for info in created_playlists:
        print(info)

def process_track(i, total_tracks, track, playlists_by_genre):
    # Получение полной информации о треке
    track_data = track.fetch_track()
    artists = ', '.join(artist.name for artist in track_data.artists)
    title = track_data.title
    
    print(f"Обработка трека {i}/{total_tracks}: {artists} - {title}")
    
    # Получение жанра трека
    if track_data.albums and track_data.albums[0].genre:
        genre = track_data.albums[0].genre
    else:
        genre = 'Unknown'

    # Добавление трека в соответствующий плейлист по жанру
    if genre not in playlists_by_genre:
        playlists_by_genre[genre] = []
    playlists_by_genre[genre].append(track_data)

main()
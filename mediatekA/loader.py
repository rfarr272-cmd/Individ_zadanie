def load_tracks_from_file(filename):
    """Загрузка аудиозаписей из текстового файла"""
    tracks = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(';')
                    if len(parts) == 6:
                        track = {
                            'artist': parts[0].strip(),
                            'title': parts[1].strip(),
                            'album': parts[2].strip(),
                            'year': int(parts[3].strip()),
                            'duration': int(parts[4].strip()),
                            'plays': int(parts[5].strip())
                        }
                        tracks.append(track)
        print(f"Загружено {len(tracks)} записей из файла {filename}")
        return tracks
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден!")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return []


def save_tracks_to_file(filename, tracks):
    """Сохранение аудиозаписей в текстовый файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for track in tracks:
                line = f"{track['artist']};{track['title']};{track['album']};"
                line += f"{track['year']};{track['duration']};{track['plays']}\n"
                file.write(line)
        print(f"Сохранено {len(tracks)} записей в файл {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        return False


def display_track(track, index=None):
    """Отображение информации о треке с возможной нумерацией"""
    minutes = track['duration'] // 60
    seconds = track['duration'] % 60

    if index is not None:
        return (f"{index:3}. {track['artist']:25} | {track['title']:30} | "
                f"{track['album']:35} | {track['year']:4} | "
                f"{minutes:2}:{seconds:02d} | {track['plays']:>15,}")
    else:
        return (f"{track['artist']:25} | {track['title']:30} | "
                f"{track['album']:35} | {track['year']:4} | "
                f"{minutes:2}:{seconds:02d} | {track['plays']:>15,}")


def display_tracks_table(tracks, title=None, show_index=False):
    """Отображение списка треков в виде таблицы"""
    if title:
        print("\n" + "=" * 140)
        print(title.center(140))
        print("=" * 140)

    if not tracks:
        print("Записи не найдены")
        return

    if show_index:
        print(f"{'№':3} | {'Исполнитель':25} | {'Название трека':30} | {'Альбом':35} | "
              f"{'Год':4} | {'Длит.':6} | {'Прослушивания':>15}")
    else:
        print(f"{'Исполнитель':25} | {'Название трека':30} | {'Альбом':35} | "
              f"{'Год':4} | {'Длит.':6} | {'Прослушивания':>15}")

    print("-" * 140)

    for i, track in enumerate(tracks, 1):
        if show_index:
            print(display_track(track, i))
        else:
            print(display_track(track))

    print(f"\nВсего записей: {len(tracks)}")
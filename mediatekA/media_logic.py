def quicksort(tracks, key_func, descending=False):
    """Реализация сортировки Хоара"""
    if len(tracks) <= 1:
        return tracks.copy()

    pivot = tracks[len(tracks) // 2]
    pivot_key = key_func(pivot)

    left = []
    middle = []
    right = []

    for track in tracks:
        track_key = key_func(track)
        if descending:
            if track_key > pivot_key:
                left.append(track)
            elif track_key < pivot_key:
                right.append(track)
            else:
                middle.append(track)
        else:
            if track_key < pivot_key:
                left.append(track)
            elif track_key > pivot_key:
                right.append(track)
            else:
                middle.append(track)

    return quicksort(left, key_func, descending) + middle + quicksort(right, key_func, descending)


def sort_by_multiple_keys(tracks, sort_specs):
    """
    Сортировка по нескольким ключам
    sort_specs: список кортежей (ключ_функция, обратный_порядок)
    """
    if not tracks:
        return []

    sorted_tracks = tracks.copy()
    for key_func, reverse in reversed(sort_specs):
        sorted_tracks = quicksort(sorted_tracks, key_func, reverse)

    return sorted_tracks


# Функции для трех отчетов по заданию
def report_all_sorted(tracks):
    """
    Отчет 1: Список всех аудиозаписей, отсортированный по:
    исполнитель (по возрастанию) + год выпуска (по убыванию) +
    количество прослушиваний (по убыванию)
    """
    sort_specs = [
        (lambda x: x['plays'], True),  # по убыванию
        (lambda x: x['year'], True),  # по убыванию
        (lambda x: x['artist'].lower(), False)  # по возрастанию
    ]
    return sort_by_multiple_keys(tracks, sort_specs)


def report_by_artist(tracks, artist_name):
    """
    Отчет 2: Список всех аудиозаписей конкретного исполнителя,
    отсортированный по: альбом (по убыванию) + название трека (по возрастанию)
    """
    artist_tracks = [t for t in tracks if t['artist'].lower() == artist_name.lower()]

    sort_specs = [
        (lambda x: x['title'].lower(), False),  # по возрастанию
        (lambda x: x['album'].lower(), True)  # по убыванию
    ]

    return sort_by_multiple_keys(artist_tracks, sort_specs)


def report_by_year_range(tracks, start_year, end_year):
    """
    Отчет 3: Список всех аудиозаписей, выпущенных в период с N1 до N2 года,
    отсортированный по: год выпуска (по убыванию) + исполнитель (по возрастанию)
    """
    filtered_tracks = [t for t in tracks if start_year <= t['year'] <= end_year]

    sort_specs = [
        (lambda x: x['artist'].lower(), False),  # по возрастанию
        (lambda x: x['year'], True)  # по убыванию
    ]

    return sort_by_multiple_keys(filtered_tracks, sort_specs)
from loader import load_tracks_from_file, save_tracks_to_file, display_tracks_table
from media_logic import report_all_sorted, report_by_artist, report_by_year_range


def display_menu():
    """Отображение главного меню"""
    print("\n" + "=" * 60)
    print("МЕДИАТЕКА - Управление аудиозаписями".center(60))
    print("=" * 60)
    print("1. Показать исходные данные ")
    print("2. Отчет 1: Полный отсортированный список ")
    print("3. Отчет 2: Отсортирован по исполнителю")
    print("4. Отчет 3: Отсортирован по диапазону лет")
    print("5. Добавить новую аудиозапись")
    print("6. Удалить аудиозапись")
    print("7. Редактировать аудиозапись")
    print("8. Сохранить текущие данные в файл")
    print("9. Выход")
    print("-" * 60)
    return input("Выберите действие (1-9): ").strip()


def validate_track_data(artist, title, album, year, duration, plays):
    """Проверка корректности числовых данных"""
    errors = []

    # Проверка строковых полей
    if not artist or not artist.strip():
        errors.append("Исполнитель не может быть пустым")
    elif len(artist.strip()) < 1:
        errors.append("Исполнитель должен содержать минимум 1 символ")

    if not title or not title.strip():
        errors.append("Название трека не может быть пустым")
    elif len(title.strip()) < 1:
        errors.append("Название трека должно содержать минимум 1 символ")

    if not album or not album.strip():
        errors.append("Альбом не может быть пустым")
    elif len(album.strip()) < 1:
        errors.append("Альбом должен содержать минимум 1 символ")

    if year < 1900 or year > 2026:
        errors.append("Год должен быть в диапазоне 1900-2026")

    if duration <= 0:
        errors.append("Длительность должна быть положительным числом")
    elif duration > 3600:  # больше 1 часа
        errors.append("Длительность не должна превышать 3600 секунд (1 час)")

    if plays < 0:
        errors.append("Количество прослушиваний не может быть отрицательным")
    elif plays > 1000000000000:
        errors.append("Количество прослушиваний слишком велико")

    return errors


def add_new_track(tracks):
    """Добавление новой аудиозаписи"""
    print("\n" + "=" * 60)
    print("ДОБАВЛЕНИЕ НОВОЙ АУДИОЗАПИСИ".center(60))
    print("=" * 60)

    try:
        artist = input("Исполнитель: ").strip()
        title = input("Название трека: ").strip()
        album = input("Альбом: ").strip()

        # Ввод и проверка года
        year_input = input("Год выпуска (1900-2026): ").strip()
        if not year_input:
            print("Ошибка: год не может быть пустым!")
            return False
        year = int(year_input)

        # Ввод и проверка длительности
        duration_input = input("Длительность в секундах, (1-3600): ").strip()
        if not duration_input:
            print("Ошибка: длительность не может быть пустой!")
            return False
        duration = int(duration_input)

        # Ввод и проверка прослушиваний
        plays_input = input("Количество прослушиваний (0-1,000,000,000,000): ").strip()
        if not plays_input:
            print("Ошибка: количество прослушиваний не может быть пустым!")
            return False
        plays = int(plays_input)

        # Проверка на пустые строки и некорректные значения
        validation_errors = validate_track_data(artist, title, album, year, duration, plays)

        if validation_errors:
            print("\nОшибки в данных:")
            for error in validation_errors:
                print(f"  - {error}")
            return False

        new_track = {
            'artist': artist,
            'title': title,
            'album': album,
            'year': year,
            'duration': duration,
            'plays': plays
        }
        tracks.append(new_track)
        print(f"\nЗапись '{title}' исполнителя '{artist}' успешно добавлена!")
        return True

    except ValueError:
        print("Ошибка: некорректные числовые данные!")
        return False


def delete_track(tracks):
    """Удаление аудиозаписи"""
    if not tracks:
        print("Нет записей для удаления!")
        return False

    print("\n" + "=" * 60)
    print("УДАЛЕНИЕ АУДИОЗАПИСИ".center(60))
    print("=" * 60)

    # Показываем все записи с номерами
    display_tracks_table(tracks, "ТЕКУЩИЕ ЗАПИСИ", show_index=True)

    try:
        track_num = int(input("\nВведите номер записи для удаления: ").strip())

        if 1 <= track_num <= len(tracks):
            track_to_delete = tracks[track_num - 1]
            print(f"\nВы действительно хотите удалить запись:")
            print(f"Исполнитель: {track_to_delete['artist']}")
            print(f"Трек: {track_to_delete['title']}")
            print(f"Альбом: {track_to_delete['album']}")

            confirm = input("Подтвердите удаление (да/нет): ").strip().lower()

            if confirm in ['да', 'д', 'yes', 'y']:
                deleted_track = tracks.pop(track_num - 1)
                print(f"Запись '{deleted_track['title']}' удалена успешно!")
                return True
            else:
                print("Удаление отменено.")
                return False
        else:
            print(f"Ошибка: номер должен быть от 1 до {len(tracks)}")
            return False
    except ValueError:
        print("Ошибка: введите корректный номер!")
        return False


def edit_track(tracks):
    """Редактирование аудиозаписи"""
    print("\n" + "=" * 60)
    print("РЕДАКТИРОВАНИЕ АУДИОЗАПИСИ".center(60))
    print("=" * 60)

    # Показываем все записи с номерами
    display_tracks_table(tracks, "ТЕКУЩИЕ ЗАПИСИ", show_index=True)

    if not tracks:
        print("Нет записей для редактирования!")
        return tracks

    try:
        track_num = int(input("\nВведите номер записи для редактирования: ").strip())

        if 1 <= track_num <= len(tracks):
            track = tracks[track_num - 1]

            print(f"\nРедактирование записи:")
            print(f"1. {track['artist']} - {track['title']}")
            print(f"2. Альбом: {track['album']}")
            print(f"3. Год выпуска: {track['year']}")
            print(f"4. Длительность: {track['duration']} сек ({track['duration'] // 60}:{track['duration'] % 60:02d})")
            print(f"5. Прослушивания: {track['plays']:,}")
            print("-" * 60)

            print("Что изменить?")
            print("1. Исполнитель")
            print("2. Название трека")
            print("3. Альбом")
            print("4. Год выпуска")
            print("5. Длительность")
            print("6. Количество прослушиваний")
            print("7. Все поля")
            print("0. Отмена")

            choice = input("Ваш выбор (0-7): ").strip()

            if choice == '0':
                print("Редактирование отменено.")
                return tracks

            elif choice == '1':
                # Изменение исполнителя
                new_artist = input("Новый исполнитель: ").strip()
                if not new_artist:
                    print("Ошибка: исполнитель не может быть пустым!")
                    return tracks
                elif len(new_artist) < 1:
                    print("Ошибка: исполнитель должен содержать минимум 1 символа")
                    return tracks
                track['artist'] = new_artist
                print("Исполнитель изменен!")

            elif choice == '2':
                # Изменение названия трека
                new_title = input("Новое название трека: ").strip()
                if not new_title:
                    print("Ошибка: название трека не может быть пустым!")
                    return tracks
                elif len(new_title) < 1:
                    print("Ошибка: название трека должно содержать минимум 1 символ")
                    return tracks
                track['title'] = new_title
                print("Название трека изменено!")

            elif choice == '3':
                # Изменение альбома
                new_album = input("Новый альбом: ").strip()
                if not new_album:
                    print("Ошибка: альбом не может быть пустым!")
                    return tracks
                elif len(new_album) < 1:
                    print("Ошибка: альбом должен содержать минимум 1 символ")
                    return tracks
                track['album'] = new_album
                print("Альбом изменен!")

            elif choice == '4':
                # Изменение года выпуска
                try:
                    new_year_input = input("Новый год выпуска (1900-2026): ").strip()
                    if not new_year_input:
                        print("Ошибка: год не может быть пустым!")
                        return tracks
                    new_year = int(new_year_input)
                    if 1900 <= new_year <= 2026:
                        track['year'] = new_year
                        print("Год выпуска изменен!")
                    else:
                        print("Ошибка: год должен быть в диапазоне 1900-2026")
                except ValueError:
                    print("Ошибка: введите корректный год!")

            elif choice == '5':
                # Изменение длительности
                try:
                    new_duration_input = input("Новая длительность (в секундах, 1-3600): ").strip()
                    if not new_duration_input:
                        print("Ошибка: длительность не может быть пустой!")
                        return tracks
                    new_duration = int(new_duration_input)
                    if 1 <= new_duration <= 3600:
                        track['duration'] = new_duration
                        print("Длительность изменена!")
                    else:
                        print("Ошибка: длительность должна быть в диапазоне 1-3600 секунд")
                except ValueError:
                    print("Ошибка: введите корректную длительность!")

            elif choice == '6':
                # Изменение количества прослушиваний
                try:
                    new_plays_input = input("Новое количество прослушиваний (0-1,000,000,000,000): ").strip()
                    if not new_plays_input:
                        print("Ошибка: количество прослушиваний не может быть пустым!")
                        return tracks
                    new_plays = int(new_plays_input)
                    if 0 <= new_plays <= 1000000000000:
                        track['plays'] = new_plays
                        print("Количество прослушиваний изменено!")
                    else:
                        print("Ошибка: количество прослушиваний должно быть в диапазоне 0-1,000,000,000,000")
                except ValueError:
                    print("Ошибка: введите корректное число!")

            elif choice == '7':
                # Изменение всех полей
                print("\nРедактирование всех полей:")

                new_artist = input("Исполнитель: ").strip()
                new_title = input("Название трека: ").strip()
                new_album = input("Альбом: ").strip()

                try:
                    new_year_input = input("Год выпуска: ").strip()
                    new_duration_input = input("Длительность в секундах: ").strip()
                    new_plays_input = input("Количество прослушиваний: ").strip()

                    # Проверка на пустые числовые поля
                    if not new_year_input or not new_duration_input or not new_plays_input:
                        print("Ошибка: все числовые поля обязательны!")
                        return tracks

                    new_year = int(new_year_input)
                    new_duration = int(new_duration_input)
                    new_plays = int(new_plays_input)

                    # Проверка всех полей
                    validation_errors = validate_track_data(new_artist, new_title, new_album, new_year, new_duration,
                                                            new_plays)

                    if not validation_errors:
                        track['artist'] = new_artist
                        track['title'] = new_title
                        track['album'] = new_album
                        track['year'] = new_year
                        track['duration'] = new_duration
                        track['plays'] = new_plays
                        print("\nВсе поля изменены успешно!")
                    else:
                        print("\nОшибки в данных:")
                        for error in validation_errors:
                            print(f"  - {error}")
                        print("Изменения не сохранены!")

                except ValueError:
                    print("Ошибка: некорректные числовые данные!")

            else:
                print("Неверный выбор!")
                return tracks

            # Показываем обновленную запись
            print("\n" + "-" * 60)
            print("ОБНОВЛЕННАЯ ЗАПИСЬ:".center(60))
            print("-" * 60)
            minutes = track['duration'] // 60
            seconds = track['duration'] % 60
            print(f"Исполнитель: {track['artist']}")
            print(f"Трек: {track['title']}")
            print(f"Альбом: {track['album']}")
            print(f"Год: {track['year']}")
            print(f"Длительность: {minutes}:{seconds:02d}")
            print(f"Прослушивания: {track['plays']:,}")

            return tracks

        else:
            print(f"Ошибка: номер должен быть от 1 до {len(tracks)}")
            return tracks

    except ValueError:
        print("Ошибка: введите корректный номер!")
        return tracks

def main():
    # Загрузка исходных данных
    tracks = load_tracks_from_file("tracks_data.txt")

    if not tracks:
        print("Невозможно загрузить данные! Проверьте файл tracks_data.txt")
        return

    while True:
        choice = display_menu()

        if choice == "1":
            # Показать исходные данные без сортировки
            display_tracks_table(tracks, "ИСХОДНЫЕ ДАННЫЕ ", show_index=True)

        elif choice == "2":
            # Отчет 1
            sorted_tracks = report_all_sorted(tracks)
            display_tracks_table(sorted_tracks, "ОТЧЕТ 1: Полный отсортированный список  ",
                                 show_index=True)

        elif choice == "3":
            # Отчет 2
            artist = input("Введите имя исполнителя для отчета: ").strip()
            if artist:
                sorted_tracks = report_by_artist(tracks, artist)
                if sorted_tracks:
                    display_tracks_table(sorted_tracks,
                                         f"ОТЧЕТ 2: {artist.upper()} ",
                                         show_index=True)
                else:
                    print(f"Исполнитель '{artist}' не найден в медиатеке!")
            else:
                print("Исполнитель не указан!")

        elif choice == "4":
            # Отчет 3
            try:
                print("\nВведите диапазон лет для отчета:")
                start_year = int(input("Начальный год: ").strip())
                end_year = int(input("Конечный год: ").strip())

                if start_year > end_year:
                    start_year, end_year = end_year, start_year
                    print(f"Диапазон автоматически изменен на {start_year}-{end_year}")

                sorted_tracks = report_by_year_range(tracks, start_year, end_year)
                if sorted_tracks:
                    display_tracks_table(sorted_tracks,
                                         f"ОТЧЕТ 3: Годы {start_year}-{end_year} ",
                                         show_index=True)
                else:
                    print(f"В диапазоне {start_year}-{end_year} записей не найдено!")

            except ValueError:
                print("Ошибка: введите корректные года!")

        elif choice == "5":
            # Добавление новой записи
            if add_new_track(tracks):
                # Показываем обновленный список
                display_tracks_table(tracks, "ОБНОВЛЕННЫЙ СПИСОК", show_index=True)

        elif choice == "6":
            # Удаление записи
            if delete_track(tracks):
                # Показываем обновленный список
                display_tracks_table(tracks, "ОБНОВЛЕННЫЙ СПИСОК ПОСЛЕ УДАЛЕНИЯ", show_index=True)

        elif choice == "7":
            # Редактирование записи
            tracks = edit_track(tracks)
            # Показываем обновленный список
            display_tracks_table(tracks, "ОБНОВЛЕННЫЙ СПИСОК", show_index=True)

        elif choice == "8":
            # Сохранение данных
            if save_tracks_to_file("tracks_data.txt", tracks):
                print("Данные успешно сохранены!")

        elif choice == "9":
            # Выход с сохранением и проверкой ввода
            while True:  # Цикл для повторного запроса при некорректном вводе
                save_choice = input("\nСохранить изменения перед выходом? (да/нет): ").strip().lower()

                if save_choice in ['да', 'д', 'yes', 'y']:
                    if save_tracks_to_file("tracks_data.txt", tracks):
                        print("Изменения сохранены.")
                    break  # Выход из цикла проверки

                elif save_choice in ['нет', 'н', 'no', 'n']:
                    print("Изменения не сохранены.")
                    break  # Выход из цикла проверки

                else:
                    print("Ошибка: введите 'да' или 'нет'!")
                    print("Допустимые варианты: да, д, yes, y, нет, н, no, n")

            print("\n" + "=" * 60)
            print("Спасибо за использование Медиатеки!".center(60))
            print("=" * 60)
            break

        else:
            print("Неверный выбор! Пожалуйста, выберите действие от 1 до 9.")

        # Пауза перед следующим шагом
        if choice != "9":
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
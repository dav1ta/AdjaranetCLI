#!/usr/bin/env python
from settings import Settings
import sys
from adjara import *


def main():
    s = Settings()
    s.check_if_settings_exists('history.json')
    settings = s.read_json_file('history.json')
    s.update_data(settings)
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

    if "-n" in opts:

        if s.get_last_info('episodeCount') + 1 > s.get_last_info('episode'):
            s.update_last_info('season', s.get_last_info('season') + 1)
            s.update_last_info('episode', 1)
            choose_film(s.get_last_info('movie_id'), s.get_last_info('season'), s, autoChoose=True)

        else:
            choose_film(s.get_last_info('movie_id'), s.get_last_info('season'), s)

    elif "-p" in opts:
        if s.get_last_info('episode') == 1:
            s.update_last_info('season', s.get_last_info('season') - 1)
            s.update_last_info('episode', 1)
            choose_film(s.get_last_info('movie_id'), s.get_last_info('season'), s, autoChoose=True)

    elif "-h" in opts:
        print("-n Next episode\n-p Previous episode \n-h help \n")
    else:
        film_name = " ".join([ x for x in sys.argv[1:] if not x.startswith("-")]) if len(sys.argv[1:]) > 1 else input('ფილმის სახელი: ')
        movies_json = search_film(film_name)
        s.update_last_info('name', film_name)
        selected_film = int(input('აირჩიეთ ფილმის ნომერი: ')) - 1
        if movies_json:
            film_id = check_film_seasons(movies_json, selected_film, s)
            s.update_last_info('movie_id', film_id)
            if film_id:
                selected_season = int(input('აირჩიენ სეზონი: '))
                choose_film(film_id, selected_season, s)


if __name__ == "__main__":
    main()

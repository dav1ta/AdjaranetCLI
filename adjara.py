import requests
import subprocess


def safe_request_json(url):
    try:
        return requests.get(url).json()
    except Exception as e:
        print('კავშირის პრობლემა')
        exit(0)
       
def play_video(source_url):
    subprocess.Popen(f"mpv {source_url} >>/dev/null &", shell=True)


def search_film(keyword):
    adjaranet_api_uri = f"https://api.adjaranet.com/api/v1/search-advanced?movie_filters%5Bwith_actors%5D=3&movie_filters%5Bwith_directors%5D=1&movie_filters%5Bkeyword=&movie_filters%5Byear_range%5D=1900%2C2019&movie_filters%5Binit%5D=true&filters%5Btype%5D=movie&keywords={keyword}&page=1&per_page=15&source=adjaranet"
    searched_films_json = safe_request_json(adjaranet_api_uri)['data'] if safe_request_json(adjaranet_api_uri) else False
    if searched_films_json:
    	print('\n'.join([
                        f"{searched_films_json.index(movie) + 1}) {movie['primaryName']} - {movie['secondaryName']}  - {movie['year']} - {movie['rating']['imdb']['score']}"
                        for movie in searched_films_json]))
    return searched_films_json

def check_film_seasons(data, selected_id, settings):
    film_id = data[selected_id]['id']
    selected_film_uri = f"https://api.adjaranet.com/api/v1/movies/{film_id}"
    selected_film_info = safe_request_json(selected_film_uri)
    if selected_film_info:
        season_info = selected_film_info['data']['seasons']['data']
        if len(season_info) == 1 and season_info[0]['number'] == 0:
            choose_film(film_id, 0, settings)
            return False
        else:
            print('\n'.join([f"{season_info.index(season) + 1}){season['name']}" for season in season_info]))
    return film_id

def choose_film(film_id, selected_season_id, settings, autoChoose=False):
    season_files_uri = f"https://api.adjaranet.com/api/v1/movies/{film_id}/season-files/{selected_season_id}?source=adjaranet"
    season_files_json = safe_request_json(season_files_uri)["data"]
    if autoChoose:
        languages = season_files_json[settings.get_last_info('episode')]['files']
    else:
        if selected_season_id != 0:
            print('\n'.join([f"{episode['episode']}){episode['title']}" for episode in season_files_json]))
            selected_episode = int(input('აირჩიეთ ნომერი: ')) - 1
            languages = season_files_json[selected_episode]['files']
            settings.update_last_info('season', selected_season_id)
            settings.update_last_info('episode', selected_episode + 1)
            settings.update_last_info('episodeCount', season_files_json[-1]['episode'])
        else:
            languages = season_files_json[0]['files']
            settings.update_last_info('season', 0)
            settings.update_last_info('episode', 0)
    if settings.get_info('enablePreferedLanguage'):
        try:
            selected_language_id = next((languages.index(item) for item in languages if
                                         item["lang"] == settings.get_info('preferedLanguage')[0]), next(
                languages.index(item) for item in languages if
                item["lang"] == settings.get_info('preferedLanguage')[1]))
        except Exception:
            print('ენები ვერ მოინახა,ხელმისაწვდომი ენებია: ')
            print('\n'.join([f"{languages.index(language) + 1} {language['lang']}" for language in languages]))
            selected_language_id = int(input('აირჩიეთ ენა: ')) - 1
            settings.update_last_info('language', selected_language_id)
    else:
        print('\n'.join([f"{languages.index(language) + 1} {language['lang']}" for language in languages]))
        selected_language_id = int(input('აირჩიეთ ენა: ')) - 1
        settings.update_last_info('language', selected_language_id)
    settings.write_setting_in_file('history.json', settings.data)
    file_source_list = languages[selected_language_id]['files']
    possible_high_quality_link = next((item for item in file_source_list if item["quality"] == "HIGH"),
                                      next(item for item in file_source_list if item["quality"] == "MEDIUM"))['src']
    play_video(possible_high_quality_link)

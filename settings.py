import json


class Settings:
    data = {
        'preferedLanguage': ['GEO', 'ENG'],
        'enablePreferedLanguage': False,
        'lastPlayedMovie': {'movie_id': '', 'season': 0, 'episode': 0, 'language': '', 'episodeCount': 0},
        'preferedQuality': ['HIGH', 'MEDIUM'],
        'enablePreferedQuality': True, }

    @staticmethod
    def write_setting_in_file(filename, json_obj):
        with open(filename, 'w') as outfile:
            json.dump(json_obj, outfile)

    @staticmethod
    def read_json_file(filename):
        with open(filename) as json_file:
            try:
                data = json.load(json_file)
            except:
                data = {}
            return data

    @staticmethod
    def if_setting_not_exists(atr, json_data):
        if atr not in json_data:
            return True
        return False

    def check_if_settings_exists(self, filename):
        try:
            json_data = self.read_json_file(filename)
            if not json_data or self.if_setting_not_exists('preferedLanguage', json_data) or self.if_setting_not_exists(
                    'enablePreferedLanguage', json_data) or \
                    self.if_setting_not_exists('lastPlayedMovie', json_data) or self.if_setting_not_exists(
                'preferedQuality', json_data) or self.if_setting_not_exists('enablePreferedQuality', json_data):
                print('missing parameters...restoring default')
                self.write_setting_in_file(filename, self.data)


        except FileNotFoundError as e:
            print('settings not found...creating default')
            self.write_setting_in_file(filename, self.data)

    def update_last_info(self, key, value):
        self.data['lastPlayedMovie'][key] = value

    def update_data(self, data):
        self.data = data

    def get_last_info(self, key):
        return self.data['lastPlayedMovie'][key]

    def get_info(self, key):
        return self.data[key]

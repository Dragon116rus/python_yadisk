import requests
import json


class Yadisk:
    def __init__(self, auth=True):
        self.session = requests.Session()
        self.application_id = "c5bd227fe9384e74bf7693e5bc933cfd"
        if auth:
            self.create_oauth_token()

    def create_oauth_token(self, ouath_token = None):
        if ouath_token is None:
            self.oauth_token = self.get_oauth_token()
        else:
            self.oauth_token = ouath_token
        self.session.headers['Authorization'] = self.oauth_token

    def get_download_url(self, file_name, dir_url=None):
        if dir_url is None:
            url = "https://cloud-api.yandex.net/v1/disk/resources/download?path=/{}".format(
                file_name)
        else:
            url = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}&path=/{}".format(
                dir_url, file_name)
        response = self.session.get(url)
        return json.loads(response.text)['href']

    def download_by_url(self, url, file_name):
        get_response = requests.get(url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in get_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    def download(self, file_name, dir_url=None, file_name_to_save=None):
        if file_name_to_save is None:
            file_name_to_save = file_name
        download_url = self.get_download_url(file_name, dir_url)
        self.download_by_url(download_url, file_name_to_save)

    def get_upload_url(self, path_to_save, overwrite=True):
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload?path={}&overwrite={}".format(
            path_to_save, overwrite)
        response = self.session.get(url)
        return json.loads(response.text)['href']

    def upload_by_url(self, url, file_name):
        with open(file_name, "rb") as f:
            response = self.session.put(url, data=f)
            return response

    def upload(self, file_name, path_to_save=None, overwrite=True):
        if path_to_save is None:
            path_to_save = file_name
        upload_url = self.get_upload_url(path_to_save, overwrite=overwrite)
        return self.upload_by_url(upload_url, file_name)

    def get_oauth_code(self):
        print("https://oauth.yandex.ru/authorize?response_type=code&client_id={}".format(self.application_id))
        oauth_code = input()
        return oauth_code

    def get_oauth_token(self):
        # oauth_code = get_oauth_code()
        # return session.post("https://oauth.yandex.ru/token", data= {"grant_type" : "authorization_code",\
        #      "code" : oauth_code, \
        #      "client_id" : application_id})
        print("https://oauth.yandex.ru/authorize?response_type=token&client_id={}".format(self.application_id))
        oauth_token = input()
        return oauth_token

if __name__ == "__main__":
    disk = Yadisk()
    disk.download("main.py")

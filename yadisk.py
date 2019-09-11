import requests
import json


class Yadisk:
    """
    Api for downloading/uploading files from disk.yandex
    """
    def __init__(self, auth=True):
        """Class initialization
        
        Keyword Arguments:
            auth {bool} -- set oauth token with init (default: {True}),
            also you can set token with set_oauth_token method
        """
        self.session = requests.Session()
        self.application_id = "c5bd227fe9384e74bf7693e5bc933cfd"
        if auth:
            self.set_oauth_token()

    def set_oauth_token(self, oauth_token = None):
        """Setting oauth token
        
        Keyword Arguments:
            oauth_token {string} -- oauth_token (default: {None})
            if set None, then you need to go by link, and put token
            into script
        """
        if oauth_token is None:
            self.oauth_token = self._get_oauth_token()
        else:
            self.oauth_token = oauth_token
        self.session.headers['Authorization'] = self.oauth_token

    def _parse_response(self, response):
        data = response.content
        return json.loads(data)

    def _download(self, url, file_name):
        get_response = self.session.get(url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in get_response.iter_content(chunk_size=1024*16):
                if chunk:
                    f.write(chunk)

    def get_download_url_public(self, url, path=None):
        """Get url to dowlnoad data by shared link 
        
        Arguments:
            url {str} -- shared link to disk
            example: "https://yadi.sk/d/Tid5zLokLHb30g"
        
        Keyword Arguments:
            path {str} -- path to file in folder (default: {None})
            example: "main.py"
        """
        api_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
        payload = {'public_key': url}
        if path is not None:
            if path[0] != "/":
                path = "/" + path
            payload['path'] = path
        downloading_url_response = self.session.get(api_url, params=payload)
        downloading_url = self._parse_response(downloading_url_response)['href']
        return downloading_url

    def download_public(self, url, path=None, path_to_save="tmp"):
        """Download data by shared link 
        
        Arguments:
            url {str} -- shared link to disk
            example: "https://yadi.sk/d/Tid5zLokLHb30g"
        
        Keyword Arguments:
            path {str} -- path to file in folder (default: {None})
            example: "main.py"
            path_to_save {str} -- filename to save (default: {"tmp"})
        """
        downloading_url = self.get_download_url_public(url, path) 
        self._download(downloading_url, path_to_save)


    def _upload(self, url, file_name):
        with open(file_name, "rb") as f:
            response = self.session.put(url, data=f)
            return response

    def upload(self, file_name, path_to_save=None, overwrite=True):
        """Upload file to yandex.disk
        
        Arguments:
            file_name {str} -- file to upload
        
        Keyword Arguments:
            path_to_save {str} -- path (in ya.disk) to save (default: {None})
            overwrite {bool} -- overwrite file or not (default: {True})
        
        Returns:
            requests.Response -- response
        """
        if path_to_save is None:
            path_to_save = file_name
        api_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        payload = {"path": path_to_save,
                    "overwrite": overwrite}
        response = self.session.get(api_url, params=payload)
        upload_url = self._parse_response(response)['href']
        return self._upload(upload_url, file_name)

    def get_oauth_code(self):
        print("https://oauth.yandex.ru/authorize?response_type=code&client_id={}".format(self.application_id))
        oauth_code = input()
        return oauth_code

    def _get_oauth_token(self):
        print("https://oauth.yandex.ru/authorize?response_type=token&client_id={}".format(self.application_id))
        oauth_token = input()
        return oauth_token

    def list_item(self, path=None, limit=None):
        """Show items in dir

        Keyword Arguments:
            path {str} -- path to file in folder (default: {None})
            limit {int} -- number of items to return
        """
        api_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        payload = {
            # 'public_key': url,
                    'fields':'_embedded.items.path'
                    }
        if path is None:
            path = "/"
        if path[0] != "/":
            path = "/" + path
        payload['path'] = path
        if limit is not None:
            payload['limit'] = limit
        response = self.session.get(api_url, params=payload)
        items_json = json.loads(response.text)['_embedded']['items']

        items = []
        for item in items_json:
            items.append(item['path'])

        return items

    def mkdir(self, path):
        """Create dir with given path

            path {str} -- path to dir (default: {None})
        """
        api_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        payload = {}
        if path[0] != "/":
            path = "/" + path
        payload['path'] = path
        response = self.session.put(api_url, params=payload)
        return response

if __name__ == "__main__":
    disk = Yadisk(auth=True)
    print(disk.list_item("tmp"))
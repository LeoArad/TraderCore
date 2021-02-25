import requests
import configparser
import json

def get_config_parser(file_path='./custom.conf'):
    conf = configparser.ConfigParser()
    conf.read(file_path)
    return conf

conf = get_config_parser()
ip_address = conf.get("api", "ip_address")
port = conf.get("api", "port")
auth_uri= conf.get("api", "auth_uri")


class API_client:
    DEFAULT_HEADER = {
        'Content-Type': 'application/json'
    }

    def __init__(self, ip_address=ip_address, port=port, user=None, password=None):
        self.full_address = f"http://{ip_address}:{port}/"
        self.user = user
        self._password = password
        self.update_token()

    def update_token(self):
        self._access_token, self_refrsh_token = self.get_token()


    def _execute_post(self, uri: str, body: dict, headers=DEFAULT_HEADER):
        try:
            result = requests.post(f"{self.full_address}{uri}", headers=headers, data=json.dumps(body))
            if result.status_code == 401:
                self.update_token()
            return result
        except Exception:
            return None

    def _execute_get(self, uri: str, headers=DEFAULT_HEADER):
        try:
            result = requests.get(f"{self.full_address}{uri}", headers=headers)
            if result.status_code == 401:
                self.update_token()
            return result
        except Exception:
            return None

    def get_token(self):
        if all([self.user, self._password]):
            body = {"username": self.user, "password":self._password}
            res = self._execute_post("api/token/", body)

            if res and res.status_code == 200:
                res_obj = json.loads(res.text)
                self.DEFAULT_HEADER.update({'Authorization': f"Bearer {res_obj.get('access')}"})
                return res_obj.get("access"), res_obj.get("refresh")
            else:
                raise ValueError(f"There was an error geting user {self.user} make sure his exists")
            print(f"Couldn't Get token for user {self.user}")

    def create_user(self, email: str, password: str) -> bool:
        body = {"email": email, "password": password}
        res = self._execute_post("accounts/create/", body)
        return res.status_code == 201

    def create_post(self, title: str, content: str):
        body = {"title": title, "content": content}
        res = self._execute_post("posts/", body)
        return res.status_code == 201

    def get_next_user_id(self, max_likes):
        res = self._execute_get(f"next/user/{max_likes}")
        if res.status_code == 200:
            return json.loads(res.text).get("next_user_id"), json.loads(res.text).get("current_likes_count")
        return None, None

    def get_next_posts_ids(self, user_id):
        res = self._execute_get(f"next/posts/{user_id}")
        if res.status_code == 200:
            return json.loads(res.text).get("possible_posts_ids")
        if res.status_code == 404:
            return []
        return None


    def add_like(self, user_id, post_id):
        body = {"user": user_id, "post": post_id}
        res = self._execute_post("postslikes/", body)
        return res.status_code == 201


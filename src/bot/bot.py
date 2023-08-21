import yaml
import pathlib
import json
import requests
from random import randrange


basedir = pathlib.Path(__file__).parent.resolve()

class Bot(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Bot"

    base_user_name = "user"
    user_password = "12345"

    registred_users = []
    created_posts_by_id = []

    def __init__(self, users_info, base_url, headers, authorization, out_json):
        self.users_info = users_info
        self.base_url = base_url
        self.headers = headers
        self.authorization = authorization
        self.out_json = out_json

    def log_ok(self, msg: str) -> None:
        print("\033[92m [OK] \033[0m" + msg)

    def log_error(self, msg: str) -> None:
        print("\033[91m [ERR] \033[0m" + msg)

    def register_users(self) -> None:
        for i in range(self.users_info["number_of_users"]):
            user = { "username": f"{self.base_user_name}_{i}", "password": self.user_password }
            res = requests.post(self.base_url + "/auth/signup", headers=self.headers, data=json.dumps(user))

            if res.status_code == 201:
                self.log_ok(f"User {user} is successfully registred.")
                self.registred_users.append(user["username"])
            else:
                self.log_error(f"User registration for user {user} failed.\nServer respond with {res.status_code}.")

    def signin(self, username: str) -> bool:
        user = { "username": username, "password": self.user_password }
        res = requests.post(self.base_url + "/auth/signin", headers=self.headers, data=json.dumps(user))

        if res.status_code == 200:
            token = json.loads(res.content)["token"]
            self.headers["Authorization"] = self.authorization["type"] + " " + token
            return True
        else:
            self.log_error(f"Failed to signin user {user}.\nServer respond with {res.status_code}")
            return False


    def create_posts(self) -> None:
        for username in self.registred_users:
            if not self.signin(username):
                continue

            for i in range(randrange(1, self.users_info["max_posts_per_user"] + 1)):
                post = { "content": f"It's my {i} post!" }
                res = requests.post(self.base_url + "/posts", headers=self.headers, data=json.dumps(post))
                if res.status_code == 201:
                    self.log_ok(f"{username} posted {post} successfully.")
                    created_post = json.loads(res.content)
                    self.created_posts_by_id.append(created_post["id"])
                else:
                    self.log_error(f"{username} failed to publish post {post}.\nServer respond with {res.status_code}")

    def like_posts(self) -> None:
        number_of_posts = self.created_posts_by_id.__len__()

        if number_of_posts == 0:
            self.log_error("There is no posts to like.")
            return

        for username in self.registred_users:
            if not self.signin(username):
                continue

            for _ in range(randrange(self.users_info["min_likes_per_user"], self.users_info["max_likes_per_user"])):
                post_id = self.created_posts_by_id[randrange(0, number_of_posts)]
                res = requests.post(self.base_url + f"/posts/{post_id}/like", headers=self.headers)

                if res.status_code == 201:
                    self.log_ok(f"{username} liked post with id {post_id}.")
                elif res.status_code == 200:
                    self.log_ok(f"{username} unliked post with id {post_id}.")
                else:
                    self.log_error(f"{username} failed to like post with id {post_id}.\nServer respond with {res.status_code}")

    def dump_all_users_to_file(self) -> None:
        res = requests.get(self.base_url + "/users", headers=self.headers)

        if res.status_code != 200:
            self.log_error(f"Failed to get all users.\nServer respond with {res.status_code}")
            return

        with open(str(basedir) + "/" + self.out_json, "w") as f:
            f.write(res.text)

        self.log_ok(f"Dump of all users in the file {self.out_json}.")

    def run(self) -> None:
        print(f"Bot started with url {self.base_url}")
        self.register_users()
        self.create_posts()
        self.like_posts()
        self.dump_all_users_to_file()
        

def main():
    with open(str(basedir) + "/config.yml", "r") as stream:
        bot = yaml.safe_load(stream)
        bot.run()


if __name__ == "__main__":
    main()

import configparser
from api_client import get_config_parser, API_client
from random import randint, sample

conf = get_config_parser()

try:
    number_of_users = int(conf.get("automate_bot", "number_of_users"))
    max_likes_per_user = int(conf.get("automate_bot", "max_likes_per_user"))
    max_posts_per_user = int(conf.get("automate_bot", "max_posts_per_user"))
    DEFAULT_PASSWORD = conf.get("api", "default_pass")
    test_user = conf.get("api", "test_user")
except configparser.NoOptionError as e:
    print(f"The option {e.option} is not a valide option under section {e.section}")
except configparser.NoSectionError as e:
    print(f"The section {e.section} is not a valide section")

api_client = API_client(user=test_user, password=DEFAULT_PASSWORD)

def create_users_and_posts():
    print("In create_users_and_posts")
    for i in range(number_of_users):
        email = f"test{i + 1}@gmail.com"
        if api_client.create_user(email, DEFAULT_PASSWORD):
            api_client_inner_user = API_client(user=email, password=DEFAULT_PASSWORD)
            for y in range(randint(1, int(max_posts_per_user))):
                api_client_inner_user.create_post(f"Title number {(i + 1)  * (y + 1)}", f"Content number {(i + 1)  * (y + 1)}")
    print("Done with create_users_and_posts")


def run_users_likes_process():
    print("In run_users_likes_process method")
    next_user_id = True
    while next_user_id:
        next_user_id, current_likes_count = api_client.get_next_user_id(max_likes_per_user)
        if next_user_id:
            posible_posts_ids = api_client.get_next_posts_ids(next_user_id)
            if posible_posts_ids:
                num_of_likes = max_likes_per_user-current_likes_count
                for i in sample(posible_posts_ids, num_of_likes) if num_of_likes > len(posible_posts_ids) else posible_posts_ids:
                    api_client.add_like(next_user_id, i)
            elif isinstance(posible_posts_ids, list):
                next_user_id = False
                print("There are no posts that don't have likes")
    print("Done with run_users_likes_process method")


def main_process():
    create_users_and_posts()
    run_users_likes_process()


if __name__ == '__main__':
    main_process()


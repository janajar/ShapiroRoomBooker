import yaml
from users import create_db
from messager import check_email

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def main():
    create_db()
    email_account = load_config()
    check_email(email_account["username"], email_account["password"])

if __name__ == '__main__':
    main()

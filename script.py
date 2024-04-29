import yaml
from messager import check_email

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def main():
    email_account = load_config()
    check_email(email_account["username"], email_account["password"])
    pass

if __name__ == '__main__':
    main()

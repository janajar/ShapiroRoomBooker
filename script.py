from users import create_db
from messenger import check_email

def main():
    create_db()
    check_email()

if __name__ == '__main__':
    main()

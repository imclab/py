from mailsnake import MailSnake
from mailsnake.exceptions import EmailNotExistsException, ListNotSubscribedException
import json

def main():
    mailsnake = MailSnake("385108a2f086d0ede1a046291c92fc4f-us2")
    list_num = "e2f95e9547"
    for email in emails:
        try:
            returned = mailsnake.listUpdateMember(
                id=list_num,
                email_address=email,
                merge_vars={
                    'PURCHASED': True
                }
            )
            print "updated", email
        except EmailNotExistsException:
            print email, "isn't a subscriber"
            continue
        except ListNotSubscribedException:
            print email, "isn't a part of this list"
            continue


if __name__ == "__main__":
    main()
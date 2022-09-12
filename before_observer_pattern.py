
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Account:
    name: str
    email: str
    plan: int = 1


class AccountClient:
    
    def register_account(self, name, email):
        account = Account(name=name, email=email)
        print(f"Account created: {account}")
        print(f"Emailing {account.email} a verification code.")
        return account


    def upgrade_account(self, account: Account):
        account.plan = 2
        print(f"\nAccount upgraded: {account}")
        print(f"Emailing {account.email} their receipt.")
        print(f"Sending a Slack message to Accounting; {account.email} upgraded their account.")
        return account


def main():
    account_client = AccountClient()

    account = account_client.register_account('John Doe', "john.doe@foo.com")

    account_client.upgrade_account(account)


if __name__ == '__main__':
    main()

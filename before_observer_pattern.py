
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Account:
    name: str
    email: str
    plan: int = 1


class AccountClient:

    def configure_test_mode(self, enabled: bool):
        self.test_mode = enabled
    
    def register_account(self, name, email):
        account = Account(name=name, email=email)
        print(f"\nAccount created: {account}")

        if not self.test_mode:
            print(f"Emailing {account.email} a verification code.")
        
        return account

    def upgrade_account(self, account: Account):
        account.plan = 2
        print(f"\nAccount upgraded: {account}")

        if not self.test_mode:
            print(f"Emailing {account.email} their receipt.")
            print(f"Sending a Slack message to Accounting; {account.email} upgraded their account.")
        
        return account


def main():
    print("CREATE FIRST ACCOUNT...")
    account_client = AccountClient()
    account_client.configure_test_mode(False)
    account = account_client.register_account('John Doe', "john.doe@foo.com")
    account_client.upgrade_account(account)

    # Perhaps your user enters "test mode" in which no notifications should be sent
    # In this case, we can unsubscribe the listeners at runtime
    print("\n\nCREATE SECOND (TEST) ACCOUNT...")
    account_client.configure_test_mode(True)
    test_account = account_client.register_account('test', "testk@test.com")
    account_client.upgrade_account(test_account)


if __name__ == '__main__':
    main()

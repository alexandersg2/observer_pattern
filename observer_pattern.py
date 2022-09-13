
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Events:
    REGISTER = "register"
    UPGRADE = "upgrade"


@dataclass
class Account:
    name: str
    email: str
    plan: int = 1


class EventListener(ABC):
    @classmethod
    @abstractmethod
    def update(cls, data):
        ...


class CreatedVerificationEmailListener(EventListener):
    @classmethod
    def update(cls, account: Account):
        print(f"Emailing {account.email} a verification code.")


class UpgradedReceiptEmailListener(EventListener):
    @classmethod
    def update(cls, account: Account):
        print(f"Emailing {account.email} their receipt.")


class UpgradedAccountingSlackListener(EventListener):
    @classmethod
    def update(cls, account: Account):
        print(f"Sending a Slack message to Accounting; {account.email} upgraded their account.")


class EventManager:
    def __init__(self):
        self.listeners = {}
    
    def subscribe(self, event_type, listener: EventListener):
        self.listeners.setdefault(event_type, set())
        if listener not in self.listeners:
            self.listeners[event_type].add(listener)
            print(f"{listener} subscribed to {event_type}")
    
    def unsubscribe(self, event_type, listener: EventListener):
        if event_type in self.listeners:
            self.listeners[event_type].discard(listener)
            print(f"{listener} unsubscribed from {event_type}")
    
    def notify(self, event_type, data):
        for listener in self.listeners.get(event_type, set()):
            print(f"Notifying {listener}")
            listener.update(data)


class AccountClient:
    def __init__(self) -> None:
        self.event_manager = EventManager()
        self.configure_test_mode(False)
    
    def configure_test_mode(self, enabled):
        if not enabled:
            self.event_manager.subscribe(Events.REGISTER, CreatedVerificationEmailListener)
            self.event_manager.subscribe(Events.UPGRADE, UpgradedReceiptEmailListener)
            self.event_manager.subscribe(Events.UPGRADE, UpgradedAccountingSlackListener)
        else:
            print("\nEntering Testing mode...")
            self.event_manager.unsubscribe(Events.REGISTER, CreatedVerificationEmailListener)
            self.event_manager.unsubscribe(Events.UPGRADE, UpgradedReceiptEmailListener)
            self.event_manager.unsubscribe(Events.UPGRADE, UpgradedAccountingSlackListener)
    
    def register_account(self, name, email):
        account = Account(name=name, email=email)
        print(f"\nAccount created: {account}")
        self.event_manager.notify(Events.REGISTER, account)
        return account

    def upgrade_account(self, account: Account):
        account.plan = 2
        print(f"\nAccount upgraded: {account}")
        self.event_manager.notify(Events.UPGRADE, account)
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

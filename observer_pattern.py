
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
        for listener in self.listeners.get(event_type, []):
            print(f"Notifying {listener}")
            listener.update(data)


class AccountClient:
    def __init__(self, event_manager: EventManager) -> None:
        self.event_manager = event_manager
    
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
    event_manager = EventManager()
    event_manager.subscribe(Events.REGISTER, CreatedVerificationEmailListener)
    event_manager.subscribe(Events.UPGRADE, UpgradedReceiptEmailListener)
    event_manager.subscribe(Events.UPGRADE, UpgradedAccountingSlackListener)

    account_client = AccountClient(event_manager)
    account = account_client.register_account('John Doe', "john.doe@foo.com")
    account_client.upgrade_account(account)

    # Perhaps your user enters "test mode" in which no notifications should be sent
    # In this case, we can unsubscribe the listeners at runtime
    print("\nEntering Testing mode...")
    event_manager.unsubscribe(Events.REGISTER, CreatedVerificationEmailListener)
    event_manager.unsubscribe(Events.UPGRADE, UpgradedReceiptEmailListener)
    event_manager.unsubscribe(Events.UPGRADE, UpgradedAccountingSlackListener)

    account_client = AccountClient(event_manager)
    account = account_client.register_account('Tim Cook', "tim.cook@bar.com")
    account_client.upgrade_account(account)


if __name__ == '__main__':
    main()

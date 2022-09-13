from abc import ABC, abstractmethod
from dataclasses import dataclass


class EventType:
    UPDATE = "update"
    CLOSE = 'close'


@dataclass
class Document:
    name: str
    content: str = ""
    is_open: bool = True


class EventListener(ABC):
    @classmethod
    @abstractmethod
    def update(cls, data):
        ...


class SpellCheckerListener(EventListener):
    @classmethod
    def update(cls, document: Document):
        print(f"spell-checked {document.name}")


class BackupListener(EventListener):
    @classmethod
    def update(cls, document: Document):
        print(f"Backed up [{document.name}] to Google Drive")


class EventManager:
    def __init__(self) -> None:
        self.listeners = {}
    
    def subscribe(self, event_type: EventType, listener: EventListener):
        self.listeners.setdefault(event_type, set())
        if event_type not in self.listeners[event_type]:
            self.listeners[event_type].add(listener)
            print(f"{listener} subscribed to {event_type}")
            
    
    def unsubscribe(self, event_type: EventType, listener: EventListener):
        if event_type in self.listeners:
            self.listeners[event_type].discard(listener)
            print(f"{listener} unsubscribed from {event_type}")
    
    def notify(self, event_type: EventType, data):
        for listener in self.listeners.get(event_type, set()):
            print(f"Notifying {listener}")
            listener.update(data)


class WordProcessor:
    """This is a handy word processor that can spell check and back up documents to Google Drive."""

    def __init__(self):
        self.event_manager = EventManager()
    
    def configure_spell_checker(self, enabled: bool):
        if enabled:
            self.event_manager.subscribe(EventType.UPDATE, SpellCheckerListener)
        else:
            self.event_manager.unsubscribe(EventType.UPDATE, SpellCheckerListener)
    
    def configure_auto_backup(self, enabled: bool):
        if enabled:
            self.event_manager.subscribe(EventType.CLOSE, BackupListener)
        else:
            self.event_manager.unsubscribe(EventType.CLOSE, BackupListener)

    def create_document(self, name: str):
        document =  Document(name=name)
        print(f"\nCreated document: {document.name}")
        return document
    
    def close_document(self, document: Document):
        # Close document
        document.is_open = False
        print(f"\nClosed {document.name}")
        
        self.event_manager.notify(EventType.CLOSE, document)

        return document

    def add_text(self, document: Document, text: str):
        # Add the new text
        document.content += text
        print(f"\nDocument now reads: {document.content}")
        
        self.event_manager.notify(EventType.UPDATE, document)

        return document


def main():
    print("FIRST DOCUMENT...")
    
    # Create a word processor
    word_processor = WordProcessor()

    # Enable auto backup and spell checking
    word_processor.configure_auto_backup(True)
    word_processor.configure_spell_checker(True)

    # Create, update, and close a document
    document = word_processor.create_document(name="foo.txt")

    word_processor.add_text(document, "bar")
    word_processor.add_text(document, " baz")

    word_processor.close_document(document)

    print("\n\nSECOND DOCUMENT...")

    # Disable spell checking
    word_processor.configure_spell_checker(False)

    # Create, update, and close a second document
    second_doc = word_processor.create_document(name="foo.txt")

    word_processor.add_text(second_doc, "bar")
    word_processor.add_text(second_doc, " baz")

    word_processor.close_document(second_doc)


if __name__ == '__main__':
    main()

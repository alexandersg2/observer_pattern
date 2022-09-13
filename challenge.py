from dataclasses import dataclass


@dataclass
class Document:
    name: str
    content: str = ""
    is_open: bool = True


class WordProcessor:
    """This is a handy word processor that can spell check and back up documents to Google Drive."""
    
    def configure_spell_checker(self, enabled: bool):
        self.spell_check = enabled
    
    def configure_auto_backup(self, enabled: bool):
        self.auto_backup = enabled

    def create_document(self, name: str):
        document =  Document(name=name)
        print(f"\nCreated document: {document}")
        return document
    
    def close_document(self, document: Document):
        # Close document
        document.is_open = False
        print(f"\nClosed {document.name}")

        if self.auto_backup:
            # Backup the document automatically
            print(f"Backed up [{document.name}] to Google Drive")
        
        return document

    def add_text(self, document: Document, text: str):
        # Add the new text
        document.content += text
        print(f"\nDocument now reads: {document.content}")

        if self.spell_check:
            # Spellcheck the document
            print(f"spell-checked {document.name}")
        
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

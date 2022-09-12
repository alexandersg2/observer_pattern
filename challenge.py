from dataclasses import dataclass


@dataclass
class Document:
    name: str
    content: str = ""
    is_saved: bool = False
    is_open: bool = True


class WordProcessor:

    def create_document(self, name: str):
        document =  Document(name=name)
        print(f"Created document: {document.name}")
        return document
    
    def spellcheck(self, document: Document):
        print(f"spellchecked {document.name}")
        return document
    
    def close_document(self, document: Document):
        # Close document
        document.is_open = False
        print(f"Closed {document.name}")

        # Autosave the document
        document.is_saved = True
        print(f"Saved {document.name}")
        return document

    def add_text(self, document: Document, text: str):
        # Add the new text
        document.content += text
        print(f"Document now reads: {document.content}")

        # Spellcheck the document
        print(f"spellchecked {document.name}")
        return document


def main():
    word_processor = WordProcessor()
    document = word_processor.create_document("foo.txt")

    document = word_processor.add_text(document, "foo")
    document = word_processor.add_text(document, " bar")
    document = word_processor.add_text(document, " baz")

    document = word_processor.close_document(document)


if __name__ == '__main__':
    main()

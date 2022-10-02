from typing import IO, List


class WordParser():
    def __init__(self, file_words: IO):
        self.file = file_words.read()

    def process(self) -> List[str]:
        return str(self.file).split("\n")
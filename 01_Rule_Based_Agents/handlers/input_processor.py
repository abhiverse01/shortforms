import re

class InputProcessor:
    def __init__(self):
        self._compiled_patterns = [
            (re.compile(r'\b' + re.escape(word) + r'\b'), replacement)
            for word, replacement in [
                ("don't", "do not"),
                ("can't", "cannot"),
                ("won't", "will not")
            ]
        ]

    def normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = self._expand_contractions(text)
        text = re.sub(r'[^\w\s?]', '', text)
        return text

    def _expand_contractions(self, text: str) -> str:
        for pattern, replacement in self._compiled_patterns:
            text = pattern.sub(replacement, text)
        return text
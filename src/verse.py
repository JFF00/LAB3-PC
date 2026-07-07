class Verse:
    def __init__(self, id, content):
        self.id = id
        self.content = content
        self.tokens = []
        self.frequencies = {}  # {"palabra":conteo(int)}

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content

    def set_tokens(self, tokens):
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def get_frequencies(self):
        return self.frequencies

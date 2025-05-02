import wolframalpha

class KnowledgeEngine:
    def __init__(self, api_key):
        self.client = wolframalpha.Client(api_key)

    def query(self, question: str):
        res = self.client.query(question)
        try:
            return next(res.results).text
        except:
            return "I found some information but couldn't parse it properly."
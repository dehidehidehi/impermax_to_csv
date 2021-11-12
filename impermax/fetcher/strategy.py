from impermax.fetcher.enums import DataProvenances


class DataFetcher:

    def __init__(self, fetcher: DataProvenances):
        self.fetcher = fetcher.value()

    def get(self, urls: list[str]):
        return self.fetcher.get(urls)

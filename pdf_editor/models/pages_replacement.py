from dataclasses import dataclass


@dataclass
class PagesReplacement:
    path: str
    pages: list[int]

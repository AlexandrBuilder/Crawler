import re
from typing import Iterable, List, Set, Tuple

from bs4 import BeautifulSoup


class PageParserHelper:

    def __init__(self, content: str, link_text: str) -> None:
        self.content = content
        self.link_text = link_text
        self._soup = BeautifulSoup(self.content, 'html.parser')
        self.names = {'Маша', 'Саша', 'Дима', 'Жора', 'Андрей', 'Вика', 'Ира', 'Игорь', 'Степа', 'Кеша', 'Гена'}

    def get_new_urls(self) -> Iterable[Tuple[str, str]]:
        for link in self._soup.find_all('a', href=True):
            url = link['href']
            yield url, link.text

    @staticmethod
    def prepare_text(content: str) -> str:
        content = content.replace('\n', '')
        content = re.sub(r'\s{2,}', ' ', content)
        return content

    def get_title(self) -> str:
        paragraph_tag_h1 = self._soup.find('h1')
        title = self.prepare_text(paragraph_tag_h1.text) if paragraph_tag_h1 else ''
        return title

    def get_content(self) -> str:
        paragraph_tag_collection = self._soup.findAll('p')
        paragraph_content = [self.prepare_text(paragraph_tag.text) for paragraph_tag in paragraph_tag_collection]
        content = ' ,'.join(paragraph_content)
        return content

    def get_link_text(self) -> str:
        link_text = self.prepare_text(self.link_text) if self.link_text else ''
        return link_text

    def get_word_collection(self, content: str) -> List[str]:
        word_collection = re.findall(r'\w+', content)

        for index, word in enumerate(word_collection):
            if word in self.names:
                del word_collection[index]

        return word_collection

    def get_title_word_collection(self) -> List[str]:
        return self.get_word_collection(self.get_title())

    def get_content_word_collection(self) -> List[str]:
        return self.get_word_collection(self.get_content())

    def get_page_word_collection(self) -> List[str]:
        return self.get_title_word_collection() + self.get_content_word_collection()

    def get_page_word_unique_collection(self) -> Set[str]:
        return set(self.get_page_word_collection())

    def get_link_word_unique_collection(self) -> Set[str]:
        return set(self.get_word_collection(self.get_link_text()))

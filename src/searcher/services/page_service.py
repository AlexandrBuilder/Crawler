from typing import Iterable, Set

from searcher.models import WordModel, db, UrlModel, WordLocationModel, LinkBetweenUrlModel, LinkWordModel
from searcher.helpers.page_parser_helper import PageParserHelper
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert


@compiles(Insert)
def prefix_inserts(insert, compiler, **kw):
    return compiler.visit_insert(insert, **kw) + " ON CONFLICT DO NOTHING"


class PageHandlerService:

    def __init__(self, url: str, content: str, parent_url_id: int, link_text: str):
        self.url = url
        self.content = content
        self.parent_url_id = parent_url_id
        self.link_text = link_text

        self._page_parser = PageParserHelper(content, link_text)
        self._url_id = None

    async def get_url_id(self) -> int:
        if not self._url_id:
            url_model = await UrlModel.query.where(UrlModel.url == self.url).gino.first()
            self._url_id = url_model.id
        return self._url_id

    async def save_url(self) -> None:
        await UrlModel.insert().gino.all({'url': self.url})

    async def get_not_exist_in_db_word_collection(self) -> Set[str]:
        word_collection = self._page_parser.get_page_word_unique_collection()
        word_collection.update(self._page_parser.get_link_word_unique_collection())
        word_model_collection = await WordModel.query.where(WordModel.word.in_(word_collection)).gino.all()
        word_collection_from_db = set(word_model.word for word_model in word_model_collection)
        return word_collection - word_collection_from_db

    async def save_word_collection(self):
        missing_words_collection_in_db = await self.get_not_exist_in_db_word_collection()
        words_collection_for_db = [{'word': missing_word} for missing_word in missing_words_collection_in_db]

        while len(words_collection_for_db):
            words_collection_for_query = words_collection_for_db[:50]
            words_collection_for_db = words_collection_for_db[50:]
            query = WordModel.insert().values(words_collection_for_query)
            await db.all(query)

    async def save_word_location_collection(self):
        word_collection = self._page_parser.get_page_word_unique_collection()

        word_model_collection = await WordModel.query.where(WordModel.word.in_(word_collection)).gino.all()
        word_ids = {word.word: word.id for word in word_model_collection}

        url_id = await self.get_url_id()
        word_location_for_db = []
        for position, word in enumerate(self._page_parser.get_page_word_collection()):
            word_location_for_db.append({'word_id': word_ids[word], 'url_id': url_id, 'position': position})

        while len(word_location_for_db):
            words_collection_for_query = word_location_for_db[:50]
            word_location_for_db = word_location_for_db[50:]
            query = WordLocationModel.insert().values(words_collection_for_query)
            await db.all(query)

    async def save_link_between_url(self) -> int:
        url_id = await self.get_url_id()
        await LinkBetweenUrlModel.insert().gino.all({'url_from_id': self.parent_url_id, 'url_to_id': url_id})
        link_between_url = await LinkBetweenUrlModel \
            .query \
            .where(LinkBetweenUrlModel.url_from_id == self.parent_url_id) \
            .where(LinkBetweenUrlModel.url_to_id == url_id) \
            .gino \
            .first()
        return link_between_url.id

    async def save_link_word_collection(self, link_between_url_id: int):
        word_collection = self._page_parser.get_link_word_unique_collection()
        word_model_collection = await WordModel.query.where(WordModel.word.in_(word_collection)).gino.all()
        word_ids = {word.word: word.id for word in word_model_collection}

        link_word_for_db = []
        for link_word in self._page_parser.get_link_word_unique_collection():
            link_word_for_db.append({'word_id': word_ids[link_word], 'between_url_id': link_between_url_id})

        query = LinkWordModel.insert().values(link_word_for_db)
        await db.all(query)

    async def save_index_by_content(self):
        await self.save_url()
        await self.save_word_collection()
        await self.save_word_location_collection()
        link_between_url_id = await self.save_link_between_url()
        await self.save_link_word_collection(link_between_url_id)

    def get_new_urls(self) -> Iterable:
        return self._page_parser.get_new_urls()

from typing import Dict
from typing import List

from elasticsearch import AsyncElasticsearch
from sanic import exceptions

from models import Joke
from repository.jokes import JokesRepository


class JokesRepositoryElasticsearch(JokesRepository):
    def __init__(self, elasticsearch: AsyncElasticsearch):
        self.elasticsearch = elasticsearch
    
    async def create(self, username: str, joke: str) -> Joke:
        body = {
            "username": username,
            "joke":     joke,
            }
        
        response = await self.elasticsearch.index(
            index=self.INDEX,
            body=body
            )
        _id = response['_id']
        return Joke(id=_id, username=username, joke=joke)
    
    async def __search_by_id(self, _id: str, username: str) -> Dict[str, str]:
        response = await self.elasticsearch.search(
            index=self.INDEX,
            body={
                "query": {
                    "terms": {
                        "_id": [_id]
                        }
                    }
                }
            )
        hits = response['hits']['hits']
        if len(hits) == 0:
            raise exceptions.NotFound("Joke not found.")
        source = hits[0]['_source']
        username_source = source['username']
        if username_source != username:
            raise exceptions.NotFound("Joke not found.")
        return source
    
    async def read(self, _id: str, username: str) -> Joke:
        source = await self.__search_by_id(_id, username)
        
        joke = source['joke']
        return Joke(id=_id, username=username, joke=joke)
    
    async def read_all(self, username: str) -> List[Joke]:
        response = await self.elasticsearch.search(
            index=self.INDEX,
            body={
                "query": {
                    "bool": {
                        "must": {
                            "match": {
                                "username": username,
                                }
                            }
                        }
                    }
                }
            )
        hits = response['hits']['hits']
        if len(hits) == 0: raise exceptions.NotFound("Jokes not found.")
        
        return [
            Joke(id=hit['_id'], username=hit['_source']['username'], joke=hit['_source']['joke'])
            for hit in hits
            ]
    
    async def update(self, _id: str, username: str, joke: str) -> Joke:
        source = await self.__search_by_id(_id, username)
        
        response = await self.elasticsearch.update(
            index=self.INDEX,
            id=_id,
            body={
                "doc": {
                    "joke": joke
                    }
                }
            )
        return Joke(id=_id, username=username, joke=joke)
    
    async def delete(self, _id: str, username: str) -> None:
        source = self.__search_by_id(_id, username)
        
        response = await self.elasticsearch.delete(
            index=self.INDEX,
            id=[_id]
            )
        return None

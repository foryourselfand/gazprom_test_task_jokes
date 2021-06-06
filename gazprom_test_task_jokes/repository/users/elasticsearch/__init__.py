import bcrypt
from elasticsearch import AsyncElasticsearch
from sanic import exceptions

from models import User
from repository.users import UsersRepository


class UsersRepositoryElasticsearch(UsersRepository):
    def __init__(self, elasticsearch: AsyncElasticsearch):
        self.elasticsearch = elasticsearch
    
    async def create(self, username: str, password: str) -> User:
        body_search = {
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
        response_search = await self.elasticsearch.search(
            index=self.INDEX,
            body=body_search
            )
        hits = response_search['hits']['hits']
        if len(hits) != 0:
            raise exceptions.Forbidden("User with that username already exist.")
        
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        response_index = await self.elasticsearch.index(
            index='users',
            body={
                "username": username,
                "password": password_hashed,
                }
            )
        return User(username=username, password=password_hashed)
    
    async def read(self, username: str) -> User:
        body_search = {
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
        response_search = await self.elasticsearch.search(
            index=self.INDEX,
            body=body_search
            )
        hits = response_search['hits']['hits']
        if len(hits) == 0:
            raise exceptions.Unauthorized("User not found.")
        
        source = hits[0]['_source']
        source_username = source['username']
        source_password = source['password']
        return User(username=source_username, password=source_password)

from dataclasses import dataclass

from sanic_openapi.openapi2 import doc


@dataclass
class User:
    username: str = doc.String("The name of your user account.")
    password: str = doc.String("The password of your user account.")


@dataclass
class Joke:
    id: str = doc.String("The unique identifier of your very funny joke.")
    joke: str = doc.String("Your very funny joke.")
    username: str = doc.String("The name of your user account.")

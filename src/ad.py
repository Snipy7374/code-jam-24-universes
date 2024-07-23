import json
from pathlib import Path
from random import choice

import disnake

type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class Ad(disnake.Embed):
    """A Wikipedia "ad".

    Generates an embed of a random Wikipedia "ad"
    The ad's subject is randomly chosen among the 676 the pages appearing first after searching for 2
    (random) ascii letters
    This class is a subclass of `disnake.Embed`.
    """

    def __init__(self) -> None:
        with Path("./ads.json").open() as file:
            data: JSON = json.loads(file.read())
        data: JSON = choice(data)  # noqa: S311
        self.title: str = data["title"]
        super().__init__(title=self.title, description=data["description"])

        self.set_thumbnail(url=data["thumbnail_url"])
        self.set_footer(text="Unique Universes 2024")

    def __repr__(self) -> str:
        return f"<Ad {self.title=}>"

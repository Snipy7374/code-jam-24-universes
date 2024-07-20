from random import choices
from string import ascii_letters

import disnake
import requests

type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class Ad(disnake.Embed):
    """A Wikipedia "ad".

    Generates an embed of a random Wikipedia "ad"
    The ad's subject is randomly chosen among the 676 the pages appearing first after searching for 2
    (random) ascii letters
    This class is a subclass of `disnake.Embed`.
    """

    def __init__(self) -> None:
        page_object: JSON = requests.get(
            "https://en.wikipedia.org/w/rest.php/v1/search/title",
            {
                "limit": 2,
                "q": choices(ascii_letters, k=2),  # noqa: S311
                # ascii_letters, k=2 -> 26² = 676 possible ads at runtime
            },
            timeout=5,
        ).json()[1]  # the second page_object is chosen to avoid the disambiguation pages

        self.key: str = page_object["key"]
        title: str = page_object["title"]
        url: str = f"https://en.wikipedia.org/wiki/{self.key}"
        image_url: str = page_object["thumbnail"]["url"]
        html: str = requests.get(
            f"https://en.wikipedia.org/w/rest.php/v1/page/{self.key}/html",
            timeout=5,
        ).text

        super().__init__(title=title, url=url, description=html)

        self.set_image(url=image_url)
        self.set_footer(text="Unique Universes 2024")

    def __repr__(self) -> str:
        return f"<Ad {self.key=}>"

from gbf_automata.schema.display import Display
from gbf_automata.schema.image_area import ImageModel

class GameArea:
    def __init__(
        self,
        display_identify: int,
        aspect_ratio: dict,
        menu: ImageModel,
        news: ImageModel,
        home: ImageModel
    ) -> None:
        self._display_identify = display_identify
        self._aspect_ratio = Display(**aspect_ratio)
        self._menu = menu
        self._news = news
        self._home = home

    def __repr__(self) -> str:
        return (
            f"Display ID {self._display_identify} "
            f"Aspect Ratio {self._aspect_ratio} "
        )

    def accuracy(self) -> float:
        return (self._menu.accuracy() + self._news.accuracy() + self._home.accuracy())

    def game_dimension(self) -> dict:
        return {
            "top": self._aspect_ratio.top + self._news.min_loc[1],
            "left": self._aspect_ratio.left + self._news.min_loc[0],
            "width": self._aspect_ratio.width - (self._aspect_ratio.width - self._menu.min_loc[0] + self._menu.image_width) - self._news.min_loc[0],
            "height": self._aspect_ratio.height - (self._aspect_ratio.height - self._home.min_loc[1] + self._home.image_height) - self._news.min_loc[1],
            "mon": self._display_identify
        }

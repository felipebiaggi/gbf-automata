from gbf_automata.schema.display import Display
from gbf_automata.enums.template_match import TemplateMatch


class GameArea:
    def __init__(
        self,
        display_identify: int,
        aspect_ratio: dict,
        method: TemplateMatch,
        menu_accuracy: float,
        news_accuracy: float,
        home_accuracy: float,
    ) -> None:
        self._display_identify = display_identify
        self._aspect_ratio = Display(**aspect_ratio)
        self._method = method

        self._menu_acurracy = menu_accuracy
        self._news_accuracy = news_accuracy
        self._home_accuracy = home_accuracy

    def __repr__(self) -> str:
        return (
            f"Display ID {self._display_identify} "
            f"Aspect Ratio {self._aspect_ratio} "
        )

    def accuracy(self) -> float:
        return self._menu_acurracy + self._news_accuracy + self._home_accuracy

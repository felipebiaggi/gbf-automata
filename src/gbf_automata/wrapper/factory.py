import platform
from typing import Any
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError
from gbf_automata.wrapper.base import PointerBase


def pointer(**kwargs: Any) -> PointerBase:
    os_ = platform.system().lower()

    if os_ == "linux":
        from gbf_automata.wrapper.linux import x11

        return x11.Pointer(**kwargs)

    if os_ == "windows":
        raise GBFAutomataError(f"system {os_!r} not yet implemented.")

    if os_ == "darwin":
        raise GBFAutomataError(f"system {os_!r} not yet implemented.")

    raise GBFAutomataError(f"LOL?")

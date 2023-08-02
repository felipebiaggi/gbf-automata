import logging
import os
import multiprocessing
from typing import Tuple
from ctypes.util import find_library
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError
from gbf_automata.wrapper.base import PointerBase
from ctypes import (
    POINTER,
    byref,
    c_uint32,
    cdll,
    c_char_p,
    c_void_p,
    c_int,
    c_uint,
    c_bool,
)

logger = logging.getLogger(__name__)

_X11 = find_library("X11")
ENV_DISPLAY = os.environ["DISPLAY"].encode("utf-8")

cfunctions = [
    (
        "XOpenDisplay",
        [
            c_char_p,
        ],
        c_void_p,
    ),
    (
        "XDefaultRootWindow",
        [
            c_void_p,
        ],
        c_uint32,
    ),
    (
        "XCloseDisplay",
        [
            c_void_p,
        ],
        c_void_p,
    ),
    (
        "XQueryPointer",
        [
            c_void_p,
            c_uint32,
            POINTER(c_char_p),
            POINTER(c_char_p),
            POINTER(c_int),
            POINTER(c_int),
            POINTER(c_int),
            POINTER(c_int),
            POINTER(c_uint),
        ],
        c_bool,
    ),
    (
        "XWarpPointer",
        [
            c_void_p,
            c_uint32,
            c_uint32,
            c_int,
            c_int,
            c_uint,
            c_uint,
            c_int,
            c_int,
        ],
        c_void_p,
    ),
    (
        "XFlush",
        [
            c_void_p,
        ],
        c_void_p,
    ),
]


class Pointer(PointerBase):
    def __init__(self) -> None:

        self._lock = multiprocessing.Lock()

        if not ENV_DISPLAY:
            raise GBFAutomataError("Environment Display not found")

        if not _X11:
            raise GBFAutomataError("X11 libray not found")

        self._xlib = cdll.LoadLibrary(_X11)

        self._define_cfunctions()

        self._display = self._xlib.XOpenDisplay(ENV_DISPLAY)

        self._root = self._xlib.XDefaultRootWindow(self._display)

    def close(self) -> None:
        logger.debug(f"Close Display <{self._display}>")
        self._xlib.XCloseDisplay(self._display)

    def get_position(self) -> Tuple[int, int]:
        with self._lock:
            _root_id = c_char_p()
            _child_id = c_char_p()
            _root_x = c_int()
            _root_y = c_int()
            _win_x = c_int()
            _win_y = c_int()
            _mask = c_uint()
     
            self._xlib.XQueryPointer(
                self._display,
                self._root,
                byref(_root_id),
                byref(_child_id),
                byref(_root_x),
                byref(_root_y),
                byref(_win_x),
                byref(_win_y),
                byref(_mask),
            )

        return (_root_x.value, _root_y.value)

    def set_position(self, x: int, y: int) -> None:
        with self._lock:
            self._xlib.XWarpPointer(self._display, 0, self._root, 0, 0, 0, 0, x, y)

            self._xlib.XFlush(self._display)

    def _define_cfunctions(self) -> None:
        for function, argtypes, restype in cfunctions:
            method = getattr(self._xlib, function)
            method.argtypes = argtypes
            method.restype = restype

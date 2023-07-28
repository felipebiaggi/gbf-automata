import platform
import os
from typing import Tuple
from ctypes import (
    POINTER,
    c_uint,
    c_uint32,
    cdll,
    byref,
    c_char_p,
    c_void_p,
    c_int,
    c_bool,
)
from ctypes.util import find_library

os_ = platform.system().lower()

_X11 = None

if os_ == "linux":
    _X11 = find_library("X11")

if not _X11:
    raise Exception


ENV_DISPLAY = os.environ["DISPLAY"].encode("utf-8")

xlib = cdll.LoadLibrary(_X11)

functions = [
    (xlib.XOpenDisplay, [c_char_p], c_void_p),
    (xlib.XDefaultRootWindow, [c_void_p], c_uint32),
    (xlib.XCloseDisplay, [c_void_p], c_void_p),
    (
        xlib.XQueryPointer,
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
        xlib.XWarpPointer,
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
    (xlib.XFlush, [c_void_p], c_void_p),
]

for function, argtypes, restype in functions:
    function.argtypes = argtypes
    function.restype = restype


def get_position() -> Tuple[int, int]:
    _root_id = c_char_p()
    _child_id = c_char_p()
    _root_x = c_int()
    _root_y = c_int()
    _win_x = c_int()
    _win_y = c_int()
    _mask = c_uint()

    _p_display = xlib.XOpenDisplay(ENV_DISPLAY)
    _root = xlib.XDefaultRootWindow(_p_display)

    xlib.XQueryPointer(
        _p_display,
        _root,
        byref(_root_id),
        byref(_child_id),
        byref(_root_x),
        byref(_root_y),
        byref(_win_x),
        byref(_win_y),
        byref(_mask),
    )

    xlib.XCloseDisplay(_p_display)

    return (_root_x.value, _root_y.value)


def set_position(x_position: int, y_position: int) -> None:
    _p_display = xlib.XOpenDisplay(ENV_DISPLAY)
    _root = xlib.XDefaultRootWindow(_p_display)

    xlib.XWarpPointer(_p_display, 0, _root, 0, 0, 0, 0, x_position, y_position)

    xlib.XFlush(_p_display)

    xlib.XCloseDisplay(_p_display)

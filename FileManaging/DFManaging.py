"""
Description:
    This file contains functions serving EIH.py
"""


def default_value(attribute: str, kwarg: dict):
    if attribute in kwarg:
        return kwarg[attribute]
    else:
        return None

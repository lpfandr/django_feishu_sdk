#!/usr/bin/env python3.8
class Dict2Obj(dict):

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value


class InvalidEventException(Exception):
    def __init__(self, error_info):
        self.error_info = error_info

    def __str__(self) -> str:
        return "Invalid event: {}".format(self.error_info)

    __repr__ = __str__


# class Obj(dict):
#     def __init__(self, d):
#         for a, b in d.items():
#             if isinstance(b, (list, tuple)):
#                 setattr(self, a, [Obj(x) if isinstance(x, dict) else x for x in b])
#             else:
#                 setattr(self, a, Obj(b) if isinstance(b, dict) else b)
#
#
# def dict_2_obj(d: dict):
#     return Obj(d)

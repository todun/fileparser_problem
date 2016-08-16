#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Used to simulate an enum with unique values
class Enumeration(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    def __setattr__(self, name, value):
        raise RuntimeError("Cannot override values")

    def __delattr__(self, name):
        raise RuntimeError("Cannot delete values")

# -*- coding: utf-8 -*.t-
from __future__ import print_function
from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
import functools
import numpy as np


class Searcher(with_metaclass(ABCMeta, object)):
    """Abstract class of searching data."""

    def is_type(self, data_type):
        if data_type == self.data_type:
            return True
        return False

    def _check_data(func):
        """Function of checking value of search conditions."""
        @functools.wraps(func)
        def wrapper(*args):
            if args[1] is None:
                raise ValueError("Search column must not None.")
            if args[3] is None:
                raise ValueError("Search value must not None.")
            return func(*args)
        return wrapper

    @abstractmethod
    def search(self):
        pass


class NumberSearcher(Searcher):
    """Class of search number data.

    Params:
        data: number data.

        columns: number data columns.
    """

    def __init__(self, data, columns):
        self.data_type = "number"
        self.data = np.array(data)
        self.columns = columns

    @Searcher._check_data
    def search(self, column, operator, value):
        """Function of searching data.

        Params:
            column: searched data column index.

            operator: search operator.

            value: search value.
        """
        index = []
        if operator == "=":
            index.extend(np.where(self.data[:, column] == float(value))[0])
        elif operator == ">":
            index.extend(np.where(self.data[:, column] >= float(value))[0])
        elif operator == "<":
            index.extend(np.where(self.data[:, column] <= float(value))[0])
        return index


class TextSearcher(Searcher):
    """Class of search text data.

    Params:
        data: text data.

        columns: text data columns.
    """

    def __init__(self, data, columns):
        self.data_type = "text"
        self.data = np.array(data)
        self.columns = columns

    @Searcher._check_data
    def search(self, column, operator, value):
        """Function of searching data.

        Params:
            column: searched data column index.

            operator: search operator.

            value: search value.
        """
        index = []
        if operator == "=":
            index.extend(np.where(self.data[:, column] == value)[0])
        elif operator == "like":
            for i, d in enumerate(self.data[:, column]):
                if value in d:
                    index.append(i)
        return index


class SearcherResolver(object):
    """Resolve searcher from data_type."""

    def __init__(self, numbers, texts, number_columns, text_columns):
        self.searcher_list = [
            NumberSearcher(numbers, number_columns),
            TextSearcher(texts, text_columns)]

    def resolve(self, data_type):
        """Function of getting searcher.

        Params:
            data_type: type of data.

        Return:
            searcher: resolved searcher instance.
        """
        for s in self.searcher_list:
            if s.is_type(data_type):
                return s

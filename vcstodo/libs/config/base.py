#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import json

from functools import wraps


class Field(object):
    """
        Subclass this if you want to use a special type in your config file.
    """

    def __init__(self, path=None):
        self.path = path
        self.name = None


    def get_path(self):
        return self.path or self.name


    def convert_loaded_data(self, value):
        """
            Identity function to override if you plan to make a subclass.

            It should return a python object from given a json value
            serialized by "convert_data_to_save".
        """
        raise NotImplementedError


    def convert_data_to_save(self, value):
        """
            Identity function to override if you plan to make a subclass.

            It should return a json serialisable representation of the value
            and should be able to be reversed by "convert_loaded_data".
        """
        raise NotImplementedError


class Meta(object):
    """
        Just a data holder to avoid polluating the namespace
    """
    pass


class ConfigMetaclass(type):
    """
        Store all the fields to the meta namespace, in an iterable.
        Set the attribute value to None.
    """

    def __new__(cls, name, bases, dct):

        meta = dct.pop('Meta', Meta)()
        meta.fields = []
        for name, field in dct.iteritems():
            if isinstance(field, Field):
                meta.fields.append((name, field))
                field.name = name
                dct[name] = None

        dct['_meta'] = meta

        return super(ConfigMetaclass, cls).__new__(cls, name, bases, dct)


class Config(dict):
    """
        A wrapper arround a json configuration file.
    """

    __metaclass__ = ConfigMetaclass


    def __init__(self, **kwargs):
        self.load(kwargs)


    def get_default(self, name):
        """
            Return a default value for the give field.
            The default should be stored in the meta default mapping
            of name and values.
            Values can be callable, they will receive the config object
            and the name in parameter.
        """
        default = self._meta.default[name]

        try:
            return default(self, name)
        except TypeError:
            return default


    def get_config_file_path(self):
        try:
            return self.config_file_path
        except AttributeError:
            raise NotImplemented("You must set 'config_file_path' or "
                                 "implement 'get_config_file_path'" )

    @classmethod
    def update_file(cls, **kwargs):
        c = cls()
        c.update(kwargs)
        c.save()


    def load(self, data=None):
        try:
            path = self.get_config_file_path()
            data = data or json.load(open(path))
        except ValueError:
            raise ValueError("Unable to load config file %s. "
                             "Check it's a proper json file" % path)
        self.update(self.convert_loaded_data(data))


    def save(self, path=None):
        json.dump(self, open(path or self.get_config_file_path(), 'w'), indent=4)


    def convert_data_with_fonction(self, data, function_name):
        """
            Apply special conversion to data for each field declared in this config.

            This allows a user to define custom types for some entries.

            If the name of the fields contains '__', consider each part
            of the same between them, as several level of nesting.
        """
        for name, field in self._meta.fields:
            value = data
            parent = data
            for step in name.split('__'):
                try:
                    parent = value
                    value = value[step]
                except KeyError:
                    parent = None
            if parent is not None:
                parent[step] = getattr(field, function_name)(value)
        return data


    def convert_loaded_data(self, data):
        """
            Apply special conversion to data that has just been loaded.

            This allows a user to define custom types for some entries.

            If the name of the fields contains '__', consider each part
            of the same between them, as several level of nesting.
        """
        return self.convert_data_with_fonction(data, 'convert_loaded_data')



    def convert_data_to_save(self, data):
        """
            Apply special conversion to data that is going to be saved.

            This allows a user to define custom types for some entries.
        """
        return self.convert_data_with_fonction(data, 'convert_data_to_save')


    def __enter__(self):
        self.load()
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.save()


    def __call__(self, func):

        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(self, *args, **kwargs)
        return inner


    def __getitem__(self, key):
        """
            Return the dict entry, or a default value if the user specified it.
        """
        try:
            return super(Config, self).__getitem__(key)
        except:
            return self.get_default(key)


    def __getattr__(self, attr):
        """
            Try to return a dict entry before returning an attribute.
        """
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

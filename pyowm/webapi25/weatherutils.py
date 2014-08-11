#!/usr/bin/env python

"""
Module containing search and filter utilities for *Weather* objects lists
management
"""
from pyowm.exceptions import not_found_error

def status_is(weather, status, weather_code_registry):
    """
    Checks if the weather status code of a *Weather* object corresponds to the
    detailed status indicated. The lookup is performed against the provided 
    *WeatherCodeRegistry* object.

    :param weather: the *Weather* object whose status code is to be checked
    :type weather: *Weather*
    :param status: a string indicating a detailed weather status
    :type status: str
    :returns: ``True`` if the check is positive, ``False`` otherwise

    """
    weather_status = weather_code_registry. \
        status_for(weather.get_weather_code()).lower()
    return weather_status == status

def any_status_is(weather_list, status, weather_code_registry):
    """
    Checks if the weather status code of any of the *Weather* objects in the
    provided list corresponds to the detailed status indicated. The lookup is
    performed against the provided *WeatherCodeRegistry* object.

    :param weathers: a list of *Weather* objects
    :type weathers: list
    :param status: a string indicating a detailed weather status
    :type status: str
    :returns: ``True`` if the check is positive, ``False`` otherwise
    
    """
    for weather in weather_list:
        if status_is(weather, status, weather_code_registry):
            return True
    return False

def status_matches_any(word_list, weather):
    """
    Checks if one or more keywords in a given list matches the
    detailed weather status of a *Weather* object

    :param word_list: a list of string keywords
    :type word_list: list
    :param weather: a *Weather* object
    :type weather: *Weather*
    :returns: ``True`` if one or more matchings are found, ``False`` otherwise

    """
    detailed_status = weather.get_detailed_status().lower()
    for word in word_list:
        if word in detailed_status:
            return True
    return False


def filter_by_matching_statuses(word_list, weathers_list):
    """
    Returns a sublist of the given list of *Weather* objects, whose items
    have at least one of the keywords from the given list as part of their
    detailed statuses.

    :param word_list: a list of string keywords
    :type word_list: list
    :param weathers_list: a list of *Weather* objects
    :type weathers_list: list
    :returns: a list of *Weather* objects
    """
    result = []
    for weather in weathers_list:
        if status_matches_any(word_list, weather):
            result.append(weather)
    return result


def is_in_coverage(unixtime, weathers_list):
    """
    Checks if the supplied UNIX time is contained into the time range
    (coverage) defined by the most ancient and most recent *Weather* objects
    in the supplied list

    :param unixtime: the UNIX time to be searched in the time range
    :type unixtime: int
    :param weathers_list: the list of *Weather* objects to be scanned for
        global time coverage
    :type weathers_list: list
    :returns: ``True`` if the UNIX time is contained into the time range,
        ``False`` otherwise
    """
    if not weathers_list:
        return False
    else:
        min_of_coverage = min([weather.get_reference_time() \
                               for weather in weathers_list])
        max_of_coverage = max([weather.get_reference_time() \
                               for weather in weathers_list])
        if unixtime < min_of_coverage or unixtime > max_of_coverage:
            return False
        return True


def find_closest_weather(weathers_list, unixtime):
    """
    Extracts from the provided list of Weather objects the item which is
    closest in time to the provided UNIXtime.

    :param weathers_list: a list of *Weather* objects
    :type weathers_list: list
    :param unixtime: a UNIX time
    :type unixtime: int
    :returns: the *Weather* object which is closest in time or ``None`` if the
        list is empty
    """
    if not weathers_list:
        return None
    if not is_in_coverage(unixtime, weathers_list):
        raise not_found_error.NotFoundError('Error: the specified time is ' + \
                                'not included in the weather coverage range')
    closest_weather = weathers_list[0]
    time_distance = abs(closest_weather.get_reference_time() - unixtime)
    for weather in weathers_list:
        if abs(weather.get_reference_time() - unixtime) < time_distance:
            time_distance = abs(weather.get_reference_time() - unixtime)
            closest_weather = weather
    return closest_weather

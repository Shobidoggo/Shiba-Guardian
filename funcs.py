from typing import Iterable
import typing, string

def count(obj: Iterable):

    """Return the number of items in a container."""
    # get the count
    number = 0

    # get the amount of elements
    for element in obj:
        number += 1
        
    # return the number
    return number

def round(num: float, to_nearest: float = None):
    if to_nearest:
        string = str(to_nearest)
        counter = count(string[1:count(string)]) if count(string) >= 1 else 1

    zero = float(num) - int(num)
    if zero >= 0.5:
        return int(num)+1
    elif zero < 0.5:
        return int(num)

def last(obj: Iterable):

    """Return the last element in a container."""

    getLast = []
    for key in obj:
        getLast.append(key)

    lastKey = getLast[-1]

    return lastKey

def first(obj: Iterable):

    """Return the last element in a container."""

    defineObj = []
    for key in obj:
        defineObj.append(key)

    firstKey = defineObj[0]

    return firstKey

def capt(obj: str):
    """Returns your string but every letter at a beggining of a word is capatilized"""

    obj = obj.lower()
    words = obj.split()
    word_data = []

    for word in words:
        word_data.append( word[0].upper() + word[1:count(word)] )
    
    return " ".join(word_data)

def rep(object: str, first: str, second: str):
    """
        A version of replace but in a simpler form of code.
        Currently in beta.
    """

    words = []
    for place in object.split(first):
        words.append(place+second)
    return ''.join(words[0:(count(words) - 1)])

def equal_to(first_obj, second_obj):

    """Returns True or False if or not if equal to."""

    if first_obj == second_obj:
        return True
    elif first_obj != second_obj:
        return False

def check(obj):

    if obj:
        return True
    elif not obj:
        return False

def raw(content: str):
    """Raws a discord markdown message"""

    strings = []
    for char in content:
        if char in string.ascii_letters or \
            char in string.digits or \
                char in [" ","\n"]:
            strings.append(char)
        else:
            strings.append(f"\\{char}")
    return ''.join(strings)

def markdown(
    join_type:str,markdown:str,
    params:typing.List
):
    notNone=[]
    for param in params:
        if param and type(param) == str:
            notNone.append(param)
    return join_type.join(f"{markdown}{p}{markdown}" for p in notNone)
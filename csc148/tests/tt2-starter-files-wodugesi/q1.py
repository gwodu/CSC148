""" CSC148 Summer 2021 Term Test 2
Q1: Recursion [35 marks]
-----------------------------------------------------------------------------

(i) [5 marks]  Create a new user-defined exception, SearchValueError, that
has the following error message:

    "Value not found in any files in this directory or its subdirectories."

(ii) [25 marks] Implement the method Directory.find according to its docstring
description. Your implementation **MUST** be recursive.

(iii) [5 marks] Indicate what precondition(s) are required on the input
parameters of the method Directory.get_filepath.

    It has to be a file. None of the parameters passed can be the same

You may not add any public functions, methods or attributes but you can add
private helper functions/methods. You don't need to provide docstrings or type
annotations for these helpers.

A syntax checker is available to you on MarkUs. Its only purpose is to check
for syntax errors i.e. it does NOT check for correctness.
"""
from __future__ import annotations
from typing import List, Union, Optional


# TODO: part (i) Create the new user-defined exception SearchValueError
class SearchValueError(Exception):

    def __str__(self):
        return "Value not found in any files in this directory or its subdirectories."


class File:
    """ A class representing a file on a computer.

    === Public Attributes ===
    name:
      The name of the file.
    contents:
      The contents of the file.
    directory:
      The directory in which the file is contained.

    === Representation Invariants ===
      - <directory> is not None iff there is exactly one <directory> for which
        the file is in <directory>.items

    === Example Usage ===

    >>> f = File("cat.txt", "meow meow meow~")
    >>> f.contents
    'meow meow meow~'
    >>> f.name
    'cat.txt'
    >>> f.directory is None
    True
    """

    name: str
    contents: str
    directory: Optional[Directory]

    def __init__(
            self, name: str, contents: str,
            directory: Optional[Directory] = None
    ) -> None:
        """ Initializer for an instance of File.

        See class-level docstring for usage.
        """
        self.name = name
        self.contents = contents
        self.directory = directory

    def __str__(self) -> str:
        """ Returns the string representation of File instances.
        """
        return self.name


class Directory:
    """ A class representation of a directory in a file system.

    === Public Attributes ===
    name:
      The name of the directory
    items:
      The items contained within the directory
    parent:
      The direct parent that this directory is contained within.

    === Representation Invariants ===
      - <parent> is None iff this directory is not contained in the <items> of
        any other directory.
      - <items> == [] iff there are no files with <directory> set to this
        directory AND there are no directories with <parent> set to this
        directory.

    === Example Usage ===
    >>> d1 = Directory("folder_1", [], None)
    >>> d1.name
    'folder_1'
    >>> d1.parent is None
    True
    >>> len(d1.items) == 0
    True
    >>> d2 = Directory("subfolder", [], None)
    >>> d1.add_item(d2)
    >>> d2 in d1.items
    True
    >>> len(d1.items) == 1
    True
    """
    name: str
    items: List[Union[Directory, File]]
    parent: Optional[Directory]

    def __init__(
            self, name, items: List[Union[Directory, File]],
            parent: Optional[Directory]
    ) -> None:
        """ Initializer for an instance of Directory.

        See class-level docstring for usage.
        """
        self.name = name
        self.items = items
        self.parent = parent

    def add_item(self, item: Union[Directory, File]) -> None:
        """ Add <item> to the <items> in this directory.

        Modify <item> so that it refers to the current directory as
        its parent/directory when it is a directory/file respectively.

        === Preconditions ===
          - <item> is not already in this directory's <items>.
        """
        self.items.append(item)
        if isinstance(item, File):
            item.directory = self
        elif isinstance(item, Directory):
            item.parent = self

    def _no_items(self):
        return len(self.items) == 0

    def find(self, val: str) -> str:
        """ Return the file path of **any file within the directory or its
        subdirectories** which has <contents> that include <val>.

        If none of the files in the directory or its subdirectories have
        <contents> that include <val>, raise a SearchValueError.

        Your implementation **MUST** be recursive.

        The file path is relative to the current directory.
        Hint: call the Directory.get_filepath method.

        >>> f1 = File("lorem.txt", "ipsum dolor")
        >>> d1 = Directory("home", [], None)
        >>> d2 = Directory("folder_1", [], d1)
        >>> d1.add_item(d2)  # d2 is a subdirectory of d1
        >>> d2.add_item(f1)  # f1 is in d2
        >>> d1.find("ipsum")
        'home/folder_1/lorem.txt'
        >>> d2.find("ipsum")
        'folder_1/lorem.txt'
        >>> d2.find("eggs")
        SearchValueError
        """
        file_path = ''
        if self._no_items(): # base case is if it's empty
             return '' #find suitable return value
        for sublist in self.items:
            if isinstance(sublist, File):
                if val in sublist.contents:
                    return self.get_filepath(sublist)
            else:
                file_name_add = str(self.name) + '/'
                file_path = sublist.find(val)
        if file_path == '':
            raise SearchValueError
        return file_name_add + file_path

    def get_filepath(self, file: File) -> str:
        """ Returns the relative file path for the file, relative
        to the current directory instance.

        **NOTE: Preconditions are omitted**

        >>> f1 = File("lorem.txt", "ipsum dolor")
        >>> d1 = Directory("home", [], None)
        >>> d2 = Directory("folder_1", [], d1)
        >>> d1.add_item(d2)
        >>> d2.add_item(f1)
        >>> d1.get_filepath(f1)
        'home/folder_1/lorem.txt'
        >>> d2.get_filepath(f1)
        'folder_1/lorem.txt'
        """
        curr = file
        path = [file.name]
        while curr != self:
            if isinstance(curr, File):
                path.append(curr.directory.name)
                curr = curr.directory
            elif isinstance(curr, Directory):
                path.append(curr.parent.name)
                curr = curr.parent

        return "/".join(path[::-1])

    def __str__(self):
        return f"{self.name}: " + "(" + ",".join(
            [str(item) for item in self.items]) + ")"


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    f1 = File("lorem.txt", "ipsum dolor")
    d1 = Directory("home", [], None)
    d2 = Directory("folder_1", [], d1)

    d1.add_item(d2)
    d2.add_item(f1)

    f2 = File("aaa.txt", "sit amet")

    print(f"Found 'ipsum' at {d1.find('ipsum')}")
    try:
        d1.find("sit amet")
    except SearchValueError:
        print(f"Correctly indicated 'sit amet' not found in {d1.name}")


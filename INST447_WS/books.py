""" Sort books by Library of Congress call number. """


from argparse import ArgumentParser
import re
import sys


# replace this comment with your implementation of the Book class

class Book:
    """A class to represent a book with its title, author, and call number.
    
    Attributes:
        - callnum (str): The call number for the book.
        - title (str): The title of the book.
        - author (str): The author of the book.
    """
    

    def __init__(self, callnum, title, author):
        """
        Initialize a Book instance.

        Parameters:
        - callnum (str): The call number for the book.
        - title (str): The title of the book.
        - author (str): The author of the book.
        """
        self.callnum = callnum
        self.title = title
        self.author = author
        
    def parse_call_number(self):
        """
        Parse the call number into its components.
        
        Args:
            self (Book): Instance of the Book class.

        Returns:
            dict: A dictionary containing the parsed components of the call 
                  number.
        """
        parts = re.match(r"([A-Z]+)(\d+(\.\d+)?)(.*)", self.callnum)
        if parts:
            class_part = parts.group(1)
            initial_numeric_part = parts.group(2)
            cutter_part = parts.group(4).strip()
            return {
                'class': class_part,
                'initial_numeric': initial_numeric_part,
                'cutter': cutter_part
            }
        else:
            return {
                'class': '',
                'initial_numeric': '',
                'cutter': ''
            }

    def __lt__(self, other):
        """
        Compare two Book instances based on their call numbers.

        Args:
            self (Book): Instance of the Book class.
            other (Book): Another instance of the Book class.

        Returns:
            bool: True if self.callnum sorts before other.callnum, 
                  False otherwise.
        """
        self_parts = self.parse_call_number()
        other_parts = other.parse_call_number()

        # Compare call numbers based on multiple criteria
        if self_parts['class'] != other_parts['class']:
            return self_parts['class'] < other_parts['class']
        elif self_parts['initial_numeric'] != other_parts['initial_numeric']:
            return float(self_parts['initial_numeric'] or 0) < float(other_parts['initial_numeric'] or 0)
        else:
            return self_parts['cutter'] < other_parts['cutter']


    def __repr__(self):
        """
        Return a string representation of the Book instance.
        
        Args:
            self (Book): Instance of the Book class.

        Returns:
        - str: A string that could be used to re-create the current instance 
               of Book.
        """
        return f"Book({repr(self.callnum)}, {repr(self.title)}, {repr(self.author)})"

def read_books(filename):
    """
    Read book information from a file and create instances of the Book class.

    Parameters:
    - filename (str): The path to the file containing book information.

    Returns:
    - list: A list of Book instances.
    """
    books = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Split the line into title, author, and call number
            title, author, callnum = line.strip().split('\t')
            # Create a Book instance and add it to the list
            books.append(Book(callnum, title, author))
    return books

def print_books(books):
    """ Print information about each book, in order. """
    for book in sorted(books):
        print(book)


def main(filename):
    """ Read book information from a file, sort the books by call number,
    and print information about each book. """
    books = read_books(filename)
    print_books(books)


def parse_args(arglist):
    """ Parse command-line arguments. """
    parser = ArgumentParser(arglist)
    parser.add_argument("filename", help="file containing book information")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filename)
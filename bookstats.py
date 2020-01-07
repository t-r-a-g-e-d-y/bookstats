#!/usr/bin/env python3
import functools
import os
import re
import sys

from collections import Counter
from pprint import pprint

# Title, Author, and Date are tab (\t) separated
# Title (Author First, Last Middle) (Date Finished)

# Example:
# 2019
# Slaughterhouse-Five	(Vonnegut, Kurt)	(1/3)
# Anna Karenina	(Tolstoy, Leo)	(2/8)
# War and Peace	(Tolstoy, Leo)	(5/11)

# year_ex = re.compile('\d{4}')
# data_ex = re.compile('(.*[\t\n]|$)(\(.*\)\t)?(\(.*\))?')

class BookLog:
    def __init__(self, fn):
        self.log_dict = self.process_log(fn)            # year: list of books
        self.author_dict = self.author_books()          # author: list of books
        self.author_counter = self.author_book_count()  # author: number of books

    def process_log(self, fn):
        '''
        Create a dict where keys are years and values are a list of books read that year
        '''
        with open(fn, 'r') as f:
            books = f.read().splitlines()

        log_dict = dict()
        current_year = ''

        for ln in books:
            if not ln or ln.startswith('#'):
                continue

            try:
                int(ln)
                current_year = ln
                log_dict[current_year] = list()
            except ValueError:
                data = re.sub('[\(\)]', '', ln)
                data = data.split('\t')
                log_dict[current_year].append(data)
        return log_dict

    def author_books(self):
        '''
        Create a dict where keys are authors and values are a list of books by author
        '''
        author_dict = dict()
        for year in self.log_dict.values():
            for book in year:
                if author_dict.get(book[1]):
                    author_dict[book[1]].append(book[0])
                else:
                    author_dict[book[1]] = [book[0]]
        return author_dict

    def author_book_count(self):
        author_counter = Counter()
        for author, books in self.author_dict.items():
            author_counter[author] = len(books)
        return author_counter

    def book_count(self, year=None):
        '''
        Return a count of books read in `year` if not none else total amount of books read
        '''
        if year:
            if not self.log_dict.get(year):
                return 0
            else:
                return len(self.log_dict[year])
        else:
            total = 0
            for year in self.log_dict:
                total += len(self.log_dict[year])
            return total

    def print_yearly_tally(self):
        for year in self.log_dict:
            print(f'{year}: {self.book_count(year):>3}')
        print(f'Total: {self.book_count()}')

    def most_common_authors(self, n=7):
        return self.author_counter.most_common(n)

    def search_authors(self, term, partial_matches=True):
        authors = list()
        split_term = re.split(', | ', term.lower())

        for author in self.author_dict.keys():
            if partial_matches:
                if any([t in author.lower() for t in split_term]):
                    authors.append(author)
            else:
                split_author = re.split(', | |; ', author.lower())
                if all([t in split_author for t in split_term]):
                    authors.append(author)
        return authors

    def search_books(self, term, partial_matches=True):
        books = list()
        split_term = re.split(', | ', term.lower())

        for year, year_books in self.log_dict.items():
            for book in year_books:
                if partial_matches:
                    if any([t in book[0].lower() for t in split_term]):
                        books.append(book)
                else:
                    split_title = re.split(', | |; ', book[0].lower())
                    if all([t in split_title for t in split_term]):
                        books.append(book)
        return books

class Prompt:
    def __init__(self, log):
        self.log = log
        self.log_dict = log.log_dict

        if os.name == 'nt':
            cls = 'cls'
        else:
            cls = 'clear'

        self.actions = {
            'ac':   {'help': 'Author count',
                     'func': functools.partial(print, len(self.log.author_dict.keys()))},

            'b':    {'help': 'b <term> Search books (partial matches)',
                     'func': functools.partial(self.search_books)},

            'bf':   {'help': 'bf <term> Search books (full matches)',
                     'func': functools.partial(self.search_books, partial_matches=False)},

            'cl':   {'help': 'Clear screen',
                     'func': functools.partial(os.system, cls)},

            'h':    {'help': 'Help',
                     'func': self.prompt_help},

            's':    {'help': 's <term> Search authors (partial matches)',
                     'func': functools.partial(self.search_authors)},

            'sf':   {'help': 'sf <term> Search authors (full matches)',
                     'func': functools.partial(self.search_authors, partial_matches=False)},

            'x':    {'help': 'Exit',
                     'func': functools.partial(exit, 'Goodbye!')},

            'yr':   {'help': 'Print a yearly tally',
                     'func': log.print_yearly_tally}
        }

        self.print_actions = {
            'a':    {'help': 'Most read authors',
                     'func': functools.partial(log.most_common_authors)},

            'al':   {'help': 'Author list',
                     'func': functools.partial(sorted, log.author_dict.keys())},

        }

        self.help = self.build_help()

    def __call__(self):
        while(True):
            user_input = input('>>> ').lower().split()
            if user_input:
                action, *args = user_input
            else:
                continue

            if self.actions.get(action):
                try:
                    self.actions[action]['func'](*args)
                except TypeError:
                    self.actions[action]['func']()

            elif self.print_actions.get(action):
                if action == 'a' and args:
                    try:
                        args[0] = int(args[0])
                        pprint(self.print_actions[action]['func'](args[0]))
                    except ValueError:
                        pprint(self.print_actions[action]['func']())
                else:
                    pprint(self.print_actions[action]['func']())
            else:
                try:
                    int(action)
                    result = self.log_dict.get(action)
                    if result:
                        for entry in result:
                            print(entry)
                        print(f'Total for {action}: {self.log.book_count(action)}')
                    else:
                        print(f'No entries for {action}')
                except ValueError:
                    pass

    def search_authors(self, term, partial_matches=True):
        authors = self.log.search_authors(term, partial_matches)
        if authors:
            for i, author in enumerate(authors):
                print(f'{author}:')
                for book in self.log.author_dict[author]:
                    print(book)
                if i != len(authors) - 1:
                    print()
        else:
            print(f'No authors found for search term: {term}')

    def search_books(self, term, partial_matches=True):
        books = self.log.search_books(term, partial_matches)
        if books:
            for i, book in enumerate(books):
                print(f'{", ".join(book)}')
                if i != len(books) - 1:
                    print()
        else:
            print(f'No books found for search term: {term}')

    def build_help(self):
        help_list = list()

        for k, v in self.actions.items():
            help_list.append([k, v['help']])

        for k, v in self.print_actions.items():
            help_list.append([k, v['help']])

        return sorted(help_list, key=lambda x: x[0])

    def prompt_help(self):
        print('Enter a year to get the book listing for that year.')
        print(f'Available years: {", ".join(self.log_dict.keys())}\n')
        print('Commands:')
        for action_help in self.help:
            print(f'{action_help[0]:>4}: {action_help[1]}')

def main():
    fn = sys.argv[1]
    if not os.path.exists(fn):
        exit(f'File not found {fn}')

    log = BookLog(fn)

    if '-i' in sys.argv:
        from textwrap import dedent
        title = '''
        .     __   __   __  ___      ___  __
        |    /  \ / _` /__`  |   /\   |  /__`
        |___ \__/ \__> .__/  |  /~~\  |  .__/

        '''
        print(dedent(title))

        prompt = Prompt(log)
        prompt.prompt_help()
        try:
            prompt()
        except (KeyboardInterrupt, EOFError):
            exit('')

    log.print_yearly_tally()

    print('Most read authors:')
    for k, v in log.most_common_authors():
        author = ' '.join(reversed(k.split(',')))
        print(f'{v:4} {author}')

if __name__ == '__main__':
    main()


import functools
import os
import sys

from pprint import pprint

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

            'la':   {'help': 'List authors',
                     'func': functools.partial(sorted, log.author_dict.keys())},

            'lb':   {'help': 'List books by author <author> (optional)',
                     'func': functools.partial(log.print_author_dict)}

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
                        # Check if we can pass a valid argument (integer) to Counter.most_common
                        args[0] = int(args[0])
                        pprint(self.print_actions[action]['func'](args[0]))
                    except ValueError:
                        pprint(self.print_actions[action]['func']())
                else:
                    if args:
                        pprint(self.print_actions[action]['func'](*args))
                    else:
                        pprint(self.print_actions[action]['func']())

            else:
                # No action found, if input is a year then print books and total for that year
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


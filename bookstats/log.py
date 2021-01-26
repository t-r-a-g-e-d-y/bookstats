import re

from collections import Counter

from . import colors

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
        self.log_dict = self.process_log(fn)                # year: list of books
        self.author_dict = self.build_author_dict()         # author: list of books
        self.author_counter = self.build_author_counter()   # author: number of books

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

    def build_author_dict(self):
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

    def build_author_counter(self):
        '''
        Create a counter where keys are authors and values are a count of books read by author
        '''
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

    def most_read_authors(self, n=7):
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

    def print_yearly_tally(self):
        for year in self.log_dict:
            print(f'{year}: {self.book_count(year):>3}')
        print(f'Total: {self.book_count()}')

    def print_all_and_tally(self):
        for year in self.log_dict:
            self.print_books_for_year(year)
            print(f'Total:{self.book_count(year):>3}\n')

    def print_books_for_year(self, year, sep=None):
        if not self.log_dict.get(year):
            print(f'No books found for year: {year}')
        else:
            print(year)
            for book in self.log_dict.get(year):
                if len(book) == 3:
                    title, author, date_completed = book
                else:
                    title, author = book
                    date_completed = ''

                if sep:
                    print(f'{title}{sep}{author}{sep}{date_completed}')
                else:
                    col_width = 50
                    pad_width = col_width - 5

                    if len(title) >= col_width:
                        title = f'{title[:pad_width]}...'
                    if len(author) >= col_width:
                        author= f'{author[:pad_width]}...'

                    print(f'{title:<{col_width}s}{author:<{col_width}s}{date_completed}')

    def print_author_dict(self, author=None):
        if author:
            authors = sorted(self.search_authors(author))

            for a in authors:
                print(f'{colors.GREEN}{a}:{colors.RESET}')
                for book in self.author_dict.get(a):
                    print(f'  {book}')
        else:
            for author, books in sorted(self.author_dict.items(), key=lambda x: x[0]):
                print(f'{colors.GREEN}{author}:{colors.RESET}')
                for book in books:
                    print(f'  {book}')


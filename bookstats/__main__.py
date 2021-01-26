import argparse

from .log import BookLog
from .prompt import Prompt

def main():
    parser = argparse.ArgumentParser(prog='bookstats')
    parser.add_argument('file', help='Log file')
    parser.add_argument('--all', action='store_true', help='Print all authors and books')
    parser.add_argument('--year', action='store', help='Print books from year')
    parser.add_argument('--authors', action='store_true', help='Print all authors')
    parser.add_argument('--most-read', action='store_true', help='Print most read authors')
    parser.add_argument('--unique-authors', action='store_true', help='Print number of unique authors')
    parser.add_argument('--search-authors', nargs='*', metavar='term', help='Print authors found for [term]')
    parser.add_argument('--search-books', nargs='*', metavar='term', help='Print books found for [term]')
    parser.add_argument('--yearly-tally', action='store_true', help='Print yearly tally')
    parser.add_argument('--all-tally', action='store_true', help='Print yearly tally')
    args = parser.parse_args()

    log = BookLog(args.file)

#    if args.interactive:
#        from textwrap import dedent
#        title = '''
#        .     __   __   __  ___      ___  __
#        |    /  \ / _` /__`  |   /\   |  /__`
#        |___ \__/ \__> .__/  |  /~~\  |  .__/
#
#        '''
#        print(dedent(title))
#
#        prompt = Prompt(log)
#        prompt.prompt_help()
#        try:
#            prompt()
#        except (KeyboardInterrupt, EOFError):
#            exit('')

    if args.all:
        log.print_author_dict()

    if args.authors:
        for author in sorted(log.author_dict.keys()):
            print(author)

    if args.most_read:
        print('Most read authors:')
        for k, v in log.most_read_authors():
            author = ' '.join(reversed(k.split(',')))
            print(f'{v:4} {author}')

    if args.search_authors:
        print(f'Author Search [{" ".join(args.search_authors)}]:')
        log.print_author_dict(' '.join(args.search_authors))

    if args.search_books:
        print(f'Book Search [{" ".join(args.search_books)}]:')
        books = log.search_books(' '.join(args.search_books))
        for book in books:
            print(book)

    if args.unique_authors:
        print(f'Unique authors: {len(log.author_dict.keys())}')

    if args.year:
        log.print_books_for_year(args.year)

    if args.yearly_tally:
        log.print_yearly_tally()

    if args.all_tally:
        log.print_all_and_tally()

if __name__ == '__main__':
    main()


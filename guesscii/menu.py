import subprocess, typing, time

class Menu(object):
    """An interface class that displays information to the user and ac-
    cesses data from its parent Guesscii instance."""

    #-----Private properties-----

    # Mutable
    @property
    def _pages(self):
        """The stack of pages."""
        return self.__pages[:]


    #-----Public methods-----

    def push(self, page):
        """Assumes page is a page object
        push the specified page to the stack."""

        # Defensive programming
        try:
            typing.page(page)
        except AssertionError as e:
            raise e.args[0]

        self.__pages.append(page)

    def back(self):
        """Display the previous page."""

        self.__pages = self._pages[:-1]


    # -----Magic methods-----

    def __init__(self):
        """Create a Menu object."""

        # Main algorithm
        self.__pages = []

    def __call__(self):
        self._pages[-1]()

def test():
    from page import Page
    from option import Option

    m = Menu()

    page_2 = Page('test page 2', '', {
        'b': Option('b', 'back', m.back)}, ['b'])

    def parse_1(data):
        args, kwargs = [], {}
        if data == 'n':
            args = [page_2]
        elif data != 'q':
            raise ValueError
        return data, args, kwargs

    page_1 = Page('test page', '', {
            'n': Option('n', 'next page', m.push),
            'q': Option('q', 'quit', quit)},
        ['n', 'q'], parse_1)
    print page_1.options.keys()

    m.push(page_1)
    while True:
        m()

if __name__ == '__main__':
    test()

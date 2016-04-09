import random, subprocess
from menu import Menu
from game import Game
from option import Option
from settings import Settings

class Guesscii(object):
    """The main class that handles the program."""

    # -----Public properties-----

    @property
    def options(self):
        """The options dictionary."""
        return self._options.copy()

    @property
    def game(self):
        """A game instance."""

        # Defensive programming
        try:
            assert self._game is not None, AttributeError
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        return self._game

    @property
    def defaults(self):
        """The default settings."""
        return self._defaults

    @property
    def settings(self):
        """The game's current settings."""
        return self._settings


    # -----Public property prescriptors-----

    @game.setter
    def game(self, game):
        """Assumes game is a Game object.

        Modify the game property."""

        # Polymorphic defensive programming
        try:
            assert hasattr(game, 'main'), TypeError
            assert callable(game.main), AttributeError
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self._game = game

    @game.deleter
    def game(self):
        self._game = None


    @settings.setter
    def settings(self, settings):
        """Assumes settings is a settings object.

        Modify the current settings."""

        # Polymorphic defensive programming
        try:
            assert False, NotImplementedError
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self._settings = settings

    @options.setter
    def options(self, options):
        """Assumes options is a dictionary where each value is an opti-
        on and each key is the key for that option."""

        # Defensive programming
        try:
            check_options(options)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        self.options = options

    #--------------------------------------------------------------------------


    # -----Public methods-----

    @property
    def main(self):
        """The loop that runs the program."""
        option = self.options["m"]
        while True:
            try:
                option, kwargs = option(**kwargs)
            except ValueError:
                continue

    @property
    def new_game(self):
        """Play the game with the current settings."""
        del self.game
        self.game = Game(self.settings)
        return self.game.main()

    @property
    def continue_game(self):
        """Continue the current game."""
        # Defensive programming
        try:
            check_None(self.game, AttributeError)
        except AssertionError as e:
            raise e.args[0]

        # Main algorithm
        return self.game.main()

    @property
    def display_page(self):
        """Assumes page  is a character that  accesses the  appropriate
        page from the pages dictionary"""
        return self._display_page


    # -----Magic methods-----

    def __init__(self):
        self._defaults = Settings()
        self._settings = self.defaults
        self._menu = Menu()
        self._pages =  {
            'settings': Page('Settings', '', {
                'r': Option('r', 'restore defaults', None),
                't': Option('t', 'types', None),
                'l': Option('l', 'length', None),
                'a': Option('a', 'attempts', None),
                'b': Option('b', 'back', self.menu.back),
                '\n': ''}, ['r', '\n', 't', 'l', 'a', '\n', 'b'])
            'help': Page('Help', 'coming soon', {
                'b': Option('b', 'back', self.menu.back)}, ['b']),
            'about': Page('About', 'coming soon', {
                'b': Option('b', 'back', self.menu.back)}, ['b'])}
        self.pages['menu'] = Page('Menu', '', {
            'n': Option('n', 'new game', self.new_game),
            'q': Option('q', 'quit', quit),
            's': Option('s', 'settings', self.pages['settings'])
            'h': Option('h', 'help', self.pages['help']),
            'i': Option('i', 'about', self.pages['about']),
            '\n': ''}, ['n', 'q', '\n', 's', 'h', 'i'])
        self.menu.push(self.pages['menu'])
        self._game = None

#        {'m': Page('Menu', '', options, order),
#                       's': Page('Settings', '',
#                                 {'r': Option('r', 'restore defaults', None),
#                                  't': Option('t', 'amount of guessing ' \
#                                              'letters', None),
#                                  'l': Option('l', 'combination length', None),
#                                  'a': Option('a', 'attempts allowed', None)},
#                                 ['r', 't', 'l', 'a'])}

if __name__ == '__main__':
    guesscii = Guesscii()
    guesscii.main()

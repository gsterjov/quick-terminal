#
#    Copyright 2013 Goran Sterjov
#    This file is part of QuickTerminal.
#
#    QuickTerminal is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    QuickTerminal is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QuickTerminal.  If not, see <http://www.gnu.org/licenses/>.
#

import signal

from config import Config
from gi.repository import Gtk, Keybinder
from window import Window


def on_hotkey (hotkey, window):
	if window.get_visible():
		window.hide()
	else:
		window.show_all()
		window.focus()


if __name__ == "__main__":
	config = Config()
	window = Window (config)

	Keybinder.init()
	Keybinder.bind (config.hotkey, on_hotkey, window)

	signal.signal (signal.SIGINT, signal.SIG_DFL)
	Gtk.main()
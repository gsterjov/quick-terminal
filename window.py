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

from gi.repository import Gtk, Gdk
from terminal import Terminal


class Window (Gtk.Window):

	def __init__ (self, config):
		self.config = config
		self.tabs = {}

		Gtk.Window.__init__(self)
		self.connect ("delete-event", Gtk.main_quit)
		self.connect ("activate-focus", self.__on_window_focused)

		self.set_keep_above (True)
		self.set_skip_taskbar_hint (True)
		self.set_skip_pager_hint (True)
		self.set_decorated (False)


		self.notebook = Gtk.Notebook()
		self.notebook.set_tab_pos (Gtk.PositionType.BOTTOM)
		self.notebook.set_show_border (False)
		self.notebook.set_show_tabs (False)
		self.notebook.set_border_width (0)

		self.current_terminal = self.add_terminal()
		self.add (self.notebook)

		screen = self.get_screen()
		self.move (0, 0)
		self.resize (screen.width(), screen.height() * .45)

		visual = screen.get_rgba_visual()
		if visual and screen.is_composited():
			self.set_visual (visual)


	def add_terminal (self):
		terminal = Terminal (self.config)
		terminal.connect ("key-release", self.__on_key_release)
		terminal.connect ("exited", self.__on_terminal_exited)

		number = self.notebook.append_page (terminal, None)
		self.tabs[number] = terminal
		self.notebook.set_current_page (number)

		return terminal


	def remove_terminal (self, terminal):
		for number in self.tabs.keys():
			if self.tabs[number] == terminal:
				self.notebook.remove_page (number)
				del self.tabs[number]

		if len(self.tabs) == 0:
			self.hide()
			
			term = self.add_terminal()
			term.show_all()
			self.current_terminal = term


	def __on_key_release (self, terminal, keyval, state):
		key, mods = self.config.shortcuts["new_tab"]

		# ignore numlock
		mods |= Gdk.ModifierType.MOD2_MASK
		state |= Gdk.ModifierType.MOD2_MASK

		if key == keyval and mods == state:
			self.add_terminal()
			self.show_all()
			return False

		return True


	def __on_terminal_exited (self, terminal):
		self.remove_terminal (terminal)


	def __on_window_focused (self, window, data):
		self.current_terminal.focus()
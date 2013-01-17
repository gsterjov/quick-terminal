import os
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

from gi.repository import Gtk, Vte, GLib, GObject


class Terminal (Gtk.ScrolledWindow):
	__gsignals__ = {
		"exited": (GObject.SIGNAL_RUN_FIRST, None, ()),
		"key-release": (GObject.SIGNAL_RUN_FIRST, None, (int, int)),
	}

	def __init__ (self, config):
		self.config = config

		Gtk.ScrolledWindow.__init__ (self)

		self.opacity = 80

		self.terminal = Vte.Terminal()
		self.terminal.fork_command_full(
			Vte.PtyFlags.DEFAULT,
			os.environ['HOME'],
			['/bin/bash'],
			None,
			GLib.SpawnFlags.DO_NOT_REAP_CHILD,
			None,
			None,
		)

		self.terminal.connect ("key-release-event", self.__on_key_release)
		self.terminal.connect ("child-exited", self.__on_quit)
		self.terminal.set_scrollback_lines (config.scrollback)

		self.terminal.set_opacity (int(config.opacity / 100.0 * 65535))

		self.set_policy (Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.add_with_viewport (self.terminal)
		

	def focus (self):
		self.terminal.grab_focus()
		

	def __on_key_release (self, terminal, event):
		return self.emit ("key-release", event.keyval, event.state)

	def __on_quit (self, terminal):
		self.emit ("exited")
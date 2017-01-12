#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SoundConverter - GNOME application for converting between audio formats.
# Copyright 2004 Lars Wirzenius
# Copyright 2005-2017 Gautier Portet
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

# logging & debugging

from .settings import settings
from gi.repository import GObject

def log(*args):
    """
    Display a message.
    Can be disabled with 'quiet' option
    """
    if not settings['quiet']:
        print(( ' '.join([str(msg) for msg in args]) ))


def debug(*args):
    """
    Display a debug message.
    Only when activated by 'debug' option
    """
    if settings['debug']:
        print(( ' '.join([str(msg) for msg in args]) ))

def idle(func):
    def callback(*args, **kwargs):
        GObject.idle_add(func, *args, **kwargs)
    return callback
# XPCSupport: Support tool for XPC Computers
# Copyright (C) 2017 Xotic PC
#
# This file is part of `xpcsupport`.
#
# `xpcsupport` is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# `xpcsupport` is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with `xpcsupport`; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
Unit tests for `system76driver.products` module.
"""

from unittest import TestCase

from system76driver import actions, products


class TestConstants(TestCase):
    def test_PRODUCTS(self):
        self.assertIsInstance(products.PRODUCTS, dict)
        self.assertEqual(len(products.PRODUCTS), 138)
        for (key, value) in products.PRODUCTS.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)
            self.assertIn('name', value)
            self.assertIsInstance(value['name'], str)
            self.assertTrue(value['name'])

            self.assertIsInstance(value['drivers'], list)
            for action in value['drivers']:
                self.assertTrue(issubclass(action, actions.Action))
                inst = action()
                text = inst.describe()
                self.assertIsInstance(text, str)
                self.assertTrue(text, text)

            if 'screens' in value:
                screens = value['screens']
                self.assertIsInstance(screens, dict)
                for (edid_md5, description) in screens.items():
                    self.assertIsInstance(edid_md5, str)
                    self.assertIsInstance(description, str)

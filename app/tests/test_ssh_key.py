#! /usr/bin/env python
#
# IM - Infrastructure Manager
# Copyright (C) 2011 - GRyCAP - Universitat Politecnica de Valencia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import os
from app.ssh_key import SSHKey


class TestSSHKey(unittest.TestCase):
    """Class to test the SSHKey class."""

    def tearDown(self):
        if os.path.exists('/tmp/ssh.db'):
            os.unlink('/tmp/ssh.db')

    def test_ssh_key(self):
        sshkey = SSHKey("sqlite:///tmp/ssh.db")
        res = sshkey.get_ssh_key("userid")
        self.assertIsNone(res)

        sshkey.write_ssh_key("userid", "ssh-rsa AAAAB3NzaC...")

        res = sshkey.get_ssh_key("userid")
        self.assertEqual(res, "ssh-rsa AAAAB3NzaC...")

        res = sshkey.delete_ssh_key("userid")

        res = sshkey.get_ssh_key("userid")
        self.assertIsNone(res)

    def test_check_ssh_key(self):
        key = ("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD2581vX45pELFhzX7j5f8G3luuKU00IXNYYPm4kWlC/bS8Do73LjJkSdJ/ETEzA"
               "lq99DBqehqmbFPa5OgRBqZmM/W278DimwMe8Alq/0droT9KlrrIetR42Q7ODGQq7+Z0plcy4J8R4HNVLQ4zSACIVXGjBhf9Ruii1R"
               "R139qEzz3v0DlLRdj+p4Y7o4qKkxFvZwVMsXboasGMZQoc1GRAZlNq7sCQr2yUrneh43Id1dRhqEgPWjPzzi9UXUbeXvKsqx0gsGr"
               "+ttuEqy3SM2ZBuhD6xrpAUGrr0TrJBJnVVBKL31zFSu6GcDtVyjoYGJhM/vU9VuBrUHO+qYIrcGP7VaPSOgTSj7V3OLD7pp8kYmFP"
               "vLKleDSI/eiKO0nH/J6W2mGa1J6FDFaIIsLIyERdgakjvrkecfv/YfqPWkUGp1xnzNugkOug1ZMQHfuSs7Ag+kVP3TDPQoAo8u2Yy"
               "EwbLK/vVSFlTe5eaotfCmiltVu3UaPYM8QylCCTW7QCncE= micafer")
        res = SSHKey.check_ssh_key(key.encode())
        self.assertFalse(res)

        key = "ssh-rsa AAAAB3NzaC1yc2EAAAADA..."
        res = SSHKey.check_ssh_key(key.encode())
        self.assertTrue(res)

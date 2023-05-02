# Copyright (C) 2013-2017  Chris Lalancette <clalancette@gmail.com>
# Copyright (C) 2013       Ian McLeod <imcleod@redhat.com>

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

"""
RHEL-8 installation
"""

import os

import oz.OzException
import oz.RedHat
import oz.ozutil


class RHEL8Guest(oz.RedHat.RedHatLinuxCDYumGuest):
    """
    Class for RHEL-8 installation
    """
    def __init__(self, tdl, config, auto, output_disk=None, netdev=None,
                 diskbus=None, macaddress=None, useuefi=True):
        # dnf distro
        oz.RedHat.RedHatLinuxCDYumGuest.__init__(self, tdl, config, auto,
                                                 output_disk, netdev, diskbus,
                                                 True, True, "cpio", macaddress,
                                                 False, useuefi)
        self.virtio_channel_name = 'org.fedoraproject.anaconda.log.0'

    def _modify_iso(self):
        """
        Method to modify the ISO for autoinstallation.
        """
        self._copy_kickstart(os.path.join(self.iso_contents, "ks.cfg"))

        initrdline = "  append initrd=initrd.img ks=cdrom:/dev/cdrom:/ks.cfg"
        if self.tdl.installtype == "url":
            initrdline += " repo=" + self.url
        else:
            # RHEL6 dropped this command line directive due to an Anaconda bug
            # that has since been fixed.  Note that this used to be "method="
            # but that has been deprecated for some time.
            initrdline += " repo=cdrom:/dev/cdrom"
        self._modify_isolinux(initrdline)

    def get_auto_path(self):
        """
        Method to create the correct path to the RHEL 8 kickstart file.
        """
        return oz.ozutil.generate_full_auto_path("RHEL8.auto")


def get_class(tdl, config, auto, output_disk=None, netdev=None, diskbus=None,
              macaddress=None, useuefi=True):
    """
    Factory method for RHEL-8 installs.
    """
    if tdl.update.isdigit():
        if netdev is None:
            netdev = 'virtio'
        if diskbus is None:
            diskbus = 'virtio'
        return RHEL8Guest(tdl, config, auto, output_disk, netdev, diskbus,
                          macaddress, useuefi)


def get_supported_string():
    """
    Return supported versions as a string.
    """
    return "RHEL 8"

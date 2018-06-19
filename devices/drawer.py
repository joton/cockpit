#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright (C) 2018 Mick Phillips <mick.phillips@gmail.com>
##
## This file is part of Cockpit.
##
## Cockpit is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Cockpit is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Cockpit.  If not, see <http://www.gnu.org/licenses/>.

## Copyright 2013, The Regents of University of California
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions
## are met:
##
## 1. Redistributions of source code must retain the above copyright
##   notice, this list of conditions and the following disclaimer.
##
## 2. Redistributions in binary form must reproduce the above copyright
##   notice, this list of conditions and the following disclaimer in
##   the documentation and/or other materials provided with the
##   distribution.
##
## 3. Neither the name of the copyright holder nor the names of its
##   contributors may be used to endorse or promote products derived
##   from this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
## FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
## COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
## INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
## BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
## LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
## CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
## LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
## ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
## POSSIBILITY OF SUCH DAMAGE.


## This Device specifies a "drawer" of optics and filters that determines
# what cameras see what lights.
# Configure it in the config file with type, camera names, and drawer
# configurations, each with one dye and one wavelength per camera.
#
#       [name]
#       type: Drawer
#       cameras: cam1, cam2
#       default: GFP: 525, Cy5: 695
#       TRITC: FITC: 518, TRITC: 600
#

from . import device
from handlers.drawer import DrawerHandler, DrawerSettings
import re

class Drawer(device.Device):
    def __init__(self, name, config):
        device.Device.__init__(self, name, config)

    def parseConfig(self, config=None):
        if config is not None:
            self.config = config
        else:
            config = self.config
        cameras = re.split('[;, ]\s*', config['cameras'])
        settings = []
        for key, item in config.items():
            if key in ['type', 'cameras']:
                continue
            filters = re.split('[,;]\s*', item)
            if filters:
                if len(filters) != len(cameras):
                    raise Exception('Drawer: mismatch between number of cameras and filters.')
                dyes, wls = zip(*[re.split('[:]\s*', f) for f in filters])
                settings.append(DrawerSettings(key, cameras, dyes, wls))
        return settings


    def getHandlers(self):
        # Just return an empty handler for now. It will be configured
        # after the cameras have been initialized.
        settings = self.parseConfig()
        self.handler = DrawerHandler("drawer", "miscellaneous",
                                        settings, 0, None)
        return [self.handler]

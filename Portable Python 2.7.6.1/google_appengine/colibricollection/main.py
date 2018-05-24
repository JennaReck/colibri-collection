#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

from Front import *
from Hum import *
from Sort import *
from Find import *
from Compare import *
from ScaleCalibration import *
from Checklist import *
from Favorites import *
from Slideshow import *
from Resources import *
from NameMatch import *
from SearchResults import *
from Random import *
from AdminPanel import *
from UploadHum import *
from UploadResources import *
from Login import *
from Error404 import *
from ColorGen import *
from ScaleGen import *
from Videos import *
from UploadVideos import *
from About import *

page_re = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
num_re = r'(/[0-9]+/?)'
all_else = r'(?s).*'

app = webapp2.WSGIApplication([
    ('/', Front),
    ('/species' + num_re + page_re, Hum),
    ('/index', Sort),
    ('/find', Find),
    ('/compare', Compare),
    ('/calibrate', ScaleCalibration),
    ('/checklist', Checklist),
    ('/favorites', Favorites),
    ('/slideshow', Slideshow),
    ('/other-resources', Resources),
    ('/name-match', NameMatch),
    ('/search', SearchResults),
    ('/random', Random),
    ('/admin-panel', AdminPanel),
    ('/upload-hum', UploadHum),
    ('/upload-resources', UploadResources),
    ('/login', Login),
    ('/logout', Logout),
    ('/404', Error404),
    ('/color-gen', ColorGen),
    ('/scale-gen', ScaleGen),
    ('/videos', Videos),
    ('/upload-videos', UploadVideos),
    ('/about', About),
    ('/' + all_else, Error404)
], debug=True)
app.error_handlers[404] = handle_404

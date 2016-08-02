#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import collections
import io
import math
import os
import pickle
import sys
import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.ttk as ttk
import xml.etree.ElementTree as ET
import zipfile
import tempfile
import shutil
import base64

from PIL import ImageTk, Image, ImageOps


HomeFolder = os.path.expanduser("~")
ConfigFile = os.path.join(HomeFolder, 'HDView.pkl')


HDViewerIcon = 'R0lGODlhIAAgAIYAAAABAAACAAIFAQcJBQoMCAwPCw8RDhIUERcYFhocGRwdGx0fHB8gHiAhHyIjISQlIyYnJSkrKC4vLTAyLzM0MjQ2Mzo7OTw+Oz9APkFCQENFQkRGQ0hKR0xOS05QTVNUUlVWVFZYVVlbWF1fXWBiX2NlYmZnZW1vbG9xbnN1cnV3dHZ4dXp8eYuNioyOi42PjI+RjpKUkZWXlJeZlp6gnaKkoaSmo7W3tLm7uL7BvcTGw8jKx8rMyczOy87QzNTW09vd2t/h3uPl4eXn5Ors6e/x7vL08fP18vT38/b49fn7+Pv9+v7//AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAgACAAQAj/AAEIHEiwoMGDCAEMCDDiB5OHECNGLNLiQAAWADJmTBHgApOPIEOKHAlSRgAAKFOiDGCihgEOAGLKnEmzps2bOHMGQMGkp8+fQIP65BEAgNGjKQgEILCEidOnUJ8KcdEgQAEAWLNq3cq1q9evYMOGBTEgQIABEDB08LBhgoEAAQRwAEC3rl0AASIMYcK3r9+/f5ecCACgMAAJAXYwWcy4sePHjR98AECZhYAAM5ho3sy5c+cfDQIAGE2adIUASJi0CMC6tesACEoAmE27Nu0BDUoA2M27t+/fwIMLH068uPHjyImv4ADBwIABBRxkOAGguvXr2KtjCBDAQoseSZiIxx+/JIgNEQQCTADAvn17FQEY6GBCv779+/WJfAhAAoB/gAAAHBgAhMlBhAkVLmSyRMMAABEzBMDBxOJFjBk1YkQAAgCACwFqMCFZ0uRJlCWNDBABwOWBADGYzKRZ0+ZNJkAOIADQsyeJAAFCCGFS1OhRpEyUwCAQAMBTqFEVBCjC5EiJFzd8AAHyIwcNFBUCBBDwAcBZtGnPLkjAhMcADRwkMEiQwAGFDwD07uXbV6+HAAQEnABQ2PBhxIkVL2bc2PFjyJEhBwQAOw=='
AutoColors = 'R0lGODlhCwALAIUAAAD//y1psSZruTdoqSpuuiVxxEFuqDVyuh1300Rxqip3yUR1skd3syR+2Dh8xkx5skF9wTyAyj2AyVR8sD+ByCyF3UmBw0GFz0SFzFmEuzWN41yGvGKKvk+O0kqQ2VKQ0z6U6XaMqnSNrHePrVCX4Eec7l2c3YmYq1Cj84yZqmOi41eq+HWs5IG264676ZG+7JK/7JbC7pHE9ZrG8Z/K9JrM+6PO96fQ+ajR+avV/AAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAALAAsAAAh4AAEA2GDhQwcLGQAoBMBARY0cK1aQWAAAAAcTN3DgQMHRwwQAEGTYGFmiZAkIADDQWEkDhEsQEkZQmEFzhoabGhyIONAihs8KQCscOPHgwgsYMBooVZAAAIABEVi4QICgwIAUALIaCEBAQAADAMKKBRAiBICzZwMCADs='
FileFullDesktop = 'R0lGODdhDgALAIAAAGZmZvDw8CwAAAAADgALAAAIYgABCBxIsGCAgwgTHgQAIAAAAAEiSgQAIAAAAAEABNjIcSOAAAAABBhJsuRIAAACqFzJUiUAAAFiypwZEwCAAAAC6NypE0AAAAACAAAQoKhRAAACAAAQoKnTp00BSJ1KtWpAADs='
FileFullScreen = 'R0lGODdhDgALAIUAACZSkyhXmC5bnTRfoTtlqEhop0BtsDJ11yl73UZ3ujSD3lOCxjyH41qJzkCR6WKQ1WOX3F6d52qh5mSj7nq9+6fG7ZbK/sHGycbLzpvT/6XY/6fe/tXa3Nne4eXr7erv8u/x7u3z9fX6/f3//AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAADgALAAAIfAArTJggYYLBgxMkSKgwYYPDDRoiashA0QKECBQcOGDAkYECBCAPPIAwoqTJkyUbQBjBsqVLlg0ejBghoqbNmwsaiPgA4oNPnx6CekiwQESHo0g7cFjKwUCCDxiiSr1AlSoBAyFAgAjBNQSIEGBBCCgwYICAs2cDqAXANiAAOw=='
FileOpen = 'R0lGODdhDgALAIYAANiGLNiHLdiILdmOM9qUNdqYNdqaNtqfNdqhNtqkNdqmN9qqNtqrNdqrNtquNNqvNdqvNtmxMtiyLNizLNqzNtm0NNu2POHCXuLDX+LDYOnBc+PHa+THa/DLJvHNLuXKdPHOMO3KaurLbObNefLQOfLRO/HPae7Pcu7PdvPTRPPTR+7OiPHQbO/QevPUSfHScu/SgPTWT/LTee/ThfTXVPTXV/LUf/TYXPLVge/UlPXZXfPXhvXaY/XbZfXbaPPYjvbcbPPalvbecvbedvTck/TbnvbfdvXekfbgfPXelPTdp/fhgffihfXgn/fjhffji/bhrPjkjvjlkfjmlPjmlfnonPnpofnppPbpyfjqwvrsrPrts/vvufrw3PvyyvzyyPvyzPzz0Pz01/z22Pv26Pv36fv36v368f767/368v777v777/788P788f788v788/789v789//89f799P/99v/9+P/9+v7+/f/+/f/+/v///gAAAAAAAAAAAAAAAAAAACwAAAAADgALAAAIpwArXMhAEIMFCQgRTphA4Y6ePHj0mOGwoeKIDxEexIlypAmUNXPetFmjxg6EBWeSEMERQsQMGC1QnCjjgAGZHCs0YHHzxg2bNWr0NFCgpw4dOW/GTHFixMcNMQkQwPnCRUuVJ0iA6IiRIswBA2m2XKHCZEiPGi5KgABTgAAaK1KWCOFBQwUJDx28EBjQRUmRID922JDxgoWJLAMACAggoLHjxgEEAAgIADs='
FileSave = 'R0lGODlhDgAOAIUAAAAAAB9rvhhtxhltxRptxBJvzSBxxzxsqR9yykRupURvpklyqCl6zk10qCh70E12qk52qVF4qlN6rDSD1FZ9rjOF11l+rlWAt19/qFeBuFmDuVqDuVuFu2CFtUCN21+IvUuO0kCQ32KKvmWNwEuW41SV12uRw0yZ52WVyGOb01Se6FWg64WkzYSmyY2r0XWy74Sz45ezzpq10Z241I276Za635fF8ZnG86DM98/Pz9LS0tfX1+7u7vPz8/j4+Pz8/CH5BAEAAAAALAAAAAAOAA4AAAioAFmYGEiw4EAXI1a8uMGwIcMXKjqIOIHjh8WLFnGQsPAhhA0fIEOCtOGBAocKNHqoXKmSxgQJGhzA4EGzJk0YDCJkQFCihs+fPksYgHBBQIGjSJMSaHBBQAEQKaJKBVGAQIMLAgrM2MF1BwgQMwoQaHBBQAEZOtLqKFBARgECDTYEKBAjh90cBQrEKECgAYADAVC0GEwYxQACDQAAeLCgsYIECyJHxhAQADs='
OverHeight = 'R0lGODlhCAAOAIUAAD0KJDFlqDNnpzhpqDlpqBdxzi5vuSFyyD1urRt20jBzvzBzwElzqCB71kZ2tEZ3s0d3skd3tEl5tVJ6r1B+uFeBtV+AqliBtVqBs0iFykaHzVuEul2Gu2qIrmyKsmqRw4WWrVSf6Xydx4CexFOn9lms+YelzF2v+4inzwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAIAA4AAAhnAAEAoODAAQUAAFB8iHDixAMMKABICFGiRAgIADJmIEEiAwgAIEdo0NABgEmTFyYAWMmypcuXADhsAECTpgkFCzwA2AnAQIMGBgAIRXAgQYIDBACIqCCgQAEBDCwAADAgQIABAAAEBAA7'
OverWidth = 'R0lGODlhDgAIAIUAAAAAADpqqT1tqzJyvEBwrTF0v0Jyr0Nyr0V1sUh2sSx8zzd6xEh3s0h3tE14rEp5tUt5tFd7qT6AyFl9rEOBxliAtESEyjSK3mWDqjSM4l2GumuGqmGKvj+S5WyKsj+V6UeU4YGTqnWXxHmcyICdw4ypz5Csz5m01QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAOAAgAAAhpAAGcAECwoMETAACMaACgocOGD0QAgGABBAUSADICKEEBhIUEDDp8+CChAgAAHCR8+NDhAIILGTIscAAAgIYFGTJcIGCggIIBGAAIBeBhgIICAgBMCBACgNOnAAJEAADABICrWLNuABAQADs='
ReadFirst = 'R0lGODlhCwALAIYAAK5tRKpbBKpjFKpkFKtnCKpnFKprFKtrGa1tCcxlAdFkAapuFKpuFqpwFNFnAdtmAapzFLpxANtqAdFuAap5FK17Cap9FK15PKp6RttzAap7RvRsAqp9RtF5AfFwAqqARvRxAraBJKqCRqqFRtt+AbKIHN1/AdGEAaqJRvR8AraNJLqSAK+QS/+BAtuMAd2NAdGRAbGUbfSMArGWbcyZAduaAbqZc9GeAf+SAsahVLGkfPSeAdGpANupAf+mAcuvZ9u3APSxAf+7AfHBAfTFAfTWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAALAAsAAAh1AFesKAGgoEEVP3gUsQCgYcMKQFjcIEIBgMUcNIb0QAEjCAQAAELAECKkxogTOxrMQPDCh0sXIjrIMBCDgAkcOEl8mJCiAAAABya0aJGBgwMQAwAovZDAgwQNCjYIAEAVgI0ADzBEiLAAgNevDEQAGEu2rI6AADs='
ReadLast = 'R0lGODlhDAAKAIYAAMHQSKpbBKplBqpqBqlpGMxlAdFkAa9uGtFnAbRtHrRuHttmAa9xGrpxAK5zG9tqAal0OKp5BtFuAa15HLR4HrR5HttzAfRsArR+HtF5AfFwAvRxArSDHtt+AbSHHt1/AauFW7KJIKuGW9GEAbSKHquIW/R8AquIY6uJW6uLW7qSAKuOW6yPaP+BAquRW9uMAauSW92NAdGRAcuYAfSMAruWSduaAdGeAf+SAs2dac2eafSeAdGpAM2gadupAc2jac2lac2mac2paf+mAc2sac2vadu3AM2xafSxAc23fu6/Af+7AfTFAfTWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAMAAoAAAh7AI+EAECwIAkVKpIUMRIBgEOHHprwgEHEh5IZNQBo5MDkhgshNpYskTEBAAAMSGSsCPJiiMsYAwBU2DEixY8OOHJ+EMCCAY0MKHpYaNFCAgEAAA6YkFBCxwMNBSAAmKpgAwIRORYEOAGgK4AEFwyAAOIAgNmzFBo0SBEQADs='
ReadNext = 'R0lGODlhCAAKAIUAAAAAAKpeCqpoDMNjAaxvENdlAalwJs5tAa53Jqt8DeZtAupuAqp+TNZ8Ab6APOp5Ar6BPLSFMr6EPL6HPNWHAcKNAL6KPL6LPM2NAfuAAuqGArWRMv+BAr6PPKqSd76TPL6XPL6aPLCafuqXAf+SAuqoAcWpbNawAP+mAeW0Aeq6Afm2Af+7AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAIAAoAAAhOAENsAECwIIgTCQAoVPhBRYoKJgBI7FCCxQoMEQAAuDAChUcKBABM0ECiZAMBIiQ84JDhgAEAACAsUDCAAYCbDgoE8ACgJwALCAAIHRoQADs='
ReadPrevious = 'R0lGODlhBwALAIUAAAAAAKpeCsNjAa5rEKltKNdlAalwKKxyKKlzKKp0I85tAbF0Fal1KKl3KKl7KOZtAupuAql/KLCAEtZ8Aep5Aq+ILbOHVdWHAcKNAM2NAfuAAuqGAv+BAr6PPL2YOb6aPOqXAf+SArSkd+qoAdawAP+mAeW0AdK0eOq6Afm2Af+7AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAHAAsAAAhNAAEIFOjhA4CDACSQqAAAwAkMJlBEANAhQwoVIxwsuFCiI4gGAyaEGLkBAYADCjRwoGAAAAALAh5AIACgJoAABQgA2LkzAQMAQIOKCAgAOw=='
RotateLeft = 'R0lGODlhDAALAIUAAAAAADJmqC5qsjFttCVwwTRvtht20yp0xDdyuEFyr0Nyri94xyJ81z53ujR9ykp5tDt8xE55rjt9x0t6timC2z9/xzuCzkOBxkCDy0eCxkeEyUCG0ECG0TGJ4FuCs2OCqGSCqWWDqmaEqmeFq2iGrGmHrDqR5kGQ32mJsUuP10uQ2UeR3GOMv0eU4U+T2naNrEKX6kKY63aPrU6Z5U6a5n6TrEqf8H6bwVKl9Y2r0I6r0ZSw1AAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAMAAsAAAh1AAEIZAGgoMGDE1x4uKFjB4CHAHJomIGDhgoVKTI8AADgQgsbIEPaWJEAAAAFG2BwaNCgwokYGGQAABBBQgkAAGpAMGGBBICfKF4AGIqgg4MRAJIqTVqAwgIRAKJKjTqAwYEQALJqzSrAAAEQAMKKDRug7IeAADs='
RotateRight = 'R0lGODlhDQALAIUAAAAAADJmqC5qsjFttCVwwTRvtht20yp0xDdyuEJysENyri94xyJ81z53ukh3s0x3rTR9ykp5tTt8xDt9xymC2z9/xzuCzkOBxkCDy0eCxkeEyUCG0ECG0TGJ4GmHrGCJvDqR5kGQ30uP10uQ2UeR3EeU4U+T2kKX6kKY62qRw3GRuE6Z5U6a5n6TrEqf8IWWrFKl9YOgxYaly4elzI+lwIimzYmnzYqozoupz46r0ZSw1JiwzgAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAANAAsAAAh6AAEIHCjwA4CDCA/qyJEjhQkHACJGjJBBxIgRLGCs0BADAIAEJFyIHOmixAUaADCgCFGhQQMOJzYoeAEAhwUQEloAAOBhwgMAQG9A6IAAgNEdKgAoBWBjAYUCAKJKlVrjAIMBALJq1TqDgAEBAMKKFSsjgFkAaNOmDQgAOw=='
UnderHeight = 'R0lGODlhCAAMAIUAAMJMoyhuvDprqzpsqztsrCxwvDxurUFuqEBwrT9xr0NyrkRzrkZzrCB71kV0sEV1sSp80kh4tCeA2lN7rlt8qS6G3EiFyTaL32eGrWeHr02M0WGJvE2N0j6R5GWNwGuMuWiPwkqW4XmPq0WZ7HORtk2h8VOn9oSkzIemzY6s0QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAIAAwAAAhhAAEIBOEBgEGDKTRwIAGgIQALJkxYAEAxQogSJUI4AHBiQ4IRIxJMyAAAwIIOHRQAWAngwYULCADIRGGgQgUCGAAAGABBggQIAgAILdCgQQERAJJ+CBCAAoCnTxkcAEA1IAA7'
UnderWidth = 'R0lGODlhDAAIAIUAACAAVDhqqjhrrEJzsjR2wEd0rEp5tTt+yEx7tjt/yS+C11d7qS6D2Fl9q1J+tkKDykKDy0eDx0eEyVuCtV+Cr0iHzWWDql6HvTqR5TqR5nSMq06Y40aa7E6Z5Uab7Eab7XaZxYSbuXudyYaixoelzI2r0J+42AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAMAAgAAAhgAAEIBGACAAATABIqBIAABAAAIgwAmAighIQOFQYMqLAhwggAFyB8GOnBw4cPHB5McHAgg0sMGDLITFAAAAUCCggIEECAAYEGAIKGCLAAAIAFATQAWMrUAgAAJABIBRAQADs='
ZoomIn = 'R0lGODlhDQANAIYAAAAAADZoqShtvDlqqztsrDNutCtwvT1urC9zvy50wURxqjV1vjJ2wh961UV2szt4vkh4tCV/2VB3qy1/01F6rVB8tDKC0yyE3S6E2ld9rEWAxFd9rlV+sTGF2kqCw0CHz12CsUGI0GCDsVqFvEuJzV2HvUuNz0+Mz0+N0FKNzU2P0WOMv0+T2EyU3FeS0FaS1XeOqnaOrXiQrVWZ3YiXqomXqoqZrF+i5Wqh2Gqo5XKo4myt7Xau53az7qu+0rLAz7TBz7vM3dLT1NTU1NTa4dvb29ve4dDg8dff5+Dk6Nvr++Ht+uPu+vDw8PT19vb29gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAANAA0AAAipAAEAKOHhxQsPIwAoXAiBhxImS5TwcACgIoAVOpw86bHjiRMdHACI1HCkSZMcN5o0OaIBgEsUSVq06IChRQskJ2QAAEDCCA4cFibgwEGERAwAAB4EKVJERYgiRYI8sAEAQAUXQoaY+DBEyIwDAMICIJDCB5AfPlhcYJABgFsACgosWFBgQIIICEAA2LsXBgwAACQYaGBABIDDiBFTEBCgBoDHkCNvoAEgIAA7'
ZoomOut = 'R0lGODlhDQANAIYAAAAAADZoqShtvDlqqztsrDNutCtwvT1urC9zvy50wURxqjV1vjJ2wh961UV2szt4vkh4tCV/2VB3q1F6rVB8tCyE3Vd9rEWAxFd9rlV+sUqCw12CsWCDsVqFvEuJzV2HvU+Mz0+N0FKNzWOMv0+T2EyU3FeS0FaS1XeOqnaOrXiQrVWZ3YiXqomXqoqZrGqh2HKo4nau56u+0rvM3c/Pz9LT1NTU1NTa4dvb29ve4dDg8dff5+Dk6Nvr+/Dw8PT19vb29vv7+wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAANAA0AAAiZAAEA+KDhxAkNHQAoXAghRo8gQXrEcACgIoARMH4A2QjkB4wMAEJe0OGjpEkdFwCoDMGjhMuXO0CoAADAQ44XOHPe8JACAIAHM3AIHTrjgQsAACiYqGGjqY0aKw4AmAqAgAgZNGjIIFGBgQUAYAEoKLBgQYEBCSIg2ACgbVsUKAAAkGCggQEOAPLq1TtBQIAWAAILHoyBBYCAADs='


class Doujinshi:
    def __init__(self):
        self.comic_file_path = None

        self.loaded = False
        self.title = ''
        self.pages = []
        self.comic_info = None

    def load_comic(self, comic_file_path, progress, display_page):
        self.loaded = False
        self.comic_file_path = comic_file_path
        self.title = self.comic_file_path
        self.pages = []
        self.comic_info = None

        with zipfile.ZipFile(self.comic_file_path, 'r') as zipread:
            file_list = zipread.namelist()

            progress['maximum'] = len(file_list)
            progress['value'] = 0
            first_page = True

            if 'ComicInfo.xml' in file_list:
                data = zipread.read('ComicInfo.xml')
                self.comic_info = ET.fromstring(data)
                self.title = self.comic_info.find('Title').text

            for filename in file_list:
                progress['value'] += 1
                progress.update()
                _, ext = os.path.splitext(filename.lower())
                if ext == '.xml':
                    pass
                    data = zipread.read(filename)
                    self.comic_info = ET.fromstring(data)
                    self.title = self.comic_info.find('Title').text
                else:
                    data = zipread.read(filename)
                    dataEnc = io.BytesIO(data)
                    try:
                        self.pages.append(Image.open(dataEnc))
                        if first_page:
                            first_page = False
                            display_page()
                    except OSError:
                        pass

        self.loaded = True

    def save_comic(self, progress):
        self.loaded = False

        temp_dir = tempfile.mkdtemp()
        try:
            temp_name = os.path.join(temp_dir, 'temp.zip')
            with zipfile.ZipFile(self.comic_file_path, 'r') as zipread:
                with zipfile.ZipFile(temp_name, 'w', zipfile.ZIP_LZMA) as zipwrite:
                    progress['maximum'] = len(zipread.infolist())
                    progress['value'] = 0

                    for item in zipread.infolist():
                        progress['value'] += 1
                        progress.update()

                        if item.filename != 'ComicInfo.xml':
                            data = zipread.read(item.filename)
                            zipwrite.writestr(item, data)

                    data = ET.tostring(self.comic_info, encoding='unicode')
                    zipwrite.writestr('ComicInfo.xml', data)

            shutil.move(temp_name, self.comic_file_path)
        finally:
            shutil.rmtree(temp_dir)

        self.loaded = True

    def is_loaded(self):
        return self.loaded

    def get_title(self):
        return self.title

    def get_nb_pages(self):
        return len(self.pages)

    def get_page_image(self, page_num):
        image = self.pages[page_num - 1]
        try:
            image = image.convert('RGB')
        except OSError:
            pass
        if self.comic_info is not None:
            angle = self.get_page_rotation(page_num)
            if angle != 0:
                image = image.rotate(angle, expand=True)
        return image

    def create_page(self, page_num):
        pages = self.comic_info.find('Pages')
        if pages is None:
            pages = ET.SubElement(self.comic_info, 'Pages')
        page = pages.find("Page[@Image='{0:d}']".format(page_num))
        if page is None:
            page = ET.SubElement(pages, 'Page')
            page.set('Image', str(page_num))
        return page

    def get_page_rotation(self, page_num):
        rot = self.comic_info.find("Pages/Page[@Image='{0:d}']/Rotate".format(page_num))
        if rot is None:
            return 0
        else:
            return int(rot.text)

    def set_page_rotation(self, page_num, angle):
        page = self.create_page(page_num)
        rot = page.find('Rotate')
        if rot is None:
            rot = ET.SubElement(page, 'Rotate')
        rot.text = str(angle)

    def get_page_type(self, page_num):
        node = self.comic_info.find("Pages/Page[@Image='{0:d}']".format(page_num))
        if node is None or 'Type' not in node.attrib:
            return 'Story'
        else:
            return node.attrib['Type']


class HDViewer(tk.Tk):
    def __init__(self, comic_file_path=''):
        tk.Tk.__init__(self)
        self.title('HDoujinshi viewer')

        self.doujinshi = Doujinshi()
        self.current_page = -1

        self.params = {'width': 600, 'height': 800, 'win_x': 0, 'win_y': 0, 'scroll_speed': 200, 'scroll_next': 1,
                       'bg_color': '#404040', 'bg_auto_color': True,
                       'portrait_under_height': False, 'portrait_over_height': False,
                       'portrait_under_width': True, 'portrait_over_width': True,
                       'landscape_under_height': True, 'landscape_over_height': True,
                       'landscape_under_width': False, 'landscape_over_width': False, 'auto_colors': True}
        self.load_config()

        self.portrait_under_height = tk.BooleanVar()
        self.portrait_over_height = tk.BooleanVar()
        self.portrait_under_width = tk.BooleanVar()
        self.portrait_over_width = tk.BooleanVar()
        self.landscape_under_height = tk.BooleanVar()
        self.landscape_over_height = tk.BooleanVar()
        self.landscape_under_width = tk.BooleanVar()
        self.landscape_over_width = tk.BooleanVar()
        self.auto_colors = tk.BooleanVar()
        self.bg_auto_color = tk.BooleanVar()
        self.portrait_under_height.set(self.params['portrait_under_height'])
        self.portrait_over_height.set(self.params['portrait_over_height'])
        self.portrait_under_width.set(self.params['portrait_under_width'])
        self.portrait_over_width.set(self.params['portrait_over_width'])
        self.landscape_under_height.set(self.params['landscape_under_height'])
        self.landscape_over_height.set(self.params['landscape_over_height'])
        self.landscape_under_width.set(self.params['landscape_under_width'])
        self.landscape_over_width.set(self.params['landscape_over_width'])
        self.auto_colors.set(self.params['auto_colors'])
        self.bg_auto_color.set(self.params['bg_auto_color'])
        self.portrait_under_height.trace('w', self.update_params)
        self.portrait_over_height.trace('w', self.update_params)
        self.portrait_under_width.trace('w', self.update_params)
        self.portrait_over_width.trace('w', self.update_params)
        self.landscape_under_height.trace('w', self.update_params)
        self.landscape_over_height.trace('w', self.update_params)
        self.landscape_under_width.trace('w', self.update_params)
        self.landscape_over_width.trace('w', self.update_params)
        self.auto_colors.trace('w', self.update_params)
        self.bg_auto_color.trace('w', self.update_params)

        self.geometry('{0:d}x{1:d}+{2:d}+{3:d}'.format(self.params['width'], self.params['height'],
                                                       self.params['win_x'], self.params['win_y']))

        self.full_screen = False
        self.full_desktop = False

        self.file_operation = False

        self.hdviewer_image = ImageTk.PhotoImage(data=base64.b64decode(HDViewerIcon))
        self.file_open_image = ImageTk.PhotoImage(data=base64.b64decode(FileOpen))
        self.file_save_image = ImageTk.PhotoImage(data=base64.b64decode(FileSave))
        self.file_full_screen_image = ImageTk.PhotoImage(data=base64.b64decode(FileFullScreen))
        self.file_full_desktop_image = ImageTk.PhotoImage(data=base64.b64decode(FileFullDesktop))
        self.read_first_image = ImageTk.PhotoImage(data=base64.b64decode(ReadFirst))
        self.read_last_image = ImageTk.PhotoImage(data=base64.b64decode(ReadLast))
        self.read_next_image = ImageTk.PhotoImage(data=base64.b64decode(ReadNext))
        self.read_previous_image = ImageTk.PhotoImage(data=base64.b64decode(ReadPrevious))
        self.zoom_in_image = ImageTk.PhotoImage(data=base64.b64decode(ZoomIn))
        self.zoom_out_image = ImageTk.PhotoImage(data=base64.b64decode(ZoomOut))
        self.rotate_left_image = ImageTk.PhotoImage(data=base64.b64decode(RotateLeft))
        self.rotate_right_image = ImageTk.PhotoImage(data=base64.b64decode(RotateRight))
        self.under_height_image = ImageTk.PhotoImage(data=base64.b64decode(UnderHeight))
        self.under_width_image = ImageTk.PhotoImage(data=base64.b64decode(UnderWidth))
        self.over_height_image = ImageTk.PhotoImage(data=base64.b64decode(OverHeight))
        self.over_width_image = ImageTk.PhotoImage(data=base64.b64decode(OverWidth))
        self.auto_colors_image = ImageTk.PhotoImage(data=base64.b64decode(AutoColors))

        self.iconphoto(True, self.hdviewer_image)

        self.file_menu = None
        self.read_menu = None
        self.option_menu = None
        self.help_menu = None
        self.toolbar = None

        self.button_file = None
        self.button_read = None
        self.button_option = None
        self.button_help = None

        self.button_load = None
        self.button_first = None
        self.button_previous = None
        self.button_next = None
        self.button_last = None
        self.button_auto_colors = None

        self.toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas = tk.Canvas(self, width=self.params['width'], height=self.params['height'])
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.create_menu()
        self.check_menu()

        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.bind('<Configure>', self.window_resize)
        self.canvas.bind('<Button-1>', self.mouse_down)
        self.canvas.bind('<B1-Motion>', self.mouse_move)
        self.canvas.bind('<MouseWheel>', self.mouse_wheel)

        self.scroll_attempts = self.params['scroll_next']

        self.last_x = 0
        self.last_y = 0
        self.tkImage_id = None
        self.tkImage = None
        self.zoom = 1.0

        self.timer = None

        if comic_file_path:
            self.load_comic(comic_file_path)

    def load_config(self):
        try:
            params = pickle.load(open(ConfigFile, 'rb'))
            self.params.update(params)
        except FileNotFoundError:
            pass

    def save_config(self):
        pickle.dump(self.params, open(ConfigFile, 'wb'), pickle.HIGHEST_PROTOCOL)

    def update_params(self, *args):
        self.params['portrait_under_height'] = self.portrait_under_height.get()
        self.params['portrait_over_height'] = self.portrait_over_height.get()
        self.params['portrait_under_width'] = self.portrait_under_width.get()
        self.params['portrait_over_width'] = self.portrait_over_width.get()
        self.params['landscape_under_height'] = self.landscape_under_height.get()
        self.params['landscape_over_height'] = self.landscape_over_height.get()
        self.params['landscape_under_width'] = self.landscape_under_width.get()
        self.params['landscape_over_width'] = self.landscape_over_width.get()
        self.params['auto_colors'] = self.auto_colors.get()
        self.params['bg_auto_color'] = self.bg_auto_color.get()
        self.show_current_page()

    def create_menu(self):
        self.button_file = tk.Menubutton(self.toolbar, text='File', underline=0, takefocus=True)
        self.button_file.pack(side=tk.LEFT, padx=2, pady=2)
        self.button_read = tk.Menubutton(self.toolbar, text='Read', underline=0, takefocus=True)
        self.button_read.pack(side=tk.LEFT, padx=2, pady=2)
        self.button_option = tk.Menubutton(self.toolbar, text='Options', underline=0, takefocus=True)
        self.button_option.pack(side=tk.LEFT, padx=2, pady=2)
        self.button_help = tk.Menubutton(self.toolbar, text='Help', underline=0, takefocus=True)
        self.button_help.pack(side=tk.LEFT, padx=2, pady=2)

        self.button_load = tk.Button(self.toolbar, command=self.menu_file_open, image=self.file_open_image, relief=tk.FLAT, takefocus=True)
        self.button_load.pack(side=tk.LEFT, padx=2, pady=2)
        self.button_first = tk.Button(self.toolbar, command=self.menu_read_first, image=self.read_first_image, relief=tk.FLAT, takefocus=True)
        self.button_first.pack(side=tk.LEFT, padx=2, pady=2)
        self.button_previous = tk.Button(self.toolbar, command=self.menu_read_previous, image=self.read_previous_image, relief=tk.FLAT, takefocus=True)
        self.button_previous.pack(side=tk.LEFT, padx=2, pady=2)
        self.button_next = tk.Button(self.toolbar, command=self.menu_read_next, image=self.read_next_image, relief=tk.FLAT, takefocus=True)
        self.button_next.pack(side=tk.LEFT, padx=2, pady=2)
        self.button_last = tk.Button(self.toolbar, command=self.menu_read_last, image=self.read_last_image, relief=tk.FLAT, takefocus=True)
        self.button_last.pack(side=tk.LEFT, padx=2, pady=2)
        self.button_auto_colors = tk.Button(self.toolbar, command=self.menu_auto_colors, image=self.auto_colors_image, relief=tk.FLAT, takefocus=True)
        self.button_auto_colors.pack(side=tk.LEFT, padx=2, pady=2)

        self.file_menu = tk.Menu(self.button_file, tearoff=False)
        self.read_menu = tk.Menu(self.button_read, tearoff=False)
        self.option_menu = tk.Menu(self.button_option, tearoff=False)
        self.help_menu = tk.Menu(self.button_help, tearoff=False)

        self.button_file.config(menu=self.file_menu)
        self.button_read.config(menu=self.read_menu)
        self.button_option.config(menu=self.option_menu)
        self.button_help.config(menu=self.help_menu)

        self.file_menu.add_command(label='Open...', underline=0, image=self.file_open_image, compound=tk.LEFT, command=self.menu_file_open, accelerator='Ctrl+O')
        self.file_menu.add_command(label='Save Comic', underline=0, image=self.file_save_image, compound=tk.LEFT, command=self.menu_file_save, accelerator='Ctrl+S')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Full Screen', underline=5, image=self.file_full_screen_image, compound=tk.LEFT, command=self.menu_file_full_screen, accelerator='F11')
        self.file_menu.add_command(label='Full Desktop', underline=5, image=self.file_full_desktop_image, compound=tk.LEFT, command=self.menu_file_full_desktop, accelerator='F12')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', underline=1, command=self.menu_file_exit, accelerator='Alt+F4')

        self.read_menu.add_command(label='First Page', underline=0, image=self.read_first_image, compound=tk.LEFT, command=self.menu_read_first, accelerator='Home')
        self.read_menu.add_command(label='Last Page', underline=1, image=self.read_last_image, compound=tk.LEFT, command=self.menu_read_last, accelerator='End')
        self.read_menu.add_command(label='Next Page', underline=0, image=self.read_next_image, compound=tk.LEFT, command=self.menu_read_next, accelerator='PgDn')
        self.read_menu.add_command(label='Previous Page', underline=0, image=self.read_previous_image, compound=tk.LEFT, command=self.menu_read_previous, accelerator='PgUp')
        self.read_menu.add_separator()
        self.read_menu.add_command(label='Scroll Up', underline=7, command=self.menu_read_up, accelerator='Up')
        self.read_menu.add_command(label='Scroll Down', underline=7, command=self.menu_read_down, accelerator='Down')
        self.read_menu.add_command(label='Scroll Left', underline=7, command=self.menu_read_left, accelerator='Left')
        self.read_menu.add_command(label='Scroll Right', underline=7, command=self.menu_read_right, accelerator='Right')

        zoom_menu = tk.Menu(self.option_menu, tearoff=False)
        self.option_menu.add_cascade(label='Zoom', underline=0, image=self.zoom_in_image, compound=tk.LEFT, menu=zoom_menu)
        zoom_menu.add_command(label='Zoom In', underline=5, image=self.zoom_in_image, compound=tk.LEFT, command=self.menu_zoom_in, accelerator='Ctrl++')
        zoom_menu.add_command(label='Zoom Out', underline=5, image=self.zoom_out_image, compound=tk.LEFT, command=self.menu_zoom_out, accelerator='Ctrl+-')
        zoom_menu.add_command(label='Zoom 100%', underline=5, command=lambda: self.menu_zoom(1.0), accelerator='Ctrl+0')
        zoom_menu.add_command(label='Zoom 125%', underline=5, command=lambda: self.menu_zoom(1.25))
        zoom_menu.add_command(label='Zoom 150%', underline=5, command=lambda: self.menu_zoom(1.5))
        zoom_menu.add_command(label='Zoom 200%', underline=5, command=lambda: self.menu_zoom(2.0))
        zoom_menu.add_command(label='Zoom 400%', underline=5, command=lambda: self.menu_zoom(4.0))
        rotate_menu = tk.Menu(self.option_menu, tearoff=False)
        self.option_menu.add_cascade(label='Rotate', underline=0, menu=rotate_menu)
        rotate_menu.add_command(label='Left', underline=0, image=self.rotate_left_image, compound=tk.LEFT, command=self.menu_rotate_left)
        rotate_menu.add_command(label='Right', underline=0, image=self.rotate_right_image, compound=tk.LEFT, command=self.menu_rotate_right)
        rotate_menu.add_command(label='Reset', underline=1, command=self.menu_rotate_reset)
        rotate_all_menu = tk.Menu(self.option_menu, tearoff=False)
        self.option_menu.add_cascade(label='Rotate All', underline=1, menu=rotate_all_menu)
        rotate_all_menu.add_command(label='Left', underline=0, image=self.rotate_left_image, compound=tk.LEFT, command=self.menu_rotate_all_left)
        rotate_all_menu.add_command(label='Right', underline=0, image=self.rotate_right_image, compound=tk.LEFT, command=self.menu_rotate_all_right)
        rotate_all_menu.add_command(label='Reset', underline=1, command=self.menu_rotate_all_reset)
        fit_portrait_menu = tk.Menu(self.option_menu, tearoff=False)
        self.option_menu.add_cascade(label='Fit Portrait', underline=4, menu=fit_portrait_menu)
        fit_portrait_menu.add_checkbutton(label='Under Height', underline=0, image=self.under_height_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.portrait_under_height)
        fit_portrait_menu.add_checkbutton(label='Under Width', underline=1, image=self.under_width_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.portrait_under_width)
        fit_portrait_menu.add_checkbutton(label='Over Height', underline=0, image=self.over_height_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.portrait_over_height)
        fit_portrait_menu.add_checkbutton(label='Over Width', underline=1, image=self.over_width_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.portrait_over_width)
        fit_landscape_menu = tk.Menu(self.option_menu, tearoff=False)
        self.option_menu.add_cascade(label='Fit Landscape', underline=4, menu=fit_landscape_menu)
        fit_landscape_menu.add_checkbutton(label='Under Height', underline=0, image=self.under_height_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.landscape_under_height)
        fit_landscape_menu.add_checkbutton(label='Under Width', underline=1, image=self.under_width_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.landscape_under_width)
        fit_landscape_menu.add_checkbutton(label='Over Height', underline=0, image=self.over_height_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.landscape_over_height)
        fit_landscape_menu.add_checkbutton(label='Over Width', underline=1, image=self.over_width_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.landscape_over_width)
        self.option_menu.add_checkbutton(label='Auto Colors', underline=0, image=self.auto_colors_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.auto_colors, accelerator='Ctrl+A')
        self.option_menu.add_checkbutton(label='Auto Background', underline=5, image=self.auto_colors_image, compound=tk.LEFT, onvalue=True, offvalue=False, variable=self.bg_auto_color, accelerator='Ctrl+B')

        self.help_menu.add_command(label='About', underline=0, command=self.menu_help_about)

        self.bind_all('<Control-o>', self.menu_file_open)
        self.bind_all('<F11>', self.menu_file_full_screen)
        self.bind_all('<F12>', self.menu_file_full_desktop)
        self.bind_all('<Escape>', self.menu_file_end_screen_desktop)
        self.bind_all('<Home>', self.menu_read_first)
        self.bind_all('<End>', self.menu_read_last)
        self.bind_all('<Prior>', self.menu_read_previous)
        self.bind_all('<Next>', self.menu_read_next)
        self.bind_all('<Up>', self.menu_read_up)
        self.bind_all('<Down>', self.menu_read_down)
        self.bind_all('<Left>', self.menu_read_left)
        self.bind_all('<Right>', self.menu_read_right)
        self.bind_all('<Control-plus>', self.menu_zoom_in)
        self.bind_all('<Control-minus>', self.menu_zoom_out)
        self.bind_all('<Control-0>', lambda e: self.menu_zoom(1.0))
        self.bind_all('<Control-a>', self.menu_auto_colors)
        self.bind_all('<Control-b>', self.menu_bg_auto_color)

    def check_menu(self):
        test = self.doujinshi.is_loaded() and self.current_page > 1 and not self.file_operation
        state = tk.NORMAL if test else tk.DISABLED
        self.read_menu.entryconfig('First Page', state=state)
        self.read_menu.entryconfig('Previous Page', state=state)
        self.button_first.config(state=state)
        self.button_previous.config(state=state)

        test = self.doujinshi.is_loaded() and self.current_page < self.doujinshi.get_nb_pages() and not self.file_operation
        state = tk.NORMAL if test else tk.DISABLED
        self.read_menu.entryconfig('Last Page', state=state)
        self.read_menu.entryconfig('Next Page', state=state)
        self.button_next.config(state=state)
        self.button_last.config(state=state)

        test = self.doujinshi.is_loaded() and not self.file_operation
        state = tk.NORMAL if test else tk.DISABLED
        self.file_menu.entryconfig('Save Comic', state=state)
        self.button_read.config(state=state)
        self.option_menu.entryconfig('Zoom', state=state)
        self.option_menu.entryconfig('Rotate', state=state)
        self.option_menu.entryconfig('Rotate All', state=state)

        test = not self.file_operation
        state = tk.NORMAL if test else tk.DISABLED
        self.file_menu.entryconfig('Open...', state=state)
        self.file_menu.entryconfig('Save Comic', state=state)
        self.button_load.config(state=state)

    def load_comic(self, comic_file_path):
        self.file_operation = True
        self.check_menu()

        progress = ttk.Progressbar(self.canvas, orient=tk.HORIZONTAL, mode='determinate',
                                   length=self.params['width'])
        progress.pack(side=tk.BOTTOM)
        self.doujinshi.load_comic(comic_file_path, progress, self.show_current_page)
        progress.pack_forget()

        self.current_page = 1
        self.show_current_page(mode='tl')

        self.file_operation = False
        self.check_menu()

    def save_comic(self):
        self.file_operation = True
        self.check_menu()

        progress = ttk.Progressbar(self.canvas, orient=tk.HORIZONTAL, mode='determinate',
                                   length=self.params['width'])
        progress.pack(side=tk.BOTTOM)
        self.doujinshi.save_comic(progress)
        progress.pack_forget()
        self.show_current_page()

        self.file_operation = False
        self.check_menu()

    def menu_file_open(self, event=None):
        comic_file_path = tkfd.askopenfilename(title="Ouvrir un Comic",
                                               filetypes=[('Comic archive', '.cbz'), ('all files', '.*')])
        if comic_file_path != '':
            self.load_comic(comic_file_path)

    def menu_file_save(self, event=None):
        if self.doujinshi.is_loaded():
            self.save_comic()

    def menu_file_full_screen(self, event=None):
        self.full_screen = not self.full_screen;
        if self.full_screen:
            self.state('zoomed')
        else:
            self.state('normal')

    def menu_file_full_desktop(self, event=None):
        self.full_desktop = not self.full_desktop
        if self.full_desktop:
            self.attributes('-fullscreen', True)
            self.wm_attributes('-topmost', 1)
        else:
            self.attributes('-fullscreen', False)
            self.wm_attributes('-topmost', 0)

    def menu_file_end_screen_desktop(self, event=None):
        if self.full_screen:
            self.full_screen = not self.full_screen
            self.state('normal')

        if self.full_desktop:
            self.full_desktop = not self.full_desktop
            self.attributes('-fullscreen', False)
            self.wm_attributes('-topmost', 0)

        self.show_current_page()

    def menu_file_exit(self):
        self.quit()

    def menu_read_first(self, event=None):
        self.current_page = 1
        self.show_current_page(mode='tl')

    def menu_read_last(self, event=None):
        self.current_page = self.doujinshi.get_nb_pages()
        self.show_current_page(mode='tl')

    def menu_read_next(self, event=None):
        self.current_page = min(self.current_page + 1, self.doujinshi.get_nb_pages())
        self.show_current_page(mode='tl')

    def menu_read_previous(self, event=None):
        self.current_page = max(self.current_page - 1, 1)
        self.show_current_page(mode='br')

    def menu_read_up(self, event=None):
        old_pos = self.canvas.coords(self.tkImage_id)
        self.canvas.move(tk.ALL, 0, self.params['scroll_speed'])
        self.constrain_image()
        new_pos = self.canvas.coords(self.tkImage_id)

        if new_pos == old_pos:
            self.scroll_attempts -= 1
            if self.scroll_attempts <= 0:
                self.scroll_attempts = self.params['scroll_next']
                if self.current_page > 1:
                    self.menu_read_previous()

    def menu_read_down(self, event=None):
        old_pos = self.canvas.coords(self.tkImage_id)
        self.canvas.move(tk.ALL, 0, -self.params['scroll_speed'])
        self.constrain_image()
        new_pos = self.canvas.coords(self.tkImage_id)

        if new_pos == old_pos:
            self.scroll_attempts -= 1
            if self.scroll_attempts <= 0:
                self.scroll_attempts = self.params['scroll_next']
                if self.current_page < self.doujinshi.get_nb_pages():
                    self.menu_read_next()

    def menu_read_left(self, event=None):
        self.canvas.move(tk.ALL, self.params['scroll_speed'], 0)
        self.constrain_image()

    def menu_read_right(self, event=None):
        self.canvas.move(tk.ALL, -self.params['scroll_speed'], 0)
        self.constrain_image()

    def menu_help_about(self, event=None):
        pass

    def menu_zoom_in(self, event=None):
        self.zoom = min(self.zoom * 1.15, 10)
        self.show_current_page()

    def menu_zoom_out(self, event=None):
        self.zoom = max(self.zoom / 1.15, 0.1)
        self.show_current_page()

    def menu_zoom(self, zoom, event=None):
        self.zoom = zoom
        self.show_current_page()

    def menu_auto_colors(self, event=None):
        self.auto_colors.set(not self.auto_colors.get())
        self.show_current_page()

    def menu_bg_auto_color(self, event=None):
        self.bg_auto_color.set(not self.bg_auto_color.get())
        self.show_current_page()

    def menu_rotate_left(self, event=None):
        angle = (self.doujinshi.get_page_rotation(self.current_page) + 90) % 360
        self.doujinshi.set_page_rotation(self.current_page, angle)
        self.show_current_page()

    def menu_rotate_right(self, event=None):
        angle = (self.doujinshi.get_page_rotation(self.current_page) + 270) % 360
        self.doujinshi.set_page_rotation(self.current_page, angle)
        self.show_current_page()

    def menu_rotate_reset(self, event=None):
        self.doujinshi.set_page_rotation(self.current_page, 0)
        self.show_current_page()

    def menu_rotate_all_left(self, event=None):
        for page in range(1, self.doujinshi.get_nb_pages()+1):
            angle = (self.doujinshi.get_page_rotation(page) + 90) % 360
            self.doujinshi.set_page_rotation(page, angle)
        self.show_current_page()

    def menu_rotate_all_right(self, event=None):
        for page in range(1, self.doujinshi.get_nb_pages()+1):
            angle = (self.doujinshi.get_page_rotation(page) + 270) % 360
            self.doujinshi.set_page_rotation(page, angle)
        self.show_current_page()

    def menu_rotate_all_reset(self, event=None):
        for page in range(1, self.doujinshi.get_nb_pages()+1):
            self.doujinshi.set_page_rotation(page, 0)
        self.show_current_page()

    def quit(self):
        self.save_config()
        sys.exit(0)

    def window_resize(self, event):
        if event.widget == self:
            self.params['width'] = event.width
            self.params['height'] = event.height
            self.params['win_x'] = self.winfo_x()
            self.params['win_y'] = self.winfo_y()

            self.show_current_page(mode='rz')

    def mouse_down(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def mouse_move(self, event):
        if self.tkImage_id is not None:
            self.canvas.move(tk.ALL, event.x - self.last_x, event.y - self.last_y)
            self.constrain_image()
        self.last_x = event.x
        self.last_y = event.y

    def mouse_wheel(self, event):
        if event.delta > 0:
            self.menu_read_up(event)
        else:
            self.menu_read_down(event)

    def constrain_image(self):
        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()
        tkimage_height = self.tkImage.height()
        tkimage_width = self.tkImage.width()
        image_left, image_top = self.canvas.coords(self.tkImage_id)
        new_image_left, new_image_top = image_left, image_top

        if tkimage_width <= canvas_width:
            new_image_left = (canvas_width - tkimage_width) // 2
        elif image_left > 0:
            new_image_left = 0
        elif tkimage_width + image_left < canvas_width:
            new_image_left = canvas_width - tkimage_width

        if tkimage_height <= canvas_height:
            new_image_top = (canvas_height - tkimage_height) // 2
        elif image_top > 0:
            new_image_top = 0
        elif tkimage_height + image_top < canvas_height:
            new_image_top = canvas_height - tkimage_height

        self.canvas.move(tk.ALL, new_image_left - image_left, new_image_top - image_top)

    def find_border_color(self, image):
        color_bins = collections.defaultdict(int)
        max_y = image.height - 1
        max_x = image.width - 1
        pixels = image.load()

        for y in range(1, max_y-1):
            color_bins[pixels[0, y]] += 1
            color_bins[pixels[max_x, y]] += 1

        for x in range(max_x):
            color_bins[pixels[x, 0]] += 1
            color_bins[pixels[x, max_y]] += 1

        color = max(color_bins.keys(), key=(lambda k: color_bins[k]))
        return '#{0:02x}{1:02x}{2:02x}'.format(*color)

    def show_current_page(self, mode=None, *args):
        if self.doujinshi.is_loaded():
            canvas_height = self.canvas.winfo_height()
            canvas_width = self.canvas.winfo_width()

            if self.tkImage_id is not None:
                image_left, image_top = self.canvas.coords(self.tkImage_id)
                center_horiz = (canvas_width / 2 - image_left) / self.tkImage.width()
                center_vert = (canvas_height / 2 - image_top) / self.tkImage.height()
            else:
                image_left, image_top = 0, 0
                center_horiz, center_vert = 0.0, 0.0

            image = self.doujinshi.get_page_image(self.current_page)

            if self.params['auto_colors']:
                image = ImageOps.autocontrast(image, cutoff=1)

            if self.params['bg_auto_color']:
                self.canvas['bg'] = self.find_border_color(image)
            else:
                self.canvas['bg'] = self.params['bg_color']

            ratio_width = None
            ratio_height = None

            if image.width <= image.height:  # Portrait
                if self.params['portrait_under_height'] and image.height < canvas_height:
                    ratio_height = canvas_height / image.height
                if self.params['portrait_over_height'] and image.height > canvas_height:
                    ratio_height = canvas_height / image.height
                if self.params['portrait_under_width'] and image.width < canvas_width:
                    ratio_width = canvas_width / image.width
                if self.params['portrait_over_width'] and image.width > canvas_width:
                    ratio_width = canvas_width / image.width
            else:   # Landscape
                if self.params['landscape_under_height'] and image.height < canvas_height:
                    ratio_height = canvas_height / image.height
                if self.params['landscape_over_height'] and image.height > canvas_height:
                    ratio_height = canvas_height / image.height
                if self.params['landscape_under_width'] and image.width < canvas_width:
                    ratio_width = canvas_width / image.width
                if self.params['landscape_over_width'] and image.width > canvas_width:
                    ratio_width = canvas_width / image.width

            if ratio_width is None: ratio_width = ratio_height
            if ratio_height is None: ratio_height = ratio_width
            if ratio_width is None: ratio_width = ratio_height = 1.0

            ratio = min(ratio_width, ratio_height) * self.zoom

            new_width = math.floor(image.width * ratio)
            new_height = math.floor(image.height * ratio)

            if mode == 'rz':
                image = image.resize((new_width, new_height), Image.NEAREST)
                if self.timer is not None:
                    self.after_cancel(self.timer)
                self.timer = self.after(200, self.show_current_page)
            else:
                image = image.resize((new_width, new_height), Image.ANTIALIAS)

            self.tkImage = ImageTk.PhotoImage(image)
            tkimage_height = self.tkImage.height()
            tkimage_width = self.tkImage.width()

            if mode == 'rz':
                image_left = int(canvas_width / 2 - tkimage_width * center_horiz)
                image_top = int(canvas_height / 2 - tkimage_height * center_vert)
            elif mode == 'tl':
                image_left, image_top = 0, 0
            elif mode == 'br':
                image_left = canvas_width - tkimage_width
                image_top = canvas_height - tkimage_height

            self.canvas.delete(self.tkImage_id)
            self.tkImage_id = self.canvas.create_image(image_left, image_top, anchor=tk.NW, image=self.tkImage)
            self.constrain_image()

            self.check_menu()

            self.title('HDoujinshi viewer - {0:s} - {1:d}/{2:d}'.format(self.doujinshi.title,
                                                                        self.current_page,
                                                                        self.doujinshi.get_nb_pages()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Comic file viewer.')
    parser.add_argument('comic', metavar='[drive:][path]filename', nargs='?', help='Specify the file to display.')
    args = parser.parse_args()

    app = HDViewer(args.comic)
    app.mainloop()

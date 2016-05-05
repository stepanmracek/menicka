#! /usr/bin/env python3

import os
import time
import datetime
import cherrypy
import downloader
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))


class Menicka(object):
    def __init__(self):
        self.menus = None
        self.timeStamp = None

    @cherrypy.expose
    def index(self):
        now = time.time()
        if self.menus is None or (self.timeStamp is not None and now - self.timeStamp > 3600):
            self.menus = downloader.getMenus()
            self.timeStamp = now
            print(self.menus)
        tmpl = env.get_template('index.html')
        formattedTimeStamp = datetime.datetime.fromtimestamp(self.timeStamp).strftime('%c')
        return tmpl.render(menus=self.menus, timeStamp=formattedTimeStamp)

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    config = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8500
        }, '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(path, 'static')
        }
    }

    cherrypy.quickstart(Menicka(), '/', config)

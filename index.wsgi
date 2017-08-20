#coding:utf-8
import sae

from jaydenfoo import wsgi

application = sae.create_wsgi_app(wsgi.application)

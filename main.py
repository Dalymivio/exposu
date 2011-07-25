#!/usr/bin/env python

import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class exposure:
	def __init__(self):
		self.aperture = 1.0
		self.shutter = 100
		self.iso = 100
		
	def set(self, aperture, shutter, iso):
		self.aperture = aperture
		self.shutter = shutter
		self.iso = iso
		
	def intensity(self):
		return self.aperture * self.shutter * self.iso
		#return 50

class MainHandler(webapp.RequestHandler):
	e1 = exposure()
	e2 = exposure()
	def get(self):
		if MainHandler.e1.intensity() > -1:
			#print 'e tests passed'
			template_values = {'e1': MainHandler.e1.intensity(), 'e2': MainHandler.e2.intensity()}
			#template_values = {'e1': 123, 'e2': 456}
		else:
			template_values = {'e1': 1, 'e2': 4}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
	
	def post(self):
		#print MainHandler.e1.iso
		#print MainHandler.e1.intensity()
		MainHandler.e1.set(
						float(self.request.get('aperture1')),
						float(self.request.get('shutter1')),
						int(self.request.get('iso1'))
						)
		MainHandler.e2.set(
						float(self.request.get('aperture2')),
						float(self.request.get('shutter2')),
						int(self.request.get('iso2'))
						)
		self.redirect('/')


def main():
	application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
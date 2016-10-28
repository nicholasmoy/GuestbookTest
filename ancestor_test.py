#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
from google.appengine.ext import db

# MODELS
class Child_model(db.Model):
    name = db.StringProperty()

class Parent_model(db.Model):
    name = db.StringProperty()

class Root_model(db.Model):
    pass


# MAIN
class MainHandler(webapp2.RequestHandler):
    def get(self, url):
        if not Root_model.get_by_key_name("root"):
            # Populate db on first run
            self.populate()

        logging.info("-- Get all enteties recursivly --")
        root        = Root_model.get_by_key_name("root")
        logging.info(" - %s", root)

        parents     = Parent_model.all().ancestor(root)

        # Recursivly
        for p in parents:
            logging.info(" -- %s" % p.name)
            children = list(Child_model.all().ancestor(p))
            [logging.info(" --- %s" % c.name) for c in children]

        # Shortcut
        #children   = Child_model.all().ancestor(root)

        logging.info("-- Get all children for a parent --")
        [logging.info(" -- %s" % c.name) for c in self.get_all_children_for_a_parent() ]    

        logging.info("-- Get some children for a parent --")
        [logging.info(" -- %s" % c.name) for c in self.get_all_children_for_a_parent() if c.name == "Child num 0 with parent Parent num 0" or c.name == "Doesn't exist" ]

        logging.info("-- Get parent for child --")
        child = Child_model.all()[0]
        logging.info("Child: %s" % child.name)
        logging.info("Parent: %s" % child.parent().name)

    def get_all_children_for_a_parent(self):
        parent = Parent_model.all()[0]
        logging.info(" - %s" % parent.name)
        return Child_model().all().ancestor(parent)


    def populate(self):
        root = Root_model(key_name="root")
        root.put()

        parents = []
        for i in range(3):
            parents.append( Parent_model(parent=root, name="Parent num %d" % i) )
        db.put(parents)

        import random
        children = []
        for p in parents:
            for i in range(random.randint(0,10)):
                children.append( Child_model(parent=p, name="Child num %d with parent %s" % (i, p.name)) )
        db.put(children)


app = webapp2.WSGIApplication([('/(.*)', MainHandler)],
                                debug=True)
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

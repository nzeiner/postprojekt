
#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class RandomHandler(BaseHandler):
    def get(self):
        parameters = {}
        parameters["randomnumbers"] = random.sample(range(1,46),6)
        return self.render_template("random.html", parameters)

class FormHandler(BaseHandler):
    def get(self):
        return self.render_template("post.html")
    def post(self):
        parameters = {}
        parameters["username"] = self.request.get("username")
        return self.render_template("greeting.html", parameters)
class CalcHandler(BaseHandler):
    def get(self):
        return self.render_template("calculator.html")
    def post(self):
        parameters = {}
        zahl1 = float(self.request.get("erste_zahl"))
        zahl2 = float(self.request.get("zweite_zahl"))
        operator = self.request.get("operator")
        if operator == "+":
            ergebnis = zahl1 + zahl2
        elif operator == "-":
            ergebnis = zahl1 - zahl2
        elif operator == "*":
            ergebnis = zahl1 * zahl2
        else:
            ergebnis = zahl1 / zahl2
        parameters["ergebnis"] = ergebnis
        return self.render_template("ergebnis.html",parameters)

class SecretHandler(BaseHandler):
    def get(self):
        return self.render_template("secret.html")
    def post(self):
        parameters = {}
        secret = 12
        guess = str(self.request.get("ratemal"))
        if guess == secret:
            ergebnis = "Korrekt! Gratulation!"
        else:
            ergebnis = "Wrong"
        parameters["ergebnis"] = ergebnis
        return self.render_template("loesung.html",parameters)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/zufallszahlen', RandomHandler),
    webapp2.Route('/postbeispiel', FormHandler),
    webapp2.Route('/taschenrechner', CalcHandler),
    webapp2.Route('/secretnumber', SecretHandler),
], debug=True)

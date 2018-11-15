from flask import Flask
from flask_script import Manager
from app import blueprint
import os

app = Flask(__name__)
manager = Manager(app)

app.register_blueprint(blueprint)


@manager.command
def test(coverage=False):
    import unittest
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    COV.erase()


if __name__ == '__main__':
    manager.run()

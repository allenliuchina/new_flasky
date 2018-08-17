from app import create_app, db
from app.models import User, Role, Post
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

app = create_app('dev')
manager = Manager(app)

migrate = Migrate(app, db)


def make_shell_content():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)


manager.add_command('shell', Shell(make_context=make_shell_content))
manager.add_command('db', MigrateCommand)


@manager.command
def init_role():
    Role.insert_roles()


@manager.command
def test():
    """Run the unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

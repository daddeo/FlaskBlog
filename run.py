# when working with packages will import from the __init__.py file within the package,
# so app has to exist in the __init__.py file
from flaskblog import create_app
from flaskblog.database import db_check, db_initialize

# pass in Config class (e.g. prod, dev, testing)
app = create_app()
# app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# https://flask.palletsprojects.com/en/1.1.x/cli/
# import click
# @click.command('initdb')
@app.cli.command("initdb")
def initialize_db():
    """ Reinitialize the database and preload """
    db_initialize()
    return


# import click
# @click.command('check')
@app.cli.command("check")
def check_db():
    db_check()
    return


# only job is to run the app
if __name__ == "__main__":
    app.run(debug=True)

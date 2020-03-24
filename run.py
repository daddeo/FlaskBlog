# when working with packages will import from the __init__.py file within the package,
# so app has to exist in the __init__.py file
from flaskblog import app

# only job is to run the app
if __name__ == "__main__":
    app.run(debug=True)

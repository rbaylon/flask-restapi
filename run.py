from baseapp import app
from api import rest

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=6699,debug=True)

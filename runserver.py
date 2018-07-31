import os
from project import app

port = int(os.getenv('PORT', 8000))

def runserver():
    
    app.run(host='0.0.0.0', port=port, debug = False,threaded= True)

if __name__ == '__main__':
    runserver()

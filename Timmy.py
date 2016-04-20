from app import *
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
if __name__ == '__main__':
    app = create_app()
    Config.init_app(app)
    app.run(debug=True)
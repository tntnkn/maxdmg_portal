from flask          import Flask
from .config        import Config
from .utilities     import init_utils
from .auth          import init_auth, require_login 
from .forms         import init_forms
from .storage       import init_storage
from .cache         import init_cache
from .graph         import init_dash


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object( Config() )

    with app.app_context():
        init_auth(app)    
        init_forms(app)
        init_storage(app)
        init_cache(app)
        init_utils(app)

        from . import routes

        init_dash(app)

        for f_name, f in app.view_functions.items():
            if 'graph' in f_name:
                app.view_functions[f_name] = require_login(f) 

    return app


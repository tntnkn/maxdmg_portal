def init_context_processors(app):
    @app.context_processor
    def inject_auth():
        return dict(auth=app.auth)

    @app.context_processor
    def inject_storage():
        return dict(storage=app.storage)


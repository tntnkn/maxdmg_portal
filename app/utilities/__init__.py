def init_utils(app):
    from .context_processors    import init_context_processors

    init_context_processors(app)
    return app


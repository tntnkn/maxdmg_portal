def init_cache(app):
    from .AppCache          import AppCache
    from .RedisCache        import RedisCache

    if app.config['REDIS']:
        cache = RedisCache(app.config['REDIS_HOST'], app.config['REDIS_PORT'])
    else:
        cache = AppCache()
    app.cache = cache
    return app


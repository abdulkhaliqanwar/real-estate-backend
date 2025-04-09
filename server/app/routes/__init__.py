def register_routes(app):
    from .auth_routes import auth_bp
    from .property_routes import property_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(property_bp, url_prefix='/api')

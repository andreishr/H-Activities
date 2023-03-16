from config.init import create_app
from config.routes.auth_routes import auth_routes_bp
from config.routes.management_routes import manage_routes_bp
from config.routes.utility_routes import utility_routes_bp

app = create_app()
app.register_blueprint(auth_routes_bp)
app.register_blueprint(manage_routes_bp)
app.register_blueprint(utility_routes_bp)

if __name__ == "__main__":
    app.run(debug=True)
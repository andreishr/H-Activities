from config.init import create_app
from config.routes.routes import routes_bp

app = create_app()
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(debug=True)
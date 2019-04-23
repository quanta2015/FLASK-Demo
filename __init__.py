from flask import Flask, render_template,g

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='blog')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from flaskweb.views import index
app.register_blueprint(index.bp)


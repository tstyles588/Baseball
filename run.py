from app import app, db
from app.models import User, Post

@app.shell_context_processor
def shell_Context():
    return {'app': app, 'db': db, "User": User, 'Post': Post}

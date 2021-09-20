from app import create_app, db
from app.models import Student, Course, College

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student, 'Course': Course, 'College': College}
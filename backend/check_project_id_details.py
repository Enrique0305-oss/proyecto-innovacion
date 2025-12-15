from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        result = conn.execute(text("SHOW FULL COLUMNS FROM projects WHERE Field='project_id'"))
        print("\nInformación completa de project_id:")
        print("-" * 80)
        for row in result:
            print(row)

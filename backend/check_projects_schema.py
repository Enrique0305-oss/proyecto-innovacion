from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        result = conn.execute(text('DESCRIBE projects'))
        print("\nEstructura de la tabla projects:")
        print("-" * 80)
        for row in result:
            print(row)

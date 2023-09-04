from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Default_image = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False, unique=True)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, default="https://tinyurl.com/demo-cupcake")


    def serialize(self):
        """Returns a dict representation of todo which we can turn into JSON"""
        return {
            'id': self.id,
            'flavor':self.flavor,
            'size':self.size,
            'rating':self.rating,
            'image':self.image
        }
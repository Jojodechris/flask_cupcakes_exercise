"""Flask app for Cupcakes"""
from flask import Flask, request,jsonify,render_template,  redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db,connect_db,Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

# with app.app_context():
    # connect_db(app)
# db.create_all()


@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def list_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route("/api/cupcakes/<int:id>")
def single_cakes(id):
    """Return JSON {'dessert': {id, name, calories}}"""

    cupcake=Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_todo():
    """Creates a new cupcake and returns JSON of that created cupcake"""
    new_cupcake = Cupcake(flavor=request.json["flavor"],size=request.json['size'],image=request.json['image'],rating=request.json['rating'])
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)



@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular todo and responds w/ JSON of that updated todo"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.image = request.json.get('image', cupcake.image)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.size= request.json.get('size', cupcake.size)
    # todo.done = request.json.get('done',  todo.done)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_todo(id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")


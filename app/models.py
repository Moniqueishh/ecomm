from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

cart = db.Table(
    'cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    product = db.relationship('Product', backref='product', lazy=True)
    carts = db.relationship('Product',
                            secondary='cart',
                            backref='carts',
                            lazy='dynamic',
                            cascade= 'all')

#as an example for backref
#with the post below
# p1 = Post()
# p1.author

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password) 
        #self.password = password   ---OLD  not hashed

    def saveUser(self):
        db.session.add(self)
        db.session.commit()

    def unCart(self, product):
        self.carts.remove(product)
        db.session.commit()

    def clearCart(self):
        self.carts=[]
        # x=self.carts.all()
        # x.clear()
        # self.carts=x
        db.session.commit()
    
    def addCart(self, product):
        self.carts.append(product)
        db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String)
    body = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
                                #  notice          ^^^^^ --> lowercase?  yep.  User.id

    def __init__(self, title, img_url, body, user_id):
        self.title = title
        self.img_url = img_url
        self.body = body
        self.user_id = user_id

    def saveProduct(self):
        db.session.add(self)
        db.session.commit()

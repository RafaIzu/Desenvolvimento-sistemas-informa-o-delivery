from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Consumer, Product, Destiny

form = Blueprint('form', __name__)


@form.route('/consumer')
def consumer():
    consumers = Consumer.query.with_entities(Consumer.id, Consumer.name,
                                             Consumer.email)
    destinies = Destiny.query.with_entities(Destiny.address, Destiny.number,
                                            Destiny.zipcode)
    print(consumer) 
    return render_template('consumer/consumer.html', consumers=zip(consumers, destinies))


@form.route("/add_consumer", methods=["GET", "POST"])
def add_consumer():
    if request.method == 'POST':
        destiny = Destiny(address=request.form['address'],
                          number=request.form['number'],
                          zipcode=request.form['zipcode'])
        consumer = Consumer(name=request.form['name'], email=request.form['email'],
                            password=generate_password_hash(request.form['password']),
                            destiny=destiny)
        db.session.add(consumer)
        db.session.commit()
        return redirect(url_for('form.consumer'))
    return render_template('consumer/add_consumer.html')


@form.route('/edit_consumer/<int:id>', methods=['GET', 'POST'])
def edit_consumer(id):
    consumer = Consumer.query.get(id)
    if request.method == 'POST':
        consumer.name = request.form['name']
        consumer.email = request.form['email']
        consumer.destiny.address = request.form['address']
        consumer.destiny.number = request.form['number']
        consumer.destiny.zipcode = request.form['zipcode']
        db.session.commit()
        print('comitou')
        return redirect(url_for('form.consumer'))
    return render_template('consumer/edit_consumer.html', consumer=consumer)

@form.route('/delete_consumer/<int:id>')
def delete_consumer(id):
    consumer = Consumer.query.get(id)
    db.session.delete(consumer)
    db.session.commit()
    return redirect(url_for('form.consumer'))


@form.route('/product')
def product():
    products = Product.query.all()
    print(product) 
    return render_template('product/product.html', products=products)


@form.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == 'POST':
        product = Product(name=request.form['name'],
                          price=request.form['price'].replace(",", "."),
                          description=request.form['description'],
                          players=request.form['players'],
                          age=request.form['age'])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('form.product'))
    return render_template('product/add_product.html')


@form.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        product.players = request.form['players']
        product.age = request.form['age']
        db.session.commit()
        print('comitou')
        return redirect(url_for('form.product'))
    return render_template('product/edit_product.html', product=product)


@form.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('form.product'))


@form.route('/' , methods=["GET"])
def home_get_product():
    products = Product.query.all()
    print(product) 
    return render_template('index.html', products=products)

@form.route('/product/<int:id>')
def get_produto_id(id):
    product = Product.query.get(id)
    return render_template('produto_id.html', product=product)

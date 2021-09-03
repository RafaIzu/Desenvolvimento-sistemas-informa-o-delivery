from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Consumer, Product, Destiny
from . import tables


@tables.route('/consumer')
def consumer():
    consumers = Consumer.query.with_entities(Consumer.id, Consumer.username,
                                             Consumer.email)
    destinies = Destiny.query.with_entities(Destiny.address, Destiny.number,
                                            Destiny.zipcode)
    print(consumer) 
    return render_template('consumer/consumer.html', consumers=zip(consumers, destinies))


@tables.route('/edit_consumer/<int:id>', methods=['GET', 'POST'])
def edit_consumer(id):
    consumer = Consumer.query.get(id)
    if request.method == 'POST':
        consumer.destiny.address = request.form['address']
        consumer.destiny.number = request.form['number']
        consumer.destiny.zipcode = request.form['zipcode']
        db.session.commit()
        return redirect(url_for('tables.consumer'))
    return render_template('consumer/edit_destiny.html', consumer=consumer)


@tables.route('/delete_consumer/<int:id>')
def delete_consumer(id):
    consumer = Consumer.query.get(id)
    db.session.delete(consumer)
    db.session.commit()
    return redirect(url_for('tables.consumer'))


@tables.route('/product')
def product():
    products = Product.query.all()
    print(product) 
    return render_template('product/product.html', products=products)


@tables.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == 'POST':
        product = Product(name=request.form['name'],
                          price=request.form['price'].replace(",", "."),
                          description=request.form['description'],
                          players=request.form['players'],
                          age=request.form['age'])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('tables.product'))
    return render_template('product/add_product.html')


@tables.route('/edit_product/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('tables.product'))
    return render_template('product/edit_product.html', product=product)


@tables.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('tables.product'))
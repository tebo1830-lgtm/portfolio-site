from flask import Flask, request, jsonify
import sqlite3
import os
import sys

from db_helpers import ensure_supplies_table, seed_supplies_data, get_supplies_connection

app = Flask(__name__)


def format_products(products):
    return [
        {'fertilizer_id': p[0], 'brand': p[1], 'price': p[2], 'type': p[3]}
        for p in products
    ]


def get_products_by_query(sql, params):
    conn = get_supplies_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    products = cursor.fetchall()
    conn.close()
    return products


def print_products(products):
    if not products:
        print('No matching fertilizers found.')
        return
    print('\nFound fertilizers:')
    for product in products:
        print(f"ID: {product[0]}, Brand: {product[1]}, Price: ${product[2]:.2f}, Type: {product[3]}")
    print()


def search_by_type_cli():
    ftype = input('Enter fertilizer type: ').strip()
    if not ftype:
        print('Type is required.')
        return
    products = get_products_by_query('SELECT * FROM fertilizers WHERE type = ?', (ftype,))
    print_products(products)


def search_by_brand_cli():
    brand_name = input('Enter brand name: ').strip()
    if not brand_name:
        print('Brand is required.')
        return
    products = get_products_by_query('SELECT * FROM fertilizers WHERE brand = ?', (brand_name,))
    print_products(products)


def search_by_price_cli():
    raw_price = input('Enter maximum price: ').strip()
    try:
        price = float(raw_price)
    except ValueError:
        print('Enter a valid numeric price.')
        return
    products = get_products_by_query('SELECT * FROM fertilizers WHERE price <= ?', (price,))
    print_products(products)


def run_cli():
    while True:
        print('\nFertilizer Catalog CLI')
        print('1. Search by type')
        print('2. Search by brand')
        print('3. Search by maximum price')
        print('4. Exit')
        choice = input('Choose an option: ').strip()

        if choice == '1':
            search_by_type_cli()
        elif choice == '2':
            search_by_brand_cli()
        elif choice == '3':
            search_by_price_cli()
        elif choice == '4':
            print('Exiting Fertilizer Catalog.')
            break
        else:
            print('Invalid selection.')


@app.route('/')
def home():
    return '''<span style='text-align:center'>
                <h1>Welcome to Acme Fertilizer Supply!</h1>
                <h3>The Farmer's Choice for Quality Fertilizer</h3>
            </span>'''


@app.route('/type')
def type_endpoint():
    f_type = request.args.get('ftype')
    if not f_type:
        return jsonify({'error': 'Type parameter is missing'}), 400
    products = get_products_by_query('SELECT * FROM fertilizers WHERE type = ?', (f_type,))
    product_list = format_products(products)
    if not product_list:
        return jsonify({'message': 'No fertilizer of type ' + f_type + ' found'}), 404
    return jsonify(product_list)


@app.route('/brand')
def brand_endpoint():
    brand_name = request.args.get('name')
    if not brand_name:
        return jsonify({'error': 'brand name parameter is missing'}), 400
    products = get_products_by_query('SELECT * FROM fertilizers WHERE brand = ?', (brand_name,))
    product_list = format_products(products)
    if not product_list:
        return jsonify({'message': 'No ' + brand_name + ' brand fertilizers found'}), 404
    return jsonify(product_list)


@app.route('/cost')
def cost_endpoint():
    price = request.args.get('price')
    if not price:
        return jsonify({'error': 'Price parameter is missing'}), 400
    try:
        price_value = float(price)
    except ValueError:
        return jsonify({'error': 'Price must be numeric'}), 400
    products = get_products_by_query('SELECT * FROM fertilizers WHERE price <= ?', (price_value,))
    product_list = format_products(products)
    if not product_list:
        return jsonify({'message': 'No products found at or below ' + price}), 404
    return jsonify(product_list)


def main():
    ensure_supplies_table()
    seed_supplies_data()

    print('Fertilizer Catalog is ready.')
    mode = input('Choose mode (cli/server): ').strip().lower()
    if mode == 'server':
        app.run(debug=True)
    elif mode == 'cli':
        run_cli()
    else:
        print('No valid mode chosen; exiting.')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\nExiting Fertilizer Catalog.')
        sys.exit(0)

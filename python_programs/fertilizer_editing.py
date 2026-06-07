from flask import Flask, request, jsonify
import sqlite3
import os
import sys

from db_helpers import ensure_supplies_table, seed_supplies_data, get_supplies_connection

app = Flask(__name__)


def get_supplies_product(which, chem):
    conn = get_supplies_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fertilizers WHERE brand = ? AND type = ?", (which, chem))
    product = cursor.fetchone()
    conn.close()
    return product


def update_price(brand, _type, price):
    conn = get_supplies_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE fertilizers SET price = ? WHERE brand = ? AND type = ?''', (price, brand, _type))
    conn.commit()
    conn.close()


def access_row(which, chem):
    return get_supplies_product(which, chem)


def print_product(product):
    if not product:
        print('Product not found.')
        return
    print(f"ID: {product[0]}, Brand: {product[1]}, Price: ${product[2]:.2f}, Type: {product[3]}")


def update_price_cli():
    brand = input('Enter fertilizer brand: ').strip()
    if not brand:
        print('Brand is required.')
        return
    _type = input('Enter fertilizer type: ').strip()
    if not _type:
        print('Type is required.')
        return
    product = access_row(brand, _type)
    if not product:
        print('No product found for that brand and type.')
        return
    print('Current product:')
    print_product(product)
    raw_price = input('Enter new price: ').strip()
    try:
        price = float(raw_price)
    except ValueError:
        print('Invalid price format.')
        return
    update_price(brand, _type, price)
    updated = access_row(brand, _type)
    print('Updated product:')
    print_product(updated)


def view_product_cli():
    brand = input('Enter fertilizer brand: ').strip()
    if not brand:
        print('Brand is required.')
        return
    _type = input('Enter fertilizer type: ').strip()
    if not _type:
        print('Type is required.')
        return
    product = access_row(brand, _type)
    print_product(product)


def run_cli():
    while True:
        print('\nFertilizer Edit CLI')
        print('1. View fertilizer details')
        print('2. Update fertilizer price')
        print('3. Exit')
        choice = input('Choose an option: ').strip()
        if choice == '1':
            view_product_cli()
        elif choice == '2':
            update_price_cli()
        elif choice == '3':
            print('Exiting Fertilizer Edit CLI.')
            break
        else:
            print('Invalid selection.')


@app.route('/')  # The root/Index of the server
def home():
    return '''<span style='text-align:center'>
                <h1>Acme Fertilizer Supply: Database Management</h1>
                <h3>Authorized Users Only</h3><hr/>
            </span>'''


@app.route('/revise')    # domain/revise route
def edit_request():
    brand = request.args.get('brand')
    _type = request.args.get('type')
    price = request.args.get('price')
    if not brand:
        return jsonify({'error': 'Please provide fertilizer brand.'}), 400
    if not _type:
        return jsonify({'error': 'Please provide fertilizer type.'}), 400

    product = access_row(brand, _type)
    if not product:
        return jsonify({'Product not found': brand + ':' + _type}), 400

    if price is None:
        return jsonify({'fertilizer_id': product[0], 'brand': product[1], 'price': product[2], 'type': product[3]})

    try:
        price_value = float(price)
    except ValueError:
        return jsonify({'error': 'Price must be numeric'}), 400

    update_price(brand, _type, price_value)
    updated = access_row(brand, _type)
    return jsonify({'fertilizer_id': updated[0], 'brand': updated[1], 'price': updated[2], 'type': updated[3]})


def main():
    ensure_supplies_table()
    seed_supplies_data()

    print('Fertilizer Editing tool is ready.')
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
        print('\nExiting Fertilizer Editing.')
        sys.exit(0)

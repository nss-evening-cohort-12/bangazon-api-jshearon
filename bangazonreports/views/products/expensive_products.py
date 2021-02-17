import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from bangazonreports.views import Connection


def products_over_1000(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.description,
                    p.quantity,
                    p.created_date,
                    p.location,
                    p.price,
                    cat.name AS category,
                    u.first_name || ' ' || u.last_name AS fullname
                FROM
                    bangazonapi_product p
                LEFT JOIN bangazonapi_productcategory cat ON p.category_id = cat.id
                LEFT JOIN bangazonapi_customer cust ON p.customer_id = cust.id
                LEFT JOIN auth_user u ON cust.user_id = u.id
                WHERE p.price >= 1000
            """)

            dataset = db_cursor.fetchall()

            products = {}

            for row in dataset:
              rowid = row["id"]
              products[rowid] = {}
              products[rowid]["id"] = rowid
              products[rowid]["description"] = row["description"]
              products[rowid]["quantity"] = row["quantity"]
              products[rowid]["created_date"] = row["created_date"]
              products[rowid]["location"] = row["location"]
              products[rowid]["price"] = row["price"]
              products[rowid]["category"] = row["category"]
              products[rowid]["fullname"] = row["fullname"]

                
        # Get only the values from the dictionary and create a list from them
        list_of_products_over_1000 = products.values()

        # Specify the Django template and provide data context
        template = 'products/products_over_1000.html'
        context = {
            'products_list': list_of_products_over_1000
        }

        return render(request, template, context)

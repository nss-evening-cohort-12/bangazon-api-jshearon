import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from bangazonreports.views import Connection


def incomplete_orders(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
              SELECT
	              o.id orderid,
	              u.first_name || ' ' || u.last_name AS fullname,
	              SUM (p.price) AS total
	            FROM bangazonapi_order o
	            JOIN bangazonapi_orderproduct op ON op.order_id = o.id
	            JOIN bangazonapi_product p ON p.id = op.product_id
	            JOIN bangazonapi_customer cust ON o.customer_id = cust.id
              JOIN auth_user u ON cust.user_id = u.id
	            WHERE o.payment_type_id IS NULL
	            GROUP BY o.id
            """)

            dataset = db_cursor.fetchall()

            orders = {}

            for row in dataset:
              rowid = row["orderid"]
              orders[rowid] = {}
              orders[rowid]["orderid"] = rowid
              orders[rowid]["fullname"] = row["fullname"]
              orders[rowid]["total"] = row["total"]
              orders[rowid]["payment_type"] = 'In Progress'
                
        # Get only the values from the dictionary and create a list from them
        list_of_incomplete_orders = orders.values()

        # Specify the Django template and provide data context
        template = 'orders/completed_orders.html'
        context = {
            'report_title': 'Incomplete Orders',
            'orders_list': list_of_incomplete_orders
        }

        return render(request, template, context)

import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from bangazonreports.views import Connection


def completed_orders(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
              SELECT
	              o.id orderid,
	              u.first_name || ' ' || u.last_name AS fullname,
	              SUM (p.price) AS total,
	              pt.merchant_name AS payment_type
	            FROM bangazonapi_order o
	            JOIN bangazonapi_orderproduct op ON op.order_id = o.id
	            JOIN bangazonapi_product p ON p.id = op.product_id
	            JOIN bangazonapi_customer cust ON o.customer_id = cust.id
              JOIN auth_user u ON cust.user_id = u.id
              JOIN bangazonapi_payment pt ON pt.customer_id = cust.id
	            WHERE o.payment_type_id IS NOT NULL
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
              orders[rowid]["payment_type"] = row["payment_type"]
                
        # Get only the values from the dictionary and create a list from them
        list_of_complete_orders = orders.values()

        # Specify the Django template and provide data context
        template = 'orders/completed_orders.html'
        context = {
            'report_title': 'Completed Orders',
            'orders_list': list_of_complete_orders
        }

        return render(request, template, context)

import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from bangazonreports.views import Connection


def favorited_sellers(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
              SELECT
	              u.first_name || u.last_name AS fullname, 
                
            """)

            dataset = db_cursor.fetchall()

            sellers = {}

            for row in dataset:
              rowid = row["orderid"]
              sellers[rowid] = {}
              sellers[rowid]["orderid"] = rowid
              sellers[rowid]["fullname"] = row["fullname"]
              sellers[rowid]["total"] = row["total"]
              sellers[rowid]["payment_type"] = row["payment_type"]
                
        # Get only the values from the dictionary and create a list from them
        list_of_favorite_sellers = sellers.values()

        # Specify the Django template and provide data context
        template = 'users/favorites_sellers.html'
        context = {
            'report_title': 'Favorited Sellers By User',
            'sellers_list': list_of_favorite_sellers
        }

        return render(request, template, context)

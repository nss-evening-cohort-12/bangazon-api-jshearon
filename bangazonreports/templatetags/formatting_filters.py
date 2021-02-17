from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from datetime import datetime

register = template.Library()

def currency(dollars):
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

def prettydate(datestr):
    date_object = datetime.strptime(datestr, '%Y-%m-%d')
    return datetime.strftime(date_object, '%B %d, %Y')

register.filter('currency', currency)
register.filter('prettydate', prettydate)

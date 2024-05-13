from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.snippets.models import register_snippet
from django.contrib import admin

from .models import Customer, Plan, Order, Suppliers, Ingredients, Meal, Menu

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (such as pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

admin.site.register(Customer)
admin.site.register(Plan)
admin.site.register(Order)
admin.site.register(Suppliers)
admin.site.register(Ingredients)
admin.site.register(Meal)
admin.site.register(Menu)

register_snippet(Customer)
register_snippet(Plan)
register_snippet(Order)
register_snippet(Suppliers)
register_snippet(Ingredients)
register_snippet(Meal)
register_snippet(Menu)
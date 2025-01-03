from .cart import Cart

# create context processor so our cart ca work on all pages
def cart(request):
    # Return the default data form Cart
    return {'cart':Cart(request)}
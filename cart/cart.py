# make a session user on site
from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # get request
        self.request = request
        # Get the current session key if exists
        cart = self.session.get('session_key')

        #if the user is new, no sessions key. Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True  

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':4} to {"3":1, "2":4} ca saputem folosi JSON, in db nostru se salveaza un string si cu JSON il trnasforma inapoi in dictionar
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save our carty to the profile model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True  

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':4} to {"3":1, "2":4} ca saputem folosi JSON, in db nostru se salveaza un string si cu JSON il trnasforma inapoi in dictionar
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save our carty to the profile model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)  
    
    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup products in db
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quanities = self.cart
        return quanities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # Get the cart
        ourcart = self.cart
        #update dictionari/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':4} to {"3":1, "2":4} ca saputem folosi JSON, in db nostru se salveaza un string si cu JSON il trnasforma inapoi in dictionar
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save our carty to the profile model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing


    
    def delete(self, product):
        product_id = str(product)
        
        #delete from disctionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1, '2':4} to {"3":1, "2":4} ca saputem folosi JSON, in db nostru se salveaza un string si cu JSON il trnasforma inapoi in dictionar
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save our carty to the profile model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        # Get product ids
        products_ids = self.cart.keys()
        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=products_ids)
        # get qantities
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            #convert key string in int
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total




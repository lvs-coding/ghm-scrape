class Product:

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        self._discount = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def short_description(self):
        return self._short_description

    @short_description.setter
    def short_description(self, value):
        self._short_description = value

    @property
    def sub_products(self):
        return self._sub_products

    @sub_products.setter
    def sub_products(self,value):
        self._sub_products = value

    @property
    def net_weight(self):
        return self._net_weight

    @net_weight.setter
    def net_weight(self, value):
        self._net_weight = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    
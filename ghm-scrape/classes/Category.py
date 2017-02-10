class Category:
    def __init__(self, name, link, level, has_children):
        self._link = link
        self._name = name
        self._level = level
        self._has_children = has_children
    
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
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def has_children(self):
        return self._has_children

    @has_children.setter
    def has_children(self, value):
        self._has_children = value


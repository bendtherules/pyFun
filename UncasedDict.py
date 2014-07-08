class UncasedDict(dict):

    def __getitem__(self, key):
        for each_key in self:
            if each_key.upper() == key.upper():
                return super(UncasedDict, self).__getitem__(each_key)
        else:
            return super(UncasedDict, self).__getitem__(key)

    def has_key(self, key):
        return self.__contains__(key)

    def get(self, key):
        return self.__getitem__(key)

    def __contains__(self, key):
        for each_key in self:
            if each_key.upper() == key.upper():
                return True
        else:
            return False

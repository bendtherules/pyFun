class uniquelist(list):
    ''' A list whose every value is unique.
    uniquelist.append(val) or __setitem__(pos,val) i.e. uniquelist[pos]=val is ignored if val is already in uniquelist.
    Returns True if the value is added, else returns False. '''
    def __setitem__(self,pos,val):
        if val not in self:
            super(uniquelist,self).__setitem__(pos,val)
            return True
        else:
            return False
    def append(self,val):
        if val not in self:
            super(uniquelist,self).append(val)
            return True
        else:
            return False
    def extend(self,iterable):
        for temp in iterable: # todo: use yield so that it is not copied into memory
            self.append(temp)
    # Todo: Allow for type checking by allowing a type_of_members to be set
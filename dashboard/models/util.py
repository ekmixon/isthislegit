from google.appengine.ext import ndb

class DateTimeProperty(ndb.DateTimeProperty):
    def _get_for_dict(self, entity):
        value = super(DateTimeProperty, self)._get_for_dict(entity)
        return value.isoformat() if value else None

class DateProperty(ndb.DateProperty):
    def _get_for_dict(self, entity):
        value = super(DateProperty, self)._get_for_dict(entity)
        return str(value) if value else None

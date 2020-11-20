class OldDataMixin:
    attributes = {}

    def get_attributes(self):
        return self.attributes

    def __init__(self):
        self.request = None

    def post_old_data(self, name, value=''):
        return self.request.POST[name] if name in self.request.POST else value

    def get_old_data(self, name, value=''):
        return self.request.GET[name] if name in self.request.GET else value

    def get_all_olds_datas(self, context, attributes):
        for key, value in attributes.items():
            context[key] = self.get_old_data(key, value)

        return context

    def post_all_olds_datas(self, context, attributes):
        for key, value in attributes.items():
            context[key] = self.post_old_data(key, value)

        return context

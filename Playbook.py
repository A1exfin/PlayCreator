from Custom_widgets.Custom_list_item import CustomListItem
from Enum_flags import PlaybookType


class Playbook:
    def __init__(self, playbook_name: str, playbook_type: PlaybookType, from_server:  bool = False):
        self.id = None
        self.type = playbook_type
        self.name = playbook_name
        self.schemes = []

        self.chosen_list_item = None
        self.current_scene = None
        self.from_server = from_server############################

    def add_scheme(self, scheme: CustomListItem):
        self.schemes.append(scheme)

    def remove_scheme(self, scheme: CustomListItem):
        self.schemes.remove(scheme)

    def __repr__(self):
        return f'playbook_type: {self.type}, playbook_name: {self.name},\nplaybook_schemes: {self.schemes}'

    def return_data(self):
        return self.id, self.name, self.type
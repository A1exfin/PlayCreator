from List_item_custom import CustomListItem


class Playbook:
    def __init__(self, playbook_name: str, playbook_type: str, from_server:  bool):
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
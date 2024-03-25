from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Enums import PlaybookType
    from .ListWidgetItem_scheme import Scheme

__all__ = ['Playbook']


class Playbook:
    def __init__(self, playbook_name: str, playbook_type: 'PlaybookType',
                 playbook_id_pk: int = None, team_id_fk: int = None,
                 from_server:  bool = False):#########????????????????????????????????????????????????
        self.playbook_id_pk = playbook_id_pk
        self.team_id_fk = team_id_fk
        self.name = playbook_name
        self.type = playbook_type
        self.schemes = []

        self.chosen_list_item = None
        self.current_scene = None
        self.from_server = from_server############################

    def add_scheme(self, scheme: 'Scheme'):
        self.schemes.append(scheme)

    def remove_scheme(self, scheme: 'Scheme'):
        self.schemes.remove(scheme)

    def __repr__(self):
        return f'\n{self.__class__.__name__} (id_pk: {self.playbook_id_pk}; team_id_fk: {self.team_id_fk};' \
               f' type: {self.type}; name: {self.name}) at {hex(id(self))}\n\tplaybook_schemes: {self.schemes}'

    def return_data(self):
        return self.playbook_id_pk, self.team_id_fk, self.name, self.type
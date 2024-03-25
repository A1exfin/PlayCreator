import os
from PySide6.QtCore import Qt
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload
from DB_offline.database import engine
from DB_offline.models import UserSettingsORM, PlaybookORM, SchemeORM, PlayerORM, RectangleORM, EllipseORM, PencilLineORM, \
    LabelORM, LineORM, FinalActionArrowORM, FinalActionLineORM
from DB_offline.database import Base, session_factory, DATABASE_NAME
from Playbook_scheme.Playbook import Playbook
from Graphics import FinalActionArrow, FinalActionLine, ActionLine
from Enums import AppTheme


def drop_tables() -> None:
    Base.metadata.drop_all(engine)  # для отладки


def check_db_is_created() -> bool:
    return os.path.exists(f'{os.getcwd()}\{DATABASE_NAME}')


def create_db_if_not_exists() -> None:
    if not check_db_is_created():
        Base.metadata.create_all(engine)
        with session_factory() as session:
            default_user_settings = UserSettingsORM(maximized=False, toolbar_condition=True,
                                                    toolbar_area=Qt.ToolBarArea.TopToolBarArea, theme=AppTheme.dark)
            session.add(default_user_settings)
            session.commit()


def save_user_settings(settings_orm: 'UserSettingsORM', settings_data: tuple) -> None:
    with session_factory() as session:
        settings_orm.maximized, settings_orm.toolbar_condition, settings_orm.toolbar_area, settings_orm.theme = settings_data
        session.add(settings_orm)
        session.commit()


def get_user_settings() -> 'UserSettingsORM':
    with session_factory() as session:
        statement = select(UserSettingsORM).where(UserSettingsORM.settings_id_pk == 1)
        res = session.execute(statement)
        settings = res.scalars().all()[0]
        return settings


def save_new_playbook(playbook: 'Playbook', new_playbook_name: str | None = None) -> int:
    """Сохраняет новый плейбук. Вызывается при клике по кнопке 'сохранить',
     если в текущей сессии приложения нет ORM-модели плейбука, либо при клике по кнопке 'сохранить как...'
    При клике по кнопке 'сохранить как...' должно быть переданно имя(new_playbook_name) под которым будет сохранён
     текущий плейбук. Если это имя не было передано будет взято текущее имя плейбука из пользовательского интерфейса.
     Функция возвращает id сохранённого плейбука, который используется для получения ORM-модели сохранённого плейбука
      на основе которой обновляются id_pk и id_fk в объектах пользовательского интерфейса, для последующего корректного
       сохранения плейбука.
    """
    with session_factory() as session:
        playbook_id_pk, team_id_fk, playbook_name, playbook_type = playbook.return_data()
        playbook_orm = PlaybookORM(playbook_name=new_playbook_name if new_playbook_name else playbook_name,
                                   playbook_type=playbook_type,
                                   created_at=f'{datetime.now():%d.%m.%y %H:%M}',
                                   updated_at=f'{datetime.now():%d.%m.%y %H:%M}')
        session.add(playbook_orm)
        session.flush()
        for scheme in playbook.schemes:
            scheme_id_pk, playbook_id_fk, scheme_name, row_number, view_point_x, view_point_y,\
            first_team_placed, second_team_placed, first_team_position = scheme.return_data()
            scheme_orm = SchemeORM(playbook_id_fk=playbook_orm.playbook_id_pk, scheme_name=scheme_name, row_number=row_number,
                                   view_point_x=view_point_x, view_point_y=view_point_y,
                                   first_team_placed=first_team_placed, second_team_placed=second_team_placed, first_team_position=first_team_position)
            session.add(scheme_orm)
            session.flush()
            for rect in scheme.scene.rectangles:
                rect_id_pk, scheme_id_fk, x, y, width, height, border, border_thickness, border_color,\
                fill, fill_opacity, fill_color = rect.return_data()
                rect_orm = RectangleORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y, width=width, height=height,
                                        border=border, border_thickness=border_thickness, border_color=border_color,
                                        fill=fill, fill_opacity=fill_opacity, fill_color=fill_color)
                session.add(rect_orm)
            for ellipse in scheme.scene.ellipses:
                ellipse_id_pk, scheme_id_fk, x, y, width, height, border, border_thickness, border_color, \
                fill, fill_opacity, fill_color = ellipse.return_data()
                ellipse_orm = EllipseORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y, width=width, height=height,
                                         border=border, border_thickness=border_thickness, border_color=border_color,
                                         fill=fill, fill_opacity=fill_opacity, fill_color=fill_color)
                session.add(ellipse_orm)
            for pencil_line in scheme.scene.pencil:
                line_id_pk, scheme_id_fk, x1, y1, x2, y2, line_thickness, line_color = pencil_line.return_data()
                pencil_line_orm = PencilLineORM(scheme_id_fk=scheme_orm.scheme_id_pk, x1=x1, y1=y1, x2=x2, y2=y2,
                                                line_thickness=line_thickness, line_color=line_color)
                session.add(pencil_line_orm)
            for label in scheme.scene.labels:
                label_id_pk, scheme_id_fk, label_text, font_type, font_size,\
                font_bold, font_italic, font_underline, font_color, x, y, width, height = label.return_data()
                label_orm = LabelORM(scheme_id_fk=scheme_orm.scheme_id_pk, text=label_text, font_type=font_type,
                                     font_size=font_size, font_bold=font_bold, font_italic=font_italic,
                                     font_underline=font_underline, font_color=font_color, x=x, y=y, width=width, height=height)
                session.add(label_orm)
            for player in scheme.scene.first_team_players:
                player_id_pk, scheme_id_fk, x, y, team_type, player_position, current_action_number,\
                player_text, text_color, player_color, fill_type = player.return_data()
                first_team_player_orm = PlayerORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y, team_type=team_type,
                                                  player_position=player_position, current_action_number=current_action_number,
                                                  text=player_text, text_color=text_color, player_color=player_color, fill_type=fill_type)
                session.add(first_team_player_orm)
                session.flush()
                for action in player.actions.values():
                    for action_part in action:
                        if isinstance(action_part, FinalActionArrow):
                            arr_action_id_pk, player_id_fk, x, y, angle, line_thickness, line_color,\
                            action_number, action_type = action_part.return_data()
                            fa_arrow_orm = FinalActionArrowORM(player_id_fk=first_team_player_orm.player_id_pk, x=x, y=y, angle=angle,
                                                               line_thickness=line_thickness, line_color=line_color,
                                                               action_number=action_number, action_type=action_type)
                            session.add(fa_arrow_orm)
                        elif isinstance(action_part, FinalActionLine):
                            line_action_id_pk, player_id_fk, x, y, angle, line_thickness, line_color, \
                            action_number, action_type = action_part.return_data()
                            fa_line_orm = FinalActionLineORM(player_id_fk=first_team_player_orm.player_id_pk, x=x, y=y, angle=angle,
                                                             line_thickness=line_thickness, line_color=line_color,
                                                             action_number=action_number, action_type=action_type)
                            session.add(fa_line_orm)
                        else:
                            line_id_pk, player_id_fk, x1, y1, x2, y2, action_number,\
                            line_thickness, line_color, action_type = action_part.return_data()
                            action_line = LineORM(player_id_fk=first_team_player_orm.player_id_pk, x1=x1, y1=y1, x2=x2, y2=y2,
                                                  action_number=action_number, line_thickness=line_thickness,
                                                  line_color=line_color, action_type=action_type)
                            session.add(action_line)
            for player in scheme.scene.second_team_players:
                player_id_pk, scheme_id_fk, x, y, team_type, player_position, current_action_number,\
                player_text, text_color, player_color, symbol_type = player.return_data()
                second_team_player = PlayerORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y, team_type=team_type,
                                               player_position=player_position, current_action_number=current_action_number,
                                               text=player_text, text_color=text_color, player_color=player_color, symbol_type=symbol_type)
                session.add(second_team_player)
                session.flush()
                for action in player.actions.values():
                    for action_part in action:
                        if isinstance(action_part, FinalActionArrow):
                            arr_action_id_pk, player_id_fk, x, y, angle, line_thickness, line_color, \
                            action_number, action_type = action_part.return_data()
                            fa_arrow_orm = FinalActionArrowORM(player_id_fk=second_team_player.player_id_pk, x=x, y=y, angle=angle,
                                                               line_thickness=line_thickness, line_color=line_color,
                                                               action_number=action_number, action_type=action_type)
                            session.add(fa_arrow_orm)
                        elif isinstance(action_part, FinalActionLine):
                            line_action_id_pk, player_id_fk, x, y, angle, line_thickness, line_color, \
                            action_number, action_type = action_part.return_data()
                            fa_line_orm = FinalActionLineORM(player_id_fk=second_team_player.player_id_pk, x=x, y=y, angle=angle,
                                                             line_thickness=line_thickness, line_color=line_color,
                                                             action_number=action_number, action_type=action_type)
                            session.add(fa_line_orm)
                        else:
                            line_id_pk, player_id_fk, x1, y1, x2, y2, action_number, \
                            line_thickness, line_color, action_type = action_part.return_data()
                            action_line = LineORM(player_id_fk=second_team_player.player_id_pk, x1=x1, y1=y1, x2=x2, y2=y2,
                                                  action_number=action_number, line_thickness=line_thickness,
                                                  line_color=line_color, action_type=action_type)
                            session.add(action_line)
            if scheme.scene.additional_offence_player:
                player_id_pk, scheme_id_fk, x, y, team_type, player_position, current_action_number, \
                player_text, text_color, player_color, symbol_type = scheme.scene.additional_offence_player.return_data()
                additional_offence_player = PlayerORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y, team_type=team_type,
                                                      player_position=player_position, current_action_number=current_action_number,
                                                      text=player_text, text_color=text_color, player_color=player_color, fill_type=fill_type)
                session.add(additional_offence_player)
                session.flush()
                for action in scheme.scene.additional_offence_player.actions.values():
                    for action_part in action:
                        if isinstance(action_part, FinalActionArrow):
                            arr_action_id_pk, player_id_fk, x, y, angle, line_thickness, line_color, \
                            action_number, action_type = action_part.return_data()
                            fa_arrow_orm = FinalActionArrowORM(player_id_fk=additional_offence_player.player_id_pk, x=x, y=y, angle=angle,
                                                               line_thickness=line_thickness, line_color=line_color,
                                                               action_number=action_number, action_type=action_type)
                            session.add(fa_arrow_orm)
                        elif isinstance(action_part, FinalActionLine):
                            line_action_id_pk, player_id_fk, x, y, angle, line_thickness, line_color, \
                            action_number, action_type = action_part.return_data()
                            fa_line_orm = FinalActionLineORM(player_id_fk=additional_offence_player.player_id_pk, x=x, y=y, angle=angle,
                                                             line_thickness=line_thickness, line_color=line_color,
                                                             action_number=action_number, action_type=action_type)
                            session.add(fa_line_orm)
                        else:
                            line_id_pk, player_id_fk, x1, y1, x2, y2, action_number, \
                            line_thickness, line_color, action_type = action_part.return_data()
                            action_line = LineORM(player_id_fk=additional_offence_player.player_id_pk, x1=x1, y1=y1, x2=x2, y2=y2,
                                                  action_number=action_number, line_thickness=line_thickness,
                                                  line_color=line_color, action_type=action_type)
                            session.add(action_line)
        session.flush()
        session.commit()
        return playbook_orm.playbook_id_pk


def save_playbook(playbook: 'Playbook', playbook_orm: 'PlaybookORM') -> None:
    """Сохраняет текущий плейбук.
     Для сохранения сравнивается ORM-модель плейбука (playbook_orm), которую пользователь загрузил ранее с помощью пользовательского
     интерфейса, с текущим плейбуком (playbook), созданным в пользовательском интерфейсе на основе загруженной ORM-модели плейбука,
     в который пользователь мог внести изменения.
     Если какой-то объект был удалён, он удаляется из ORM-модели и в дальнейшем удаляется из БД.
     Если какой-то объект был изменён, он обновляется в ORM-модели и в дальнейшем обновляется в БД.
     Если был создан новый объект, создаётся новая ORM-модель и загружается в БД.
     """
    with session_factory() as session:
        if playbook_orm:
            playbook_orm.playbook_name, playbook_orm.playbook_type, playbook_orm.updated_at = playbook.name, playbook.type, f'{datetime.now():%d.%m.%y %H:%M}'
        else:
            playbook_orm = PlaybookORM(playbook_name=playbook.name, playbook_type=playbook.type,
                                       created_at=f'{datetime.now():%d.%m.%y %H:%M}',
                                       updated_at=f'{datetime.now():%d.%m.%y %H:%M}')
        session.add(playbook_orm)
        session.flush()
        for scheme in playbook.schemes.copy():
            if not scheme.is_deleted:  # При удалённой схеме нельзя возвратить номер строки,
                # потому что после удаления, из итема нет ссылки на виджет, в котором располагалась схема
                scheme_id_pk, playbook_id_fk, scheme_name, row_number, view_point_x, view_point_y, \
                first_team_placed, second_team_placed, first_team_position = scheme.return_data()
            if scheme in playbook_orm.schemes:
                # У класса scheme переопределён __eq__. Сравнение происходит по scheme_id_pk. У новых схем scheme_id_pk = None
                scheme_index = playbook_orm.schemes.index(scheme)
                scheme_orm = playbook_orm.schemes[scheme_index]
                if scheme.is_deleted:
                    playbook_orm.schemes.remove(scheme_orm)
                    playbook.schemes.remove(scheme)
                else:
                    scheme_orm.scheme_name, scheme_orm.row_number, scheme_orm.view_point_x, scheme_orm.view_point_y,\
                    scheme_orm.first_team_placed, scheme_orm.second_team_placed, scheme_orm.first_team_position = \
                        scheme_name, row_number, view_point_x, view_point_y, first_team_placed, second_team_placed, first_team_position
            else:
                scheme_orm = SchemeORM(playbook_id_fk=playbook_orm.playbook_id_pk, scheme_name=scheme_name,
                                       row_number=row_number, view_point_x=view_point_x, view_point_y=view_point_y,
                                       first_team_placed=first_team_placed, second_team_placed=second_team_placed,
                                       first_team_position=first_team_position)
                playbook_orm.schemes.append(scheme_orm)
                session.flush()  # новая созданная схема получает scheme_id_pk из БД
                # Изменяем атрибуты в объектах схем во вью для избежания дублирования схемы при повторном сохранении
                scheme.scheme_id_pk, scheme.playbook_id_fk = scheme_orm.scheme_id_pk, scheme_orm.playbook_id_fk
                scheme_index = playbook_orm.schemes.index(scheme_orm)
            if not scheme.is_deleted:
                # После удаления схемы из orm всё что было на сцене удаляется каскадно, поэтому удалять из orm вручную не нужно
                for rect in scheme.scene.rectangles.copy():
                    rect_id_pk, scheme_id_fk, x, y, width, height, border, border_thickness, border_color,\
                    fill, fill_opacity, fill_color = rect.return_data()
                    if rect in playbook_orm.schemes[scheme_index].rectangles:
                        rect_index = playbook_orm.schemes[scheme_index].rectangles.index(rect)
                        rect_orm = playbook_orm.schemes[scheme_index].rectangles[rect_index]
                        if rect.is_deleted:
                            playbook_orm.schemes[scheme_index].rectangles.remove(rect_orm)
                            scheme.scene.rectangles.remove(rect)
                        else:
                            rect_orm.x, rect_orm.y, rect_orm.width, rect_orm.height, rect_orm.border, rect_orm.border_thickness,\
                            rect_orm.border_color, rect_orm.fill, rect_orm.fill_opacity, rect_orm.fill_color =\
                                x, y, width, height, border, border_thickness, border_color, fill, fill_opacity, fill_color
                    else:
                        rect_orm = RectangleORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y, width=width, height=height,
                                                border=border, border_thickness=border_thickness, border_color=border_color,
                                                fill=fill, fill_opacity=fill_opacity, fill_color=fill_color)
                        scheme_orm.rectangles.append(rect_orm)
                        session.flush()
                        rect.rect_id_pk, rect.scheme_id_fk = rect_orm.rect_id_pk, rect_orm.scheme_id_fk
                for ellipse in scheme.scene.ellipses.copy():
                    ellipse_id_pk, scheme_id_fk, x, y, width, height, border, border_thickness, border_color, \
                    fill, fill_opacity, fill_color = ellipse.return_data()
                    if ellipse in playbook_orm.schemes[scheme_index].ellipses:
                        ellipse_index = playbook_orm.schemes[scheme_index].ellipses.index(ellipse)
                        ellipse_orm = playbook_orm.schemes[scheme_index].ellipses[ellipse_index]
                        if ellipse.is_deleted:
                            playbook_orm.schemes[scheme_index].ellipses.remove(ellipse_orm)
                            scheme.scene.ellipses.remove(ellipse)
                        else:
                            ellipse_orm.x, ellipse_orm.y, ellipse_orm.width, ellipse_orm.height,\
                            ellipse_orm.border, ellipse_orm.border_thickness, ellipse_orm.border_color, \
                            ellipse_orm.fill, ellipse_orm.fill_opacity, ellipse_orm.fill_color =\
                                x, y, width, height, border, border_thickness, border_color, fill, fill_opacity, fill_color
                    else:
                        ellipse_orm = EllipseORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y, width=width, height=height,
                                                 border=border, border_thickness=border_thickness, border_color=border_color,
                                                 fill=fill, fill_opacity=fill_opacity, fill_color=fill_color)
                        scheme_orm.ellipses.append(ellipse_orm)
                        session.flush()
                        ellipse.ellipse_id_pk, ellipse.scheme_id_fk = ellipse_orm.ellipse_id_pk, ellipse_orm.scheme_id_fk
                for pencil_line in scheme.scene.pencil.copy():
                    line_id_pk, scheme_id_fk, x1, y1, x2, y2, line_thickness, line_color = pencil_line.return_data()
                    if pencil_line in playbook_orm.schemes[scheme_index].pencil_lines:  # Возможно удалить, потому что линии не редактируются, их можно только удалить
                        pencil_line_index = playbook_orm.schemes[scheme_index].pencil_lines.index(pencil_line)
                        pencil_line_orm = playbook_orm.schemes[scheme_index].pencil_lines[pencil_line_index]
                        if pencil_line.is_deleted:
                            playbook_orm.schemes[scheme_index].pencil_lines.remove(pencil_line_orm)
                            scheme.scene.pencil.remove(pencil_line)
                        else:
                            pencil_line_orm.x1, pencil_line_orm.y1, pencil_line_orm.x2, pencil_line_orm.y2, \
                            pencil_line_orm.line_thickness, pencil_line_orm.line_color = x1, y1, x2, y2, line_thickness, line_color
                    else:
                        pencil_line_orm = PencilLineORM(scheme_id_fk=scheme_orm.scheme_id_pk, x1=x1, y1=y1, x2=x2, y2=y2,
                                                        line_thickness=line_thickness, line_color=line_color)
                        scheme_orm.pencil_lines.append(pencil_line_orm)
                        session.flush()
                        pencil_line.line_id_pk, pencil_line.scheme_id_fk = pencil_line_orm.line_id_pk, pencil_line_orm.scheme_id_fk
                for label in scheme.scene.labels.copy():
                    label_id_pk, scheme_id_fk, label_text, font_type, font_size, \
                    font_bold, font_italic, font_underline, font_color, x, y, width, height = label.return_data()
                    if label in playbook_orm.schemes[scheme_index].labels:
                        label_index = playbook_orm.schemes[scheme_index].labels.index(label)
                        label_orm = playbook_orm.schemes[scheme_index].labels[label_index]
                        if label.is_deleted:
                            playbook_orm.schemes[scheme_index].labels.remove(label_orm)
                            scheme.scene.labels.remove(label)
                        else:
                            label_orm.text, label_orm.font_type, label_orm.font_size,\
                            label_orm.font_bold, label_orm.font_italic, label_orm.font_underline, label_orm.font_color,\
                            label_orm.x, label_orm.y, label_orm.width, label_orm.height = \
                                label_text, font_type, font_size, font_bold, font_italic, font_underline, font_color, x, y, width, height
                    else:
                        label_orm = LabelORM(scheme_id_fk=scheme_orm.scheme_id_pk, text=label_text, font_type=font_type,
                                             font_size=font_size, font_bold=font_bold, font_italic=font_italic,
                                             font_underline=font_underline, font_color=font_color, x=x, y=y, width=width, height=height)
                        scheme_orm.labels.append(label_orm)
                        session.flush()
                        label.label_id_pk, label.scheme_id_fk = label_orm.label_id_pk, label_orm.scheme_id_fk
                for player in scheme.scene.first_team_players:
                    player_id_pk, scheme_id_fk, x, y, team_type, player_position, current_action_number, \
                    player_text, text_color, player_color, fill_type = player.return_data()
                    if player in playbook_orm.schemes[scheme_index].players:
                        orm_player_index = playbook_orm.schemes[scheme_index].players.index(player)
                        first_team_player_orm = playbook_orm.schemes[scheme_index].players[orm_player_index]
                        first_team_player_orm.x, first_team_player_orm.y, first_team_player_orm.team_type,\
                        first_team_player_orm.player_position, first_team_player_orm.current_action_number, \
                        first_team_player_orm.text, first_team_player_orm.text_color, first_team_player_orm.player_color, \
                        first_team_player_orm.fill_type =\
                            x, y, team_type, player_position, current_action_number, player_text, text_color, player_color, fill_type
                    else:
                        first_team_player_orm = PlayerORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y,
                                                          team_type=team_type, player_position=player_position,
                                                          current_action_number=current_action_number,
                                                          text=player_text, text_color=text_color,
                                                          player_color=player_color, fill_type=fill_type)
                        scheme_orm.players.append(first_team_player_orm)
                        session.flush()
                        player.player_id_pk, player.scheme_id_fk = first_team_player_orm.player_id_pk, first_team_player_orm.scheme_id_fk
                    compare_orm_model_and_view_for_action_parts(session, player, first_team_player_orm)
                if scheme.scene.deleted_first_team_players:  # Действия для данных игроков будут удалены каскадно, поэтому для них не нужно отдельно удалять/обновлять действия
                    for deleted_first_team_player in scheme.scene.deleted_first_team_players:
                        if deleted_first_team_player in playbook_orm.schemes[scheme_index].players:
                            orm_deleted_f_t_player_index = playbook_orm.schemes[scheme_index].players.index(deleted_first_team_player)
                            playbook_orm.schemes[scheme_index].players.pop(orm_deleted_f_t_player_index)
                    scheme.scene.deleted_first_team_players.clear()
                for player in scheme.scene.second_team_players:
                    player_id_pk, scheme_id_fk, x, y, team_type, player_position, current_action_number, \
                    player_text, text_color, player_color, symbol_type = player.return_data()
                    if player in playbook_orm.schemes[scheme_index].players:
                        orm_player_index = playbook_orm.schemes[scheme_index].players.index(player)
                        second_team_player_orm = playbook_orm.schemes[scheme_index].players[orm_player_index]
                        second_team_player_orm.x, second_team_player_orm.y, second_team_player_orm.team_type,\
                        second_team_player_orm.player_position, second_team_player_orm.current_action_number, \
                        second_team_player_orm.text, second_team_player_orm.text_color, second_team_player_orm.player_color, \
                        second_team_player_orm.symbol_type =\
                            x, y, team_type, player_position, current_action_number, player_text, text_color, player_color, symbol_type
                    else:
                        second_team_player_orm = PlayerORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y,
                                                           team_type=team_type, player_position=player_position,
                                                           current_action_number=current_action_number,
                                                           text=player_text, text_color=text_color,
                                                           player_color=player_color, symbol_type=symbol_type)
                        scheme_orm.players.append(second_team_player_orm)
                        session.flush()
                        player.player_id_pk, player.scheme_id_fk = second_team_player_orm.player_id_pk, second_team_player_orm.scheme_id_fk
                    compare_orm_model_and_view_for_action_parts(session, player, second_team_player_orm)
                if scheme.scene.deleted_second_team_players:
                    for deleted_second_team_player in scheme.scene.deleted_second_team_players:
                        if deleted_second_team_player in playbook_orm.schemes[scheme_index].players:
                            orm_deleted_s_t_player_index = playbook_orm.schemes[scheme_index].players.index(deleted_second_team_player)
                            playbook_orm.schemes[scheme_index].players.pop(orm_deleted_s_t_player_index)
                    scheme.scene.deleted_second_team_players.clear()
                if scheme.scene.additional_offence_player:
                    player_id_pk, scheme_id_fk, x, y, team_type, player_position, current_action_number, \
                    player_text, text_color, player_color, fill_type = scheme.scene.additional_offence_player.return_data()
                    if scheme.scene.additional_offence_player in playbook_orm.schemes[scheme_index].players:
                        orm_player_index = playbook_orm.schemes[scheme_index].players.index(scheme.scene.additional_offence_player)
                        additional_offence_player_orm = playbook_orm.schemes[scheme_index].players[orm_player_index]
                        additional_offence_player_orm.x, additional_offence_player_orm.y, additional_offence_player_orm.team_type, \
                        additional_offence_player_orm.player_position, additional_offence_player_orm.current_action_number, \
                        additional_offence_player_orm.text, additional_offence_player_orm.text_color, additional_offence_player_orm.player_color, \
                        additional_offence_player_orm.fill_type = \
                            x, y, team_type, player_position, current_action_number, player_text, text_color, player_color, fill_type
                    else:
                        additional_offence_player_orm = PlayerORM(scheme_id_fk=scheme_orm.scheme_id_pk, x=x, y=y,
                                                                  team_type=team_type, player_position=player_position,
                                                                  current_action_number=current_action_number,
                                                                  text=player_text, text_color=text_color,
                                                                  player_color=player_color, fill_type=fill_type)
                        scheme_orm.players.append(additional_offence_player_orm)
                        session.flush()
                        scheme.scene.additional_offence_player.player_id_pk, scheme.scene.additional_offence_player.scheme_id_fk \
                            = additional_offence_player_orm.player_id_pk, additional_offence_player_orm.scheme_id_fk
                    compare_orm_model_and_view_for_action_parts(session, scheme.scene.additional_offence_player, additional_offence_player_orm)
                if scheme.scene.deleted_additional_offence_player:
                    if scheme.scene.deleted_additional_offence_player in playbook_orm.schemes[scheme_index].players:
                        orm_deleted_add_player_index = playbook_orm.schemes[scheme_index].players.index(scheme.scene.deleted_additional_offence_player)
                        playbook_orm.schemes[scheme_index].players.pop(orm_deleted_add_player_index)
                    scheme.scene.deleted_additional_offence_player = None
        session.flush()
        session.commit()
        # return playbook_orm


def compare_orm_model_and_view_for_action_parts(session: 'session_factory', view_player, orm_player: 'PlayerORM') -> None:
    for action in view_player.actions.values():
        for action_part in action:
            if isinstance(action_part, FinalActionArrow):
                arr_action_id_pk, player_id_fk, x, y, angle, line_thickness, line_color, \
                action_number, action_type = action_part.return_data()
                if action_part in orm_player.action_finishes_arr:
                    fa_arrow_orm_index = orm_player.action_finishes_arr.index(action_part)
                    fa_arrow_orm = orm_player.action_finishes_arr[fa_arrow_orm_index]
                    fa_arrow_orm.x, fa_arrow_orm.y, fa_arrow_orm.angle, \
                    fa_arrow_orm.line_thickness, fa_arrow_orm.line_color, \
                    fa_arrow_orm.action_number, fa_arrow_orm.action_type = \
                        x, y, angle, line_thickness, line_color, action_number, action_type
                else:
                    fa_arrow_orm = FinalActionArrowORM(player_id_fk=orm_player.player_id_pk, x=x, y=y, angle=angle,
                                                       line_thickness=line_thickness, line_color=line_color,
                                                       action_number=action_number, action_type=action_type)
                    orm_player.action_finishes_arr.append(fa_arrow_orm)
                    session.flush()
                    action_part.f_arr_action_id_pk, action_part.player_id_fk = \
                        fa_arrow_orm.arr_finish_id_pk, fa_arrow_orm.player_id_fk
            elif isinstance(action_part, FinalActionLine):
                line_action_id_pk, player_id_fk, x, y, angle, line_thickness, line_color, \
                action_number, action_type = action_part.return_data()
                if action_part in orm_player.action_finishes_line:
                    fa_line_orm_index = orm_player.action_finishes_line.index(action_part)
                    fa_line_orm = orm_player.action_finishes_line[fa_line_orm_index]
                    fa_line_orm.x, fa_line_orm.y, fa_line_orm.angle, \
                    fa_line_orm.line_thickness, fa_line_orm.line_color, \
                    fa_line_orm.action_number, fa_line_orm.action_type = \
                        x, y, angle, line_thickness, line_color, action_number, action_type
                else:
                    fa_line_orm = FinalActionLineORM(player_id_fk=orm_player.player_id_pk, x=x, y=y, angle=angle,
                                                     line_thickness=line_thickness, line_color=line_color,
                                                     action_number=action_number, action_type=action_type)
                    orm_player.action_finishes_line.append(fa_line_orm)
                    session.flush()
                    action_part.f_line_action_id_pk, action_part.player_id_fk = \
                        fa_line_orm.line_finish_id_pk, fa_line_orm.player_id_fk
            else:
                line_id_pk, player_id_fk, x1, y1, x2, y2, action_number, \
                line_thickness, line_color, action_type = action_part.return_data()
                if action_part in orm_player.lines:
                    action_line_index = orm_player.lines.index(action_part)
                    action_line_orm = orm_player.lines[action_line_index]
                    action_line_orm.x1, action_line_orm.y1, action_line_orm.x2, action_line_orm.y2,\
                    action_line_orm.action_number, action_line_orm.line_thickness,\
                    action_line_orm.line_color, action_line_orm.action_type = \
                        x1, y1, x2, y2, action_number, line_thickness, line_color, action_type
                else:
                    action_line_orm = LineORM(player_id_fk=orm_player.player_id_pk, x1=x1, y1=y1, x2=x2, y2=y2,
                                              action_number=action_number, line_thickness=line_thickness,
                                              line_color=line_color, action_type=action_type)
                    orm_player.lines.append(action_line_orm)
                    session.flush()
                    action_part.line_id_pk, action_part.player_id_fk = \
                        action_line_orm.line_id_pk, action_line_orm.player_id_fk
    if view_player.deleted_action_parts:
        for deleted_action_part in view_player.deleted_action_parts:
            if isinstance(deleted_action_part, FinalActionArrow) and deleted_action_part in orm_player.action_finishes_arr:
                orm_deleted_f_a_arrow_index = orm_player.action_finishes_arr.index(deleted_action_part)
                orm_player.action_finishes_arr.pop(orm_deleted_f_a_arrow_index)
            elif isinstance(deleted_action_part, FinalActionLine) and deleted_action_part in orm_player.action_finishes_line:
                orm_deleted_f_a_line_index = orm_player.action_finishes_line.index(deleted_action_part)
                orm_player.action_finishes_line.pop(orm_deleted_f_a_line_index)
            elif isinstance(deleted_action_part, ActionLine) and deleted_action_part in orm_player.lines:
                orm_deleted_line_index = orm_player.lines.index(deleted_action_part)
                orm_player.lines.pop(orm_deleted_line_index)
        view_player.deleted_action_parts.clear()


def select_playbook(playbook_id: int) -> 'PlaybookORM':
    with session_factory() as session:
        statement = (
            select(PlaybookORM).where(PlaybookORM.playbook_id_pk == playbook_id)
            .options(selectinload(PlaybookORM.schemes)
                     .options(selectinload(SchemeORM.ellipses), selectinload(SchemeORM.rectangles),
                              selectinload(SchemeORM.labels), selectinload(SchemeORM.pencil_lines),
                              selectinload(SchemeORM.players)
                              .options(selectinload(PlayerORM.lines),
                                       selectinload(PlayerORM.action_finishes_arr),
                                       selectinload(PlayerORM.action_finishes_line)
                                       )
                              )
                     )
        )
        res = session.execute(statement)
        playbook = res.unique().scalars().all()[0]
        return playbook


def get_playbook_info() -> list[tuple]:
    with session_factory() as session:
        query = text('SELECT playbook_id_pk, playbook_name, playbook_type, updated_at, created_at FROM playbooks')
        res = session.execute(query)
        return res.all()


def delete_playbook(playbook_id: int) -> None:
    with session_factory() as session:
        statement = (
            select(PlaybookORM).where(PlaybookORM.playbook_id_pk == playbook_id)
            .options(selectinload(PlaybookORM.schemes)
                     .options(selectinload(SchemeORM.ellipses), selectinload(SchemeORM.rectangles),
                              selectinload(SchemeORM.labels), selectinload(SchemeORM.pencil_lines),
                              selectinload(SchemeORM.players)
                              .options(selectinload(PlayerORM.lines),
                                       selectinload(PlayerORM.action_finishes_arr),
                                       selectinload(PlayerORM.action_finishes_line)
                                       )
                              )
                     )
        )
        res = session.execute(statement)
        playbook = res.unique().scalars().all()[0]
        session.delete(playbook)
        session.commit()

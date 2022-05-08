from aiogram.types.inline_keyboard import InlineKeyboardMarkup as IMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton as IButton
from enum import Enum


class CallBackDatas(Enum):
    """
    3 класса, у каждого свой номер, меню содержит номер класса к которому относится
    """
    # People class
    abits = -1
    students = 0
    teachs = 1
    abits_ = {'text_': 'Абитурент',
              'menu_text': 'Меню абитуриенту'}
    students_ = {'text_': 'Студент',
                 'menu_text': 'Меню студенту'}
    teachs_ = {'text_': 'Учитель',
               'menu_text': 'Меню учителю'}
    #############
    # Abiturents`s Enums
    ab_instruction = {'people_class': -1,
                      'url': 'https://rbmed03.ru/?page_id=26560',
                      'menu_text': 'Инструкция по регистрации в ЛК абитуриента',
                      'start_text': 'Инструкция по регистрации в ЛК абитуриента.\nУдачи с поступлением:)'}
    commission = {'people_class': -1,
                  'url': 'https://rbmed03.ru/?page_id=3390',
                  'start_text': 'Приемная комиссия',
                  'text': {'func': 'commission_parsing'}}
    plan_priem = {'people_class': -1,
                  'url': 'https://rbmed03.ru/?page_id=46',
                  'start_text': 'План прима в колледж', }
    perech_dok = {'people_class': -1,
                  'url': 'https://rbmed03.ru/?page_id=6741',
                  'start_text': 'Перечень документов для поступления',
                  'text': {'func': 'perech_dok_parser'}}
    preskur_plat = {'people_class': -1,
                    'url': 'https://rbmed03.ru/?page_id=6745',
                    'menu_text': 'Прейскурант платных услуг по специальностям',
                    'start_text': 'Cтоимость обучения в РБМК на договорной основе'}
    zaselenie = {'people_class': -1,
                 'url': 'https://rbmed03.ru/?page_id=26161',
                 'start_text': 'О заселении в общежитие',
                 'text': {'func': 'zaselenie_parser'}}
    med_osmotr = {'people_class': -1,
                  'url': 'https://rbmed03.ru/?page_id=26175',
                  'menu_text': 'Прохождения обязательного предварительного мед. Осмотра',
                  'start_text': 'Информация о необходимости прохождения обязательного предварительного мед. Осмотра'}
    specialnosti = {'people_class': -1,
                    'url': 'https://rbmed03.ru/',
                    'start_text': 'Описание специальностей',
                    'keyboard': {'func': 'specialnosti_parser'}}
    raspisanya_rez = {'people_class': -1,
                      'url': 'https://rbmed03.ru/?page_id=8695',
                      'start_text': 'Расписание результатов вступительных испытаний и собеседования'}
    prof_teach = {'people_class': -1,
                  'url': 'https://rbmed03.ru/?page_id=18183',
                  'menu_text': 'Профессиональное обучение и переподготовка',
                  'start_text': '',
                  'text': {'func': 'prof_teach_text'},
                  'keyboard': {'func': 'prof_teach_keyboard'}}
    project = {'people_class': -1,
               'url': 'https://rbmed03.ru/?page_id=27347',
               'start_text': 'Проект приказа на зачисление'}
    ######################################
    # Students Enums
    pamyatka = {'people_class': 0,
                'url': 'https://rbmed03.ru/?page_id=20806',
                'menu_text': 'Памятка первокурснику',
                'start_text': 'Какой раздел вас интересуетт?',
                'keyboard': {'func': 'pamyatka_keyboard'}}
    rabochie_materiali_PAS = {'people_class': 0,
                              'url': 'https://rbmed03.ru/?page_id=12191',
                              'start_text': 'Рабочие материалы для ПАС'}
    raspisanya = {'people_class': 0,
                  'start_text': 'Расписание',
                  'helpers': {'type': 'rasp'}}
    oplata = {'people_class': 0,
              'start_text': 'Оплата за обучение',
              'url': 'https://rbmed03.ru/?page_id=18645',
              'text': {'func': 'oplata_parser'}}
    gia_vkr = {'people_class': 0,
               'menu_text': 'ГИА и ВКР',
               'start_text': 'Узнать программы ГИА и темы ВКР',
               'url': 'https://rbmed03.ru/?page_id=15593'}
    graphik_practice = {'people_class': 0,
                        'menu_text': 'График производственной и преддипломной практики',
                        'start_text': '(Узнать график производственной и преддипломной практики',
                        'url': 'https://rbmed03.ru/?page_id=6123'}
    med_student = {'people_class': 0,
                   'menu_text': 'Медосмотр студентов',
                   'start_text': 'Узнать график прохождения медосмотра',
                   'url': 'https://rbmed03.ru/?page_id=21318'}
    zakaz_spravki = {'people_class': 0,
                     'start_text': 'Заказать справку онлайн',
                     'url': 'https://rbmed03.ru/?page_id=18653',
                     'keyboard': {'func': 'zakaz_spravki'}}
    vipuskniku = {'people_class': 0,
                  'start_text': 'Выпускнику',
                  'helper': 'vipuskniku'
                  }
    ######################################
    # Submenus Enums(students)

    ########
    helpers = {'rasp': {'type': 'rasp', 'elements': [
        {'menu_text': 'Расписание звонков',
         'name': 'rasp_zvonkov',
         'send_func': 'rasp_zvonkov'},
        {'menu_text': 'Расписание по группам',
         'name': 'group_rasp',
         'send_func': 'group_rasp'},
        {'menu_text': 'Расписание по преподавателям',
         'name': 'teach_rasp',
         'send_func': 'teach_rasp'},
        {'menu_text': 'Расписание по аудитории',
         'name': 'audit_rasp',
         'send_func': 'audit_rasp'}]},
               'vipuskniku': {'type': 'leveler_keyboard', 'elements': {
                   'pervich': {'menu_text': 'Первичная аккредитация специалиста',
                               'type': 'keyboard',
                               'inner_text': 'Вы можете уже подавать документы на электронный адрес аккредитационной '
                                             'комиссии '
                                             'top-akkredo@mail.ru с обязательным указанием действующего номера '
                                             'телефона и '
                                             'индекса по прописке, указанием какая аккредитация и специальность.',
                               'url': 'https://rbmed03.ru/?page_id=20470'},
                   'dop_podgotovka': {'menu_text': 'Дополнительная подготовка для трудоустройства',
                                      'type': 'l_keyboard',
                                      'inner_text': 'Дополнительная подготовка для трудоустройства',
                                      'sub_menu': {
                                          'reg_nmo': {'menu_text': 'Регистрация на портале НМО',
                                                      'inner_text': 'Необходимо зарегистрироваться  по этой инструкции',
                                                      'url': 'https://rbmed03.ru/?page_id=19484'},
                                          'next_steps': {'menu_text': 'Ваши дальнейшие действия',
                                                         'inner_text': 'Узнать подробнее о ваших дальнейших действиях',
                                                         'url': 'https://rbmed03.ru/?page_id=19469'}
                                      }
                                      }
               }}}

    @classmethod
    def all_en_name(cls, option=None):
        if option:
            return [en.name for en in cls if isinstance(en.value, dict) and en.value[option['key']] == option['value']]
        return [en.name for en in cls]

    @classmethod
    def get_by_name(cls, name: str):
        for en in cls:
            if en.name == name:
                return en

    @classmethod
    def get_people_class(cls, value: int):
        if value == -1:
            return cls.abits, cls.abits_
        if value == 0:
            return cls.students, cls.students_
        if value == 1:
            return cls.teachs, cls.teachs_
        raise TypeError('Not int')


class KeyBoards:
    '''
    Включает все клавиатуры программы.
    '''

    @staticmethod
    def get_keyboards(*btns, back_button: str = None,
                      about_button: str = None, **kwargs):
        """
        Создание клавиатуры
        :param btns: Совокупность настроек для кнопок
        :param kwargs: Настройки клавиатуры
        :return: KeyboardMarkup
        """
        markup = IMarkup(**kwargs)
        for button in btns:
            """
            :params:
                text,
                url[Optional],
                callback_data[Optional]...
            """
            markup.add(IButton(**button))
        if about_button:
            markup.add(IButton(text='Подробнее', url=about_button))
        if back_button:
            markup.add(IButton(text='Назад', callback_data=back_button))
        return markup

    @classmethod
    def welcome_keyboard(cls):
        return cls.get_keyboards(
            {'text': 'Абитуриенту', 'callback_data': CallBackDatas.abits.value},
            {'text': 'Студенту', 'callback_data': CallBackDatas.students.value},
            {'text': 'Преподавателю', 'callback_data': CallBackDatas.teachs.value}
        )

    @classmethod
    def class_menu(cls, clas: CallBackDatas):
        return cls.get_keyboards(
            *[{'text': en.value.get('menu_text', en.value['start_text']), 'callback_data': en.name} for en in
              CallBackDatas
              if isinstance(en.value, dict) and en.value.get('people_class', '') == clas.value], back_button='start'
        )

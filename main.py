import asyncio
import aioschedule as schedule
from aiogram.types import Message
from aiogram.bot import Bot
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher,FSMContext
from aiogram.types.callback_query import CallbackQuery
import configparser
from database import UserModel, close_db
from keyboards import KeyBoards, CallBackDatas
from info_parser import Parser
from utils import SendFuncs



# Подключение конфиг файла
bot_cfg = configparser.ConfigParser()
bot_cfg.read('bot.cfg')
# Получение информации с конфига
TOKEN = bot_cfg.get('UniBot', 'token')  # Токен

# Иницализация основных компонентов бота
main_loop = asyncio.new_event_loop()
asyncio.set_event_loop(main_loop)
parser = Parser(loop=main_loop)
bot = Bot(TOKEN, parse_mode='html', loop=main_loop)
storage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot, loop=main_loop, storage=storage)
schedule.every().day.do(parser.get_htmls,message='Parsing started')
main_loop.run_until_complete(parser.get_htmls())


def get_usr(object) -> UserModel:
    if isinstance(object, Message):
        return UserModel.get_by_id(object.chat.id)
    else:
        return UserModel.get_by_id(object.message.chat.id)


def get_chat_id(object) -> int | str:
    if isinstance(object, Message):
        return object.chat.id
    else:
        return object.message.chat.id


def save_last_message(usr: UserModel, message: Message):
    usr.last_message_id = message.message_id
    usr.save()


def render_leveler_keyboard(elements: dict, back, name=None):
    return KeyBoards.get_keyboards(*[{'text': el.get('menu_text'),
                                      'callback_data': name + '*' + name_el}
                                     for name_el, el in elements.items()],
                                   back_button=back)


@dp.message_handler(commands=['start'],state='*')
@dp.callback_query_handler(lambda query: query.data == 'start')
async def welcome(message):
    usr = get_usr(message)
    chat_id = get_chat_id(message)
    if usr.last_message_id is not None:
        try:
            await bot.delete_message(chat_id, usr.last_message_id)
        except MessageToDeleteNotFound:
            pass
    msg: Message = await bot.send_message(chat_id, 'Приветствуем!', reply_markup=KeyBoards.welcome_keyboard())
    save_last_message(usr, msg)


@dp.message_handler(state='*')
async def get_info(message: Message,state: FSMContext):
    usr = get_usr(message)
    func_name = (await state.get_data()).get('func_name')
    func = SendFuncs.get_method_by_name(func_name)
    await func(bot, message, usr,state)


@dp.callback_query_handler(lambda query: query.data in ['-1', '0', '1'])
async def menus(query: CallbackQuery):
    usr = get_usr(query)
    people_class, class_text = CallBackDatas.get_people_class(int(query.data))
    usr.people_class = people_class.value
    try:
        await bot.delete_message(query.message.chat.id, usr.last_message_id)
    except:
        pass
    msg: Message = await bot.send_message(query.message.chat.id, text=class_text.value['menu_text'],
                                          reply_markup=KeyBoards.class_menu(people_class))
    save_last_message(usr, msg)
    usr.that = str(people_class.value)
    usr.save()


# Menus
########################################################################################
@dp.callback_query_handler(lambda query: query.data in CallBackDatas.all_en_name())
async def instruction(query: CallbackQuery):
    usr = get_usr(query)
    menu = CallBackDatas.get_by_name(query.data)

    if menu.value.get('helper', False):
        helper = CallBackDatas.helpers.value.get(menu.value.get('helper'))
        if helper['type'] == 'leveler_keyboard':
            keyboard = render_leveler_keyboard(helper['elements'],
                                               usr.that,
                                               menu.value.get('helper'),
                                               )
        if helper['type'] == 'rasp':
            keyboard = KeyBoards.get_keyboards(*[{'text':el['menu_text'],'callback_data':'rasp-'+el['send_func']}
                for el in CallBackDatas.helpers.value['rasp']['elements']],back_button=usr.that)

    elif not menu.value.get('keyboard', False):
        keyboard = KeyBoards.get_keyboards(
            back_button=usr.that,
            about_button=menu.value['url']
        )
    else:
        keyboard_settings = await parser.get_method_by_name(menu.value['keyboard'].get('func'))()
        keyboard = KeyBoards.get_keyboards(*keyboard_settings.get('args'),
                                           **keyboard_settings.get('kwargs'),
                                           back_button=usr.that)
    text = f'{menu.value["start_text"]}'

    if menu.value.get('text', False):
        func_name = menu.value.get('text').get('func')
        text += '\n' + await Parser.get_method_by_name(func_name)()

    await bot.delete_message(query.message.chat.id, usr.last_message_id)
    msg: Message = await bot.send_message(query.message.chat.id, text,
                                          reply_markup=keyboard)
    save_last_message(usr, msg)


#####################################################################
@dp.callback_query_handler(lambda query: query.data.startswith('rasp'))
async def rasp_menu(query: CallbackQuery,state: FSMContext):
    usr = get_usr(query)
    func_name = query.data.split('-')[1]
    func = SendFuncs.get_method_by_name(func_name)
    await func(bot,query,usr,state)


#####################################################################
@dp.callback_query_handler(lambda query: query.data.startswith('done_rasp'))
async def done_rasp(query: CallbackQuery):
    usr = get_usr(query)
    rasp = await parser.rasp_parser(query.data.split('-')[2],
                              query.data.split('-')[1],
                              usr.get_by_name(query.data.split('-')[1]))
    await bot.delete_message(query.message.chat.id,usr.last_message_id)
    msg: Message = await bot.send_message(query.message.chat.id,
                                          'Расписание:\n'+rasp,
                                          reply_markup=KeyBoards.get_keyboards(
                                              back_button='raspisanya'
                                          ))
    save_last_message(usr,msg)
###########################################################


@dp.callback_query_handler(lambda query: query.data.startswith('change'))
async def change_rasp(query: CallbackQuery,state: FSMContext):
    usr = get_usr(query)
    value = query.data.split('_')[1]
    if value == 'group':
        usr.group = None
    if value == 'audit':
        usr.audit = None
    if value == 'teach':
        usr.teach = None
    usr.save()
    func_name = value+'_rasp'
    func = SendFuncs.get_method_by_name(func_name)
    await func(bot, query, usr, state)


@dp.callback_query_handler(lambda query: len(query.data.split('*'))>2)
async def sub_menus(query: CallbackQuery):
    usr = get_usr(query)
    helper_name = query.data.split('*')[0]
    name = query.data.split('*')[1]
    sub_name = query.data.split('*')[2]
    section = CallBackDatas.helpers.value.get(helper_name)\
        .get('elements')\
        .get(name)\
        .get('sub_menu')\
        .get(sub_name)
    await bot.delete_message(query.message.chat.id,usr.last_message_id)
    msg: Message = await bot.send_message(query.message.chat.id,
                                          section['inner_text'],
                                          reply_markup=KeyBoards.get_keyboards(
                                                about_button=section['url'],
                                              back_button='*'.join(query.data.split('*')[:2])
                                          ))
    save_last_message(usr,msg)


@dp.callback_query_handler(lambda query: query.data.split('*')[0] in CallBackDatas.helpers.value.keys())
async def render_leveler_menu(query: CallbackQuery):
    usr = get_usr(query)
    helper_name = query.data.split('*')[0]
    name = query.data.split('*')[1]
    section = CallBackDatas.helpers.value.get(helper_name).get('elements').get(name)
    type = section['type']
    await bot.delete_message(query.message.chat.id, usr.last_message_id)
    if type == 'keyboard':
        msg: Message = await bot.send_message(query.message.chat.id, section['inner_text'],
                                              reply_markup=KeyBoards.
                                              get_keyboards(
                                                  about_button=section['url'],
                                                  back_button=query.data.split('*')[0]
                                              ))
    if type == 'l_keyboard':
        msg: Message = await bot.send_message(query.message.chat.id,
                                              section['inner_text'],
                                              reply_markup=render_leveler_keyboard(
                                                  section['sub_menu'],
                                                  back=query.data.split('*')[0],
                                                  name=query.data
                                              ))
    save_last_message(usr,msg)

if __name__ == "__main__":
    executor.Executor(dispatcher=dp, skip_updates=True, loop=main_loop).start_polling()
    close_db()



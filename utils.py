from aiogram.bot import Bot
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
import aiohttp
from database import UserModel
from keyboards import KeyBoards
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


def get_chat_id(object) -> int | str:
    if isinstance(object, Message):
        return object.chat.id
    else:
        return object.message.chat.id


class RaspState(StatesGroup):
    get_info = State()


class SendFuncs:

    @staticmethod
    async def rasp_zvonkov(
            bot: Bot,
            query: CallbackQuery|Message,
            usr: UserModel,
            state: FSMContext
    ):
        await bot.delete_message(query.message.chat.id,usr.last_message_id)
        msg: Message = await bot.send_photo(query.message.chat.id,
                             'https://rbmed03.ru/wp-content/uploads/2018/01/звонки.jpg',
                             reply_markup=KeyBoards.get_keyboards(back_button='raspisanya'))
        usr.last_message_id = msg.message_id
        usr.save()

    @staticmethod
    async def group_rasp(
            bot: Bot,
            query: CallbackQuery|Message,
            usr: UserModel,
            state: FSMContext
    ):
        if usr.group is None:
            if isinstance(query,Message):
                if len(query.text.splitlines())==1:
                    usr.group = query.text.strip()
                    await state.finish()
                    await bot.delete_message(query.chat.id, query.message_id)
                    msg: Message = await query.answer('Какое расписание вы хотите увидеть?',
                                                      reply_markup=KeyBoards.get_keyboards(
                                                          {'text':'На неделю','callback_data':'done_rasp-group-ned'},
                                                          {'text':'На сегодня','callback_data':'done_rasp-group-day'},
                                                          {'text':f'Указать другую группу(сейчас: {usr.group})',
                                                           'callback_data':'change_group'}
                                                      ))
                    usr.last_message_id = msg.message_id
                else:
                    await bot.delete_message(query.chat.id,query.message_id)
                    await query.answer('Группа введена неверно')
                    return

            else:
                await bot.delete_message(query.message.chat.id, usr.last_message_id)
                msg: Message = await bot.send_message(query.message.chat.id,
                                                      'Введите номер группы')
                usr.last_message_id = msg.message_id
                await state.set_state(RaspState.get_info.state)
                await state.set_data({'func_name':'group_rasp'})
        else:
            chat_id = get_chat_id(query)
            await bot.delete_message(chat_id,usr.last_message_id)
            msg: Message = await bot.send_message(query.from_user.id,'Какое расписание вы хотите увидеть?',
                                              reply_markup=KeyBoards.get_keyboards(
                                                  {'text': 'На неделю', 'callback_data': 'done_rasp-group-ned'},
                                                  {'text': 'На сегодня', 'callback_data': 'done_rasp-group-day'},
                                                  {'text': f'Указать другую группу(сейчас: {usr.group})',
                                                   'callback_data': 'change_group'}
                                              ))
            usr.last_message_id = msg.message_id
            await state.finish()
        usr.save()

    @staticmethod
    async def teach_rasp(
            bot: Bot,
            query: CallbackQuery|Message,
            usr: UserModel,
            state: FSMContext
    ):
        if usr.teach is None:
            if isinstance(query, Message):
                if len(query.text.splitlines()) == 1:
                    usr.teach = query.text.strip()
                    await state.finish()
                    await bot.delete_message(query.chat.id, query.message_id)
                    msg: Message = await query.answer('Какое расписание вы хотите увидеть?',
                                                      reply_markup=KeyBoards.get_keyboards(
                                                          {'text': 'На неделю', 'callback_data': 'done_rasp-teach-ned'},
                                                          {'text': 'На сегодня', 'callback_data': 'done_rasp-teach-day'},
                                                          {'text': f'Указать другую группу(сейчас: {usr.teach})',
                                                           'callback_data': 'change_teach'}
                                                      ))
                    usr.last_message_id = msg.message_id
                else:
                    await bot.delete_message(query.chat.id, query.message_id)
                    await query.answer('Учитель введен неверно введена неверно')
                    return
            else:
                await bot.delete_message(query.message.chat.id, usr.last_message_id)
                msg: Message = await bot.send_message(query.message.chat.id,
                                                      'Введите учителя')
                usr.last_message_id = msg.message_id
                await state.set_state(RaspState.get_info.state)
                await state.set_data({'func_name': 'teach_rasp'})
        else:
            await bot.delete_message(query.message.chat.id, usr.last_message_id)
            msg: Message = await bot.send_message(query.from_user.id,'Какое расписание вы хотите увидеть?',
                                              reply_markup=KeyBoards.get_keyboards(
                                                  {'text': 'На неделю', 'callback_data': 'done_rasp-teach-ned'},
                                                  {'text': 'На сегодня', 'callback_data': 'done_rasp-teach-day'},
                                                  {'text': f'Указать другую группу(сейчас: {usr.teach})',
                                                   'callback_data': 'change_teach'}
                                              ))
            usr.last_message_id = msg.message_id
            await state.finish()
        usr.save()

    @staticmethod
    async def audit_rasp(
            bot: Bot,
            query: CallbackQuery|Message,
            usr: UserModel,
            state: FSMContext
    ):
        if usr.audit is None:
            if isinstance(query, Message):
                if len(query.text.splitlines()) == 1:
                    usr.audit = query.text.strip()
                    await state.finish()
                    await bot.delete_message(query.chat.id, query.message_id)
                    msg: Message = await query.answer('Какое расписание вы хотите увидеть?',
                                                      reply_markup=KeyBoards.get_keyboards(
                                                          {'text': 'На неделю', 'callback_data': 'done_rasp-audit-ned'},
                                                          {'text': 'На сегодня', 'callback_data': 'done_rasp-audit-day'},
                                                          {'text': f'Указать другую группу(сейчас: {usr.audit})',
                                                           'callback_data': 'change_audit'}
                                                      ))
                    usr.last_message_id = msg.message_id
                else:
                    await bot.delete_message(query.chat.id, query.message_id)
                    await query.answer('Аудитория введен неверно введена неверно')
                    return
            else:
                await bot.delete_message(query.message.chat.id, usr.last_message_id)
                msg: Message = await bot.send_message(query.message.chat.id,
                                                      'Введите номер аудитории')
                usr.last_message_id = msg.message_id
                await state.set_state(RaspState.get_info.state)
                await state.set_data({'func_name': 'audit_rasp'})
        else:
            await bot.delete_message(query.message.chat.id, usr.last_message_id)
            msg: Message = await bot.send_message(query.from_user.id,'Какое расписание вы хотите увидеть?',
                                              reply_markup=KeyBoards.get_keyboards(
                                                  {'text': 'На неделю', 'callback_data': 'done_rasp-audit-ned'},
                                                  {'text': 'На сегодня', 'callback_data': 'done_rasp-audit-day'},
                                                  {'text': f'Указать другую группу(сейчас: {usr.audit})',
                                                   'callback_data': 'change_audit'}
                                              ))
            usr.last_message_id = msg.message_id
            await state.finish()
        usr.save()

    @classmethod
    def get_method_by_name(cls, name: str):
        return cls.__dict__.get(name)

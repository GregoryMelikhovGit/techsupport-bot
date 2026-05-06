from logic import DB_Manager
from config import *
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(TOKEN)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    questions_list = manager.get_questions()
    markup.add(InlineKeyboardButton('Отправить запрос', callback_data='select_support_dept'),
               InlineKeyboardButton(questions_list[0], callback_data='Q#0'),
               InlineKeyboardButton(questions_list[1], callback_data='Q#1'),
               InlineKeyboardButton(questions_list[2], callback_data='Q#2'),
               InlineKeyboardButton(questions_list[3], callback_data='Q#3'),
               InlineKeyboardButton(questions_list[4], callback_data='Q#4'),
               InlineKeyboardButton(questions_list[5], callback_data='Q#5'))
    return markup

def gen_select_dept_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    depts_list = manager.get_depts()
    markup.add(InlineKeyboardButton(depts_list[0], callback_data='support_dept_dev'),
               InlineKeyboardButton(depts_list[1], callback_data='support_dept_sales'),
               InlineKeyboardButton('⬅️ В главное меню', callback_data='menu_back'))
    return markup

def gen_support_back_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('⬅️ В меню выбора отдела', callback_data='support_back'))
    return markup

def gen_main_back_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('Вернутся в главное меню', callback_data='menu_back'))
    return markup
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    answers_list = manager.get_answers()
    if call.data == 'select_support_dept':
        text = 'В какой отдел вы хотите направить запрос?'
        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_select_dept_markup()
        )
    elif call.data == 'support_dept_dev':
        global selected_dept_id
        selected_dept_id = 1
        depts_list = manager.get_depts()
        dept = depts_list[selected_dept_id-1]
        text = f'Напишите запрос в {dept.lower()}'
        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_support_back_markup()
        )
        bot.register_next_step_handler(
            call.message,
            insert_request,
            call.message.message_id
        )
    elif call.data == 'support_dept_sales':
        selected_dept_id = 2
        depts_list = manager.get_depts()
        dept = depts_list[selected_dept_id-1]
        text = f'Напишите запрос в {dept.lower()}'
        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_support_back_markup()
        )
        bot.register_next_step_handler(
            call.message,
            insert_request, 
            call.message.message_id
        )
    elif call.data == 'menu_back':
        text = 'Добро пожаловать в бота тех. поддержки!'
        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_markup()
        )
    elif call.data == 'support_back':
        text = 'В какой отдел вы хотите направить запрос?'
        bot.edit_message_text(
            text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_select_dept_markup()
        )
    elif call.data == 'Q#0':
        bot.answer_callback_query(call.id, answers_list[0], show_alert=True)
    elif call.data == 'Q#1':
        bot.answer_callback_query(call.id, answers_list[1], show_alert=True)
    elif call.data == 'Q#2':
        bot.answer_callback_query(call.id, answers_list[2], show_alert=True)
    elif call.data == 'Q#3':
        bot.answer_callback_query(call.id, answers_list[3], show_alert=True)
    elif call.data == 'Q#4':
        bot.answer_callback_query(call.id, answers_list[4], show_alert=True)
    elif call.data == 'Q#5':
        bot.answer_callback_query(call.id, answers_list[5], show_alert=True)

def insert_request(message, bot_message_id):
    request = message.text
    user_id = message.from_user.id
    dept_id = selected_dept_id
    data = [request, user_id, dept_id]
    manager.insert_request([tuple(data)])
    depts_list = manager.get_depts()
    dept = depts_list[selected_dept_id-1]
    text = f'Большое спасибо за написание запроса, он будет отправлен в {dept.lower()}'
    bot.delete_message(
        message.chat.id,
        message.message_id
    )
    bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=bot_message_id,
        reply_markup=gen_main_back_markup()
    )
@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в бота тех. поддержки!', reply_markup=gen_markup())


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()
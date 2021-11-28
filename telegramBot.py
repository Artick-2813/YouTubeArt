from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

from googleapiclient.discovery import build

from bs4 import BeautifulSoup
import time
import datetime


class Search(StatesGroup):
    my_search = State()
    new_video = State()
    popular_video = State()
    test = State()


# Inline_Keyboard
search_button = InlineKeyboardButton('Поиск видео  🔎', callback_data='Поиск видео')
new_video = InlineKeyboardButton('Новинки 💎', callback_data='Новинки')
popular_video = InlineKeyboardButton('Популярное 🔥', callback_data='Популярное')
support_me = InlineKeyboardButton('Поддержать 💰', callback_data='Поддержать')
search_keyboard = InlineKeyboardMarkup().add(search_button, new_video, popular_video, support_me)
# Payment_Keyboard
my_paypal = InlineKeyboardButton('PayPal', callback_data='PayPal')
Youmoney = InlineKeyboardButton('ЮMoney', callback_data='ЮMoney')
payment_keyboard = InlineKeyboardMarkup().add(my_paypal, Youmoney)


# bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Хай, {message.from_user.first_name} 🤚\n'
                         'Хочешь найти любое видео 🎬\n'
                         'Тогда быстрее жми на любую кнопку 😉', reply_markup=search_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'Поиск видео')
async def search_begin(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '\n'
                                                        'Напиши любое название видео, и я начну поиск 🔎',)

    await Search.my_search.set()

    @dp.message_handler(state=Search.my_search)
    async def search_video_1(msg: types.Message, state: FSMContext):
        get_search = msg.text

        await state.update_data(my_search=get_search)
        data = await state.get_data()
        find_search = data.get('my_search')

        file_path = 'C:/Users/Admin/PycharmProjects/YouTubeArt/ArtYoutubeVideo'

        api_key = 'AIzaSyBXEyhLdBF9n1vTFg7mQPD-M4Zxk_RS-hI'
        youtube = build('youtube', 'v3', developerKey=api_key)
        try:

            request_search = youtube.search().list(
                part='snippet',
                q=find_search,
                order='relevance',
                type='video',
                maxResults='1'

            )

            response_search_video = request_search.execute()

            save_id_videos = []

            info_video = {}

            for all_video_get in response_search_video['items']:
                find_id_video = (all_video_get['id']['videoId'])
                save_id_videos.append(find_id_video)

                find_title_video = (all_video_get['snippet']['title'])
                info_video['Title:'] = find_title_video

                find_description_video = (all_video_get['snippet']['description'])
                info_video['Description:'] = find_description_video

                find_published_video = (all_video_get['snippet']['publishedAt'])
                datetime_youtube = datetime.datetime.strptime(find_published_video, '%Y-%m-%dT%H:%M:%SZ')
                date_time_telegram = str(datetime_youtube)
                info_video['Published:'] = date_time_telegram

            request_find_video = youtube.videos().list(
                part='player',
                id=save_id_videos
            )

            response_find_video = request_find_video.execute()
            for find_all_src_videos in response_find_video['items']:
                find_src_video = (find_all_src_videos['player']['embedHtml'])
                find_elem = find_src_video
                soup = BeautifulSoup(find_elem, 'html.parser')
                find_src = soup.find('iframe').get('src')
                youtube_link = find_src.replace('//www.youtube.com/embed/', 'https://www.youtube.com/watch?v=')

                await msg.answer('📌 Cсылка на видео: ' + youtube_link + '\n' +
                                                    '\n'
                                 
                                 '🔖 Название видео: ' + info_video['Title:'] + '\n' +
                                                    '\n'
                                 
                                 '📝 Описание видео: ' + info_video['Description:'] + '\n' +
                                                    '\n'
                                 
                                 '🕐 Время публикации видео: ' + info_video['Published:'] + '\n'
                                 )
            time.sleep(3)
            await msg.answer('Загрузка завершена ✅')
            await msg.answer('Хотите загрузить другое видео или поискать что-то другое 🤔\n'
                             'Тогда выбери в меню кнопку и кликай 👇', reply_markup=search_keyboard)

            await state.finish()

        except Exception as ex:
            await msg.answer('Простите я ничего не смог найти...Попробуйте вести более точное название 🙁')
            print(ex)
        finally:
            time.sleep(1)


@dp.callback_query_handler(lambda c: c.data == 'Новинки')
async def new(new: types.CallbackQuery):
    await bot.answer_callback_query(new.id)
    await bot.send_message(new.from_user.id, '🔹 Хочешь найти новые видео, тогда тебе сюда 🔹\n'
                                             'Просто веди любое название видео, и я начну поиск 🔎\n'
                                             '📝 Например: "Марвел" или "Трейлер человека паука 2021"\n'
                                             '📌 Примечание: всего будет загруженно 5 видео')

    await Search.new_video.set()

    @dp.message_handler(state=Search.new_video)
    async def search_new_video(msg: types.Message, state: FSMContext):
        get_new_video = msg.text

        await state.update_data(new_video=get_new_video)
        data = await state.get_data()
        find_new_video = data.get('new_video')

        api_key = 'AIzaSyBXEyhLdBF9n1vTFg7mQPD-M4Zxk_RS-hI'
        youtube = build('youtube', 'v3', developerKey=api_key)
        try:
            request_search = youtube.search().list(
                part='id',
                q=find_new_video,
                order='date',
                type='video',
                maxResults='5'

            )
            save_id_videos = []

            response_search_video = request_search.execute()
            for all_video_get in response_search_video['items']:
                find_id_video = (all_video_get['id']['videoId'])
                save_id_videos.append(find_id_video)

            request_find_video = youtube.videos().list(
                part='player',
                id=save_id_videos
            )

            response_find_video = request_find_video.execute()

            for find_all_src_videos in response_find_video['items']:
                find_src_video = (find_all_src_videos['player']['embedHtml'])
                find_elem = find_src_video
                soup = BeautifulSoup(find_elem, 'html.parser')
                find_src = soup.find('iframe').get('src')
                youtube_link = find_src.replace('//www.youtube.com/embed/', 'https://www.youtube.com/watch?v=')
                await msg.answer('📌 Ссылка на видео: ' + youtube_link)

            time.sleep(3)
            await msg.answer('Загрузка завершена ✅')
            await msg.answer('Хотите загрузить другое видео или поискать что-то другое 🤔\n'
                             'Тогда выбери в меню кнопку и кликай 👇',
                             reply_markup=search_keyboard)
            await state.finish()
        except Exception as ex:
            await msg.answer('Простите я ничего не смог найти...Попробуйте вести более точное название 🙁')
            print(ex)
        finally:
            time.sleep(1)


@dp.callback_query_handler(lambda c: c.data == 'Популярное')
async def popular_video(msg_popular: types.CallbackQuery):
    await bot.answer_callback_query(msg_popular.id)
    await bot.send_message(msg_popular.from_user.id, '💠 В этом разделе ты сможешь найти популярные видео 💠\n'
                                                     'Просто веди любое название видео, и я начну поиск 🔎\n'
                                                     '📝 Например: "Вдудь" или "Фильм Майор Гром"\n'
                                                     '📌 Примечание: всего будет загруженно 5 видео')

    await Search.popular_video.set()

    @dp.message_handler(state=Search.popular_video)
    async def search_popular_video(msg: types.Message, state: FSMContext):
        get_popular_video = msg.text

        await state.update_data(popular_video=get_popular_video)
        data = await state.get_data()
        find_popular_video = data.get('popular_video')

        api_key = 'AIzaSyBXEyhLdBF9n1vTFg7mQPD-M4Zxk_RS-hI'
        youtube = build('youtube', 'v3', developerKey=api_key)
        try:
            request_search = youtube.search().list(
                part='id',
                q=find_popular_video,
                order='viewCount',
                type='video',
                maxResults='5'

            )
            save_id_videos = []

            response_search_video = request_search.execute()
            for all_video_get in response_search_video['items']:
                find_id_video = (all_video_get['id']['videoId'])
                save_id_videos.append(find_id_video)

            request_find_video = youtube.videos().list(
                part='player',
                id=save_id_videos
            )

            response_find_video = request_find_video.execute()

            for find_all_src_videos in response_find_video['items']:
                find_src_video = (find_all_src_videos['player']['embedHtml'])
                find_elem = find_src_video
                soup = BeautifulSoup(find_elem, 'html.parser')
                find_src = soup.find('iframe').get('src')
                youtube_link = find_src.replace('//www.youtube.com/embed/', 'https://www.youtube.com/watch?v=')
                await msg.answer('📌 Ссылка на видео: ' + youtube_link)

            time.sleep(3)
            await msg.answer('Загрузка завершена ✅')
            await msg.answer('Хотите загрузить другое видео или поискать что-то другое 🤔\n'
                             'Тогда выбери в меню кнопку и кликай 👇',
                             reply_markup=search_keyboard)

            await state.finish()
        except Exception as ex:
            await msg.answer('Простите я ничего не смог найти...Попробуйте вести более точное название 🙁')
            print(ex)
        finally:
            time.sleep(1)


@dp.callback_query_handler(lambda c: c.data == 'Поддержать')
async def support_me(msg_support: types.CallbackQuery):
    await bot.answer_callback_query(msg_support.id)
    await bot.send_message(msg_support.from_user.id, 'Хочешь поддержать меня, тогда выбери способ оплаты 👇'
                                                     , reply_markup=payment_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'PayPal')
async def paypal(msg_paypal: types.CallbackQuery):
    await bot.answer_callback_query(msg_paypal.id)
    await bot.send_message(msg_paypal.from_user.id, '👇 Кликни на ссылку 👇\n'
                                                    '📌 my_paypal', reply_markup=search_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'ЮMoney')
async def Youmoney(msg_youmoney: types.CallbackQuery):
    await bot.answer_callback_query(msg_youmoney.id)
    await bot.send_message(msg_youmoney.from_user.id, '👇 Кликни на ссылку 👇\n'
                                                      '📌 my_youmoney',
                                                      reply_markup=search_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)

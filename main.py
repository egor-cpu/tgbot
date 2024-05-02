"""import requests
import time

API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
BOT_TOKEN = ''
ERROR_TEXT = 'На этом месте могла быть картинка вашего котика, но её нет :('
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int
cat_response: requests.Response
cat_link: str

while counter < MAX_COUNTER:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1 """
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
import httplib2
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import creds

def get_service_sacc():
    creds_json = "kpiinfo-f2eb171a014e.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)
def process_text(message):
    model = message.text
    file = open("users.txt", "a")
    file.write(model)
    file.write("\n")
    file.close()
BOT_TOKEN = ''

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Ботик котик!\nНапиши /help , чтобы узнать, что тебе доступно')

@dp.message(Command(commands=["gayvodka"]))
async def process_gayvodka_command(message: Message):
    gayvodka=FSInputFile("photo_5891009063846789742_w.jpg")
    await message.answer_photo(gayvodka)

@dp.message(Command(commands=["gayvodka2"]))
async def process_gayvodka2_command(message: Message):
    gayvodka2=FSInputFile("photo_5195295404948840202_y.jpg")
    await message.answer_photo(gayvodka2)
# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Доступные тебе команды: \n'
        '/reg - прохождение регистрации \n'
        '/KPI -посмотреть свой KPI \n'
    )
class RegistrationStates(StatesGroup):
    waiting_for_namesirname = State()
@dp.message(Command(commands=['reg']))
async def process_reg_command(message: Message, state: FSMContext):
    id = message.chat.id
    file = open("users.txt", "r")
    notreg = 1
    for line in file:
        if str(id) in line:
            notreg = 0
            await bot.send_message(message.chat.id, "Вы уже зарегистрированны")
    file.close()
    if notreg == 1:
        file = open("users.txt", "a")
        file.write(str(id))
        file.write(' ')
        file.close()
        await bot.send_message(message.chat.id, "Укажите вашу Фамилию и Имя")
        await state.set_state(RegistrationStates.waiting_for_namesirname)  # Устанавливаем состояние

@dp.message(RegistrationStates.waiting_for_namesirname)
async def name_get(message: Message, state:FSMContext):
    name = message.text
    file = open("users.txt", "a")
    file.write(name)
    file.write('\n')
    file.close()
    await state.update_data(name=name)
    await message.reply("Регистрация прошла успешно")
    await state.clear()

@dp.message(Command(commands=['KPI']))
async def process_KPI_command(message: Message):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    if (bol != "none"):
        sheet_id = '172rh115qDUxtYUCAroXFqlh-tuZTmS8ifJcYj-EsWGM'
        service = get_service_sacc()
        sheet = service.spreadsheets()
        key = 'AIzaSyBmiUMq2qsmQPoMsIXYFrs_uqule5Wjxsk'
        results = sheet.values().get(spreadsheetId=sheet_id, range="KPI!B3:H91").execute()
        KPI = results['values']
        bol = bol.replace(id + ' ','')
        bol = bol.replace('\n', '')
        for i in range(len(KPI)):
            if (len(KPI[i]) !=0):
                if bol in KPI[i][0]:
                    await bot.send_message(message.chat.id, KPI[i][6])
    else:
        await bot.send_message(message.chat.id, "Для начала пройдите регистрацию")



dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(process_KPI_command, Command(commands='KPI'))
dp.message.register(process_KPI_command, Command(commands='reg'))

if __name__ == '__main__':
    dp.run_polling(bot)



"""spreadsheet = service.spreadsheets().create(body = {
'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист номер один',
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
}).execute()
spreadsheetId=spreadsheet['spreadsheetId']
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
driveService = googleapiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'egorkomarov2004@gmail.com'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()
"""

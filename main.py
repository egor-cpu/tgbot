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
import re
from datetime import datetime
waiting_for_tea=""
def get_pos_for_open(pos, what):
    if what=="none":
        if "ITL" in pos:
            return "IT"
        elif "HRL" in pos:
            return "HR"
        elif "PRL" in pos:
            return "PR"
        elif "CRL" in pos:
            return "CR"
        elif "LD" in pos:
            return "LD"
        else:
            return "0"
    else:
        if "ITL" in pos:
            if (what == "1"):
                return "ITtasks.txt"
            else:
                return "Boardtasks.txt"
        elif "HRL" in pos:
            if (what == "1"):
                return "HRtasks.txt"
            else:
                return "Boardtasks.txt"
        elif "PRL" in pos:
            if (what == "1"):
                return "PRtasks.txt"
            else:
                return "Boardtasks.txt"
        elif "CRL" in pos:
            if (what == "1"):
                return "CRtasks.txt"
            else:
                return "Boardtasks.txt"
        elif "LD" in pos:
            if (what == "1"):
                return "ITtasks.txt"
            elif (what == "2"):
                return "HRtasks.txt"
            elif what == "3":
                return "PRtasks.txt"
            elif what == "4":
                return "CRtasks.txt"
            else:
                return "Boardtasks.txt"
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
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = "none"
    bol = get_pos_for_open(bol, what)
    if bol!="0":
        await message.answer(
            'Доступные тебе команды: \n'
            '/reg - прохождение регистрации \n'
            '/KPI -посмотреть свой KPI \n'
            '/Photo - получить ссылку на все фотографии\n'
            '/Tasks - посмотреть все таски\n'
            '/addTasks - добавить задачу\n'
            '/removeTasks - удалить задачу'
        )
    else:
        await message.answer(
            'Доступные тебе команды: \n'
            '/reg - прохождение регистрации \n'
            '/KPI -посмотреть свой KPI \n'
            '/Photo - получить ссылку на все фотографии\n'
            '/Tasks - посмотреть все таски'
        )
class RemoveStates(StatesGroup):
    waiting_for_team = State()
    waiting_for_taskname = State()
@dp.message(Command(commands=['removeTasks']))
async def process_remove_command(message: Message, state:FSMContext):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = "none"
    bol = get_pos_for_open(bol, what)
    if bol != "0":
        if bol == "IT":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "HR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "PR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "CR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "LD":
            await message.answer(
                "Напишите 1 Если для IT команды\n"
                "Напишите 2 Если для HR команды\n"
                "Напишите 3 Если для PR команды\n"
                "Напишите 4 Если для CR команды\n"
                "Напишите 5 Если это для борда"
            )
        await state.set_state(RemoveStates.waiting_for_team)
    else:
        await bot.send_message(message.chat.id, "У вас нету прав для добавления тасков")
@dp.message(RemoveStates.waiting_for_team)
async def team_getr(message: Message, state:FSMContext):
    global waiting_for_tea
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = message.text
    bol = get_pos_for_open(bol, what)
    waiting_for_tea = bol
    await state.update_data(waiting_for_team = bol)
    await bot.send_message(message.chat.id, "Напишите название таска которого нужно удалить(Нужно писать точь-в-точь")
    await state.set_state(RemoveStates.waiting_for_taskname)
@dp.message(RemoveStates.waiting_for_taskname)
async def task_getr(message: Message, state:FSMContext):
    task = message.text
    with open(waiting_for_tea) as f:
        lines = f.readlines()
    pattern = re.compile(re.escape(task))
    with open(waiting_for_tea, 'w') as f:
        for line in lines:
            result = pattern.search(line)
            if result is None:
                f.write(line)
    await bot.send_message(message.chat.id, "Задача успешно удалена")
    await state.update_data(waiting_for_task=task)
    await state.clear()
class RegistrationStates(StatesGroup):
    waiting_for_namesirname = State()
    waiting_for_pos = State()
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
    file.write(' ')
    file.close()
    await bot.send_message(message.chat.id, "Укажите секретный код, если его нету напишите 0")
    await state.update_data(waiting_for_namesirname=name)
    await state.set_state(RegistrationStates.waiting_for_pos)

@dp.message(RegistrationStates.waiting_for_pos)
async def pos_get(message: Message, state:FSMContext):
    pos = message.text
    if (pos == 'ITld20786'):
        file = open("users.txt", "a")
        file.write('ITL')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый IT лидер")
    elif (pos == 'CRld20800'):
        file = open("users.txt", "a")
        file.write('CRL')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый CR лидер")
    elif (pos == 'HRld29039'):
        file = open("users.txt", "a")
        file.write('HRL')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый HR лидер")
    elif (pos == 'PRld28473'):
        file = open("users.txt", "a")
        file.write('PRL')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый PR лидер")
    elif (pos == 'ChairP93827'):
        file = open("users.txt", "a")
        file.write('LD')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый стул")
    elif (pos == 'IT'):
        file = open("users.txt", "a")
        file.write('IT')
        file.write('\n')
        file.close()
    elif (pos == 'CR'):
        file = open("users.txt", "a")
        file.write('CR')
        file.write('\n')
        file.close()
    elif (pos == 'HR'):
        file = open("users.txt", "a")
        file.write('HR')
        file.write('\n')
        file.close()
    elif (pos == 'PR'):
        file = open("users.txt", "a")
        file.write('PR')
        file.write('\n')
        file.close()
    else:
        file = open("users.txt", "a")
        file.write('outmem')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно")
    await state.clear()
class addTaskStates(StatesGroup):
    waiting_for_team = State()
    waiting_for_task = State()
    waiting_for_date = State()
    waiting_for_person = State()
@dp.message(Command(commands=['addTasks']))
async def process_addTasks_command(message:Message, state: FSMContext):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = "none"
    bol = get_pos_for_open(bol,what)
    if bol != "0":
        if bol == "IT":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "HR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "PR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "CR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "LD":
            await message.answer(
                "Напишите 1 Если для IT команды\n"
                "Напишите 2 Если для HR команды\n"
                "Напишите 3 Если для PR команды\n"
                "Напишите 4 Если для CR команды\n"
                "Напишите 5 Если это для борда"
            )
        await state.set_state(addTaskStates.waiting_for_team)
    else:
        await bot.send_message(message.chat.id, "У вас нету прав для добавления тасков")

@dp.message(addTaskStates.waiting_for_team)
async def team_get(message: Message, state:FSMContext):
    global waiting_for_tea
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = message.text
    bol = get_pos_for_open(bol, what)
    waiting_for_tea = bol
    await state.update_data(waiting_for_team = bol)
    await bot.send_message(message.chat.id, "Напишите сам таск")
    await state.set_state(addTaskStates.waiting_for_task)
@dp.message(addTaskStates.waiting_for_task)
async def task_get(message: Message, state:FSMContext):
    task = message.text
    file = open(waiting_for_tea, "a")
    file.write(task)
    file.write('.')
    file.close()
    await bot.send_message(message.chat.id, "Напишите дедлайн таска в формате: дата-месяц-год время")
    await state.update_data(waiting_for_task=task)
    await state.set_state(addTaskStates.waiting_for_date)

@dp.message(addTaskStates.waiting_for_date)
async def date_get(message: Message, state: FSMContext):
    date = message.text
    file = open(waiting_for_tea, "a")
    file.write(date)
    file.write('.')
    file.close()
    await bot.send_message(message.chat.id, "Напишите кто ответсвеннен за задание в виде ФИ")
    await state.update_data(waiting_for_date=date)
    await state.set_state(addTaskStates.waiting_for_person)

@dp.message(addTaskStates.waiting_for_person)
async def person_get(message: Message, state:FSMContext):
    person = message.text
    file = open(waiting_for_tea, "a")
    file.write(person)
    file.write('\n')
    file.close()
    idfrom = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if person in line:
            bol = line
            break
    file.close()
    await bot.send_message(message.chat.id, "Таск добавлен")
    await state.update_data(waiting_for_person=person)
    await state.clear()
    await notice(bol,waiting_for_tea,idfrom)

async def notice(id,fil,idfrom):
    file = open(fil, "r")
    dat = "none"
    task = ""
    name = id[id.find(" ")+1:id.rfind(" ")]
    for line in file:
        if name in line:
            dat = line[line.find(".")+1:line.rfind(".")]
            task = line[:line.find(".")]
    counter = 0
    send = 0
    results = [dat[:dat.find("-")], dat[dat.find("-")+1:dat.rfind("-")], dat[dat.rfind("-")+1:dat.rfind(" ")], dat[dat.rfind(" "):dat.rfind(":")], dat[dat.rfind(":")+1:]]
    deadlinetime = list(map(int, results))
    while (counter != 3):
        current_datetime = datetime.now()
        if counter == 1 and send == 0:
            await bot.send_message(id[:id.find(" ")], "Дедлайны горят, дедлайн наступит через 3 дня. По таску: " + task)
            await bot.send_message(idfrom, "Дедлайн по задаче " + task + " закончится через 3 дня, ответсвенный за неё " + name)
            send = 1
        elif counter == 2 and send == 1:
            await bot.send_message(id[:id.find(" ")], "Дедлайн уже завтра!!! По таску: " + task)
            await bot.send_message(idfrom, "Дедлайн по задаче " + task + " закончится через завтра, ответсвенный за неё " + name)
        if (int(current_datetime.year) - deadlinetime[2] == 0):
            if (int(current_datetime.month) - deadlinetime[1] == 0):
                if (int(current_datetime.day) - deadlinetime[0] == 3):
                    if (int(current_datetime.hour) - deadlinetime[3] == 0):
                        if (int(current_datetime.minute) - deadlinetime[4] == 0):
                            counter = 1
                elif (int(current_datetime.day) - deadlinetime[0] == 1):
                    if (int(current_datetime.hour) - deadlinetime[3] == 0):
                        if (int(current_datetime.minute) - deadlinetime[4] == 0):
                            counter = 2
                            send = 1
                elif (int(current_datetime.day) - deadlinetime[0] == 0):
                    if (int(current_datetime.hour) - deadlinetime[3] == 0):
                        if (int(current_datetime.minute) - deadlinetime[4] == 0):
                            counter = 3

    await bot.send_message(id[:id.find(" ")], "Время на выполнение задачи " + task + " истекло")
    await bot.send_message(idfrom, "Дедлайн по задаче " + task + " закончился, ответсвенный за неё " + name + ". Если она выполнена, то удалите пожалуйста данную задачу из списка тасков и поставте такому хорошему человеку + KPI=)")

@dp.message(Command(commands=['Tasks']))
async def process_Tasks_command(message:Message):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    if "IT" in bol:
        file = open("ITtasks.txt", "r")
        await bot.send_message(message.chat.id, "IT Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        if "ITL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id,"Board таски:")
            for line in file:
                await message.answer(line)
            file.close()
    elif "HR" in bol:
        file = open("HRtasks.txt", "r")
        await bot.send_message(message.chat.id, "HR Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        if "HRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id,"Board таски:")
            for line in file:
                await message.answer(line)
            file.close()
    elif "PR" in bol:
        await bot.send_message(message.chat.id, "PR Команды таски:")
        file = open("PRtasks.txt", "r")
        for line in file:
            await message.answer(line)
        file.close()
        if "PRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id,"Board таски:")
            for line in file:
                await message.answer(line)
            file.close()
    elif "CR" in bol:
        await bot.send_message(message.chat.id, "CR Команды таски:")
        file = open("CRtasks.txt", "r")
        for line in file:
            await message.answer(line)
        file.close()
        if "CRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id,"Board таски:")
            for line in file:
                await message.answer(line)
            file.close()
    elif "LD" in bol:
        file = open("ITtasks.txt", "r")
        await bot.send_message(message.chat.id, "IT Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        file = open("HRtasks.txt", "r")
        await bot.send_message(message.chat.id, "HR Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        file = open("CRtasks.txt", "r")
        await bot.send_message(message.chat.id, "CR Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        file = open("PRtasks.txt", "r")
        await bot.send_message(message.chat.id, "PR Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        file = open("Boardtasks.txt", "r")
        await bot.send_message(message.chat.id,"Board таски:")
        for line in file:
            await message.answer(line)
        file.close()
    else:
        await bot.send_message(message.chat.id, "Вы долны зарегистрироваться для просмотра тасков через /reg")
@dp.message(Command(commands=['Photo']))
async def process_Photo_command(message:Message):
    await message.answer('https://vk.com/albums-174856092')
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
        results = sheet.values().get(spreadsheetId=sheet_id, range="KPI!B3:H91").execute()
        KPI = results['values']
        bol = bol.replace(id + ' ','')
        bol = bol.replace('\n', '')
        for i in range(len(KPI)):
            if (len(KPI[i]) !=0):
                if bol[0:bol.rfind(" ")-1] in KPI[i][0]:
                    await bot.send_message(message.chat.id, KPI[i][6])
    else:
        await bot.send_message(message.chat.id, "Для начала пройдите регистрацию")


dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(process_KPI_command, Command(commands='KPI'))
dp.message.register(process_reg_command, Command(commands='reg'))
dp.message.register(process_Photo_command, Command(commands='Photo'))
dp.message.register(process_Tasks_command, Command(commands='Tasks'))
dp.message.register(process_addTasks_command, Command(commands='addTasks'))
dp.message.register(process_remove_command,Command(commands='removeTasks'))
if __name__ == '__main__':
    dp.run_polling(bot)



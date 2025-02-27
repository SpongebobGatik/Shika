import discord
from discord.ext import commands
from discord import Intents
import os
import random
import asyncio
import aiohttp
import requests

# Ваш токен бота
TOKEN = "MTMyMjg0ODkwMDc4MDEzMDM2NA.GoQlG6.AcO1OhV-yJ7YKYwm0jKurfRNQ2b1z4ytRZe0xM"

# URL репозитория на GitHub
GITHUB_REPO_URL = "https://raw.githubusercontent.com/SpongebobGatik/Shika/main/music/"
GITHUB_API_URL = "https://api.github.com/repos/SpongebobGatik/Shika/contents/music/random"

# Папка для хранения загруженных файлов
MUSIC_FOLDER = os.path.join(os.getcwd(), "music")

# Имя файла, который будет воспроизводиться по команде
SHIKA_FILENAME = "shika1.mp3"  # Замените на имя вашего файла для команды /shika
PENIS_FILENAME = "penis.mp3"
# Имя файла, который будет воспроизводиться при входе
ENTRY_FILENAME = "shikacon.mp3"  # Замените на имя вашего файла для входа
# Имя файла, который будет воспроизводиться при входе
ENTRY_FILENAME1 = "shikacon1.mp3"  # Замените на имя вашего файла для входа
# Имя файла, который будет воспроизводиться при входе
ENTRY_FILENAME2 = "shikacon2.mp3"  # Замените на имя вашего файла для входа
# Имя файла, который будет воспроизводиться при входе
ENTRY_FILENAME3 = "shikacon3.mp3"  # Замените на имя вашего файла для входа
# Имя файла, который будет воспроизводиться при входе
ENTRY_FILENAME4 = "shikacon4.mp3"  # Замените на имя вашего файла для входа

# Создание объекта Intents
intents = Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

# Создание бота
bot = commands.Bot(command_prefix="/", intents=intents)

async def download_file(session, url, filename):
    """Скачивает файл по URL и сохраняет его с указанным именем."""
    if os.path.exists(filename):
        print(f"Файл {filename} уже существует. Пропускаем загрузку.")
        return  # Пропускаем загрузку, если файл уже существует

    async with session.get(url) as response:
        if response.status == 200:
            with open(filename, 'wb') as f:
                f.write(await response.read())
            print(f"Файл {filename} успешно загружен.")
        else:
            print(f"Не удалось загрузить файл {filename}. Статус код: {response.status}")

@bot.command(name="upload")
async def upload(ctx):
    """Команда для обновления файлов из GitHub."""
    # Создаем папку, если она не существует
    if not os.path.exists(MUSIC_FOLDER):
        os.makedirs(MUSIC_FOLDER)

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Список файлов, которые нужно загрузить
        files_to_download = [SHIKA_FILENAME, PENIS_FILENAME, ENTRY_FILENAME, ENTRY_FILENAME1, ENTRY_FILENAME2, ENTRY_FILENAME3, ENTRY_FILENAME4]

        for filename in files_to_download:
            await download_file(session, GITHUB_REPO_URL + filename, os.path.join(MUSIC_FOLDER, filename))

        # Создаем папку random, если она не существует
        random_folder_path = os.path.join(MUSIC_FOLDER, "random")
        if not os.path.exists(random_folder_path):
            os.makedirs(random_folder_path)

        # Получаем список файлов из папки random через GitHub API
        response = await session.get(GITHUB_API_URL)
        if response.status == 200:
            files = await response.json()
            downloaded_files = []  # Список для хранения загруженных файлов
            for file in files:
                if file['name'].endswith('.mp3'):
                    file_url = file['download_url']
                    await download_file(session, file_url, os.path.join(random_folder_path, file['name']))
                    downloaded_files.append(file['name'])  # Добавляем имя загруженного файла в список

            # Удаляем файлы, которые не были загружены
            for existing_file in os.listdir(random_folder_path):
                if existing_file not in downloaded_files:
                    os.remove(os.path.join(random_folder_path, existing_file))
                    print(f"Удален файл: {existing_file}")

        else:
            print(f"Не удалось получить список файлов из папки random. Статус код: {response.status}")

    await ctx.send("Файлы успешно обновлены из GitHub!")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    bot.loop.create_task(random_action())  # Запускаем задачу случайного действия

async def random_action():
    """Случайно выполняет одно из действий: отправка изображения или воспроизведение аудио каждые 5 минут."""
    await bot.wait_until_ready()  # Ждем, пока бот будет готов
    while not bot.is_closed():
        action = random.choice(['send_image', 'play_audio'])  # Случайный выбор действия

        if action == 'send_image':
            await send_random_image()
        elif action == 'play_audio':
            await play_random_audio()

        await asyncio.sleep(600)  # Ждем 10 минут перед следующим действием

# Переменная для хранения последнего сообщения бота
last_bot_message = None

async def send_random_image():
    """Отправляет случайное изображение из канала 'для-души-?' в канал 'телеграммы??'."""
    global last_bot_message  # Используем глобальную переменную для хранения последнего сообщения бота

    for guild in bot.guilds:
        # Получаем каналы
        source_channel = discord.utils.get(guild.text_channels, name="для-души-☠")
        target_channel = discord.utils.get(guild.text_channels, name="телеграммы📩")
        
        if source_channel and target_channel:
            print(f"Канал источника: {source_channel.name}, Канал назначения: {target_channel.name}")
            
            # Получаем сообщения из канала
            messages = [msg async for msg in source_channel.history(limit=100)]  # Получаем последние 100 сообщений
            images = [msg for msg in messages if msg.attachments]  # Фильтруем сообщения с вложениями

            print(f"Найдено сообщений: {len(messages)}, сообщений с вложениями: {len(images)}")  # Логирование

            if images:
                random_image = random.choice(images)  # Выбираем случайное сообщение с изображением
                attachment = random.choice(random_image.attachments)  # Выбираем случайное вложение
                
                # Удаляем предыдущее сообщение бота, если оно существует
                if last_bot_message is not None:
                    await last_bot_message.delete()
                
                # Отправляем новое изображение в целевой канал
                last_bot_message = await target_channel.send(attachment.url)  # Отправляем изображение в целевой канал
                print(f"Отправлено изображение: {attachment.url}")  # Логирование
            else:
                print("Нет сообщений с вложениями.")  # Логирование, если нет изображений
        else:
            print("Не удалось найти каналы.")  # Логирование, если каналы не найдены

RANDOM_FOLDER = os.path.join(MUSIC_FOLDER, "random")
async def play_random_audio():
    """Подключается к голосовому каналу с пользователями и воспроизводит случайный аудиофайл из папки random."""
    # Проверяем, есть ли подключенные голосовые клиенты
    if not bot.voice_clients:  # Если бот не подключен
        for guild in bot.guilds:
            for channel in guild.voice_channels:
                if channel.members:  # Проверяем, есть ли пользователи в канале
                    voice_client = await channel.connect()
                    await play_file(voice_client, ENTRY_FILENAME)  # Воспроизводим файл при входе
                    break  # Выходим из цикла после подключения
            else:
                continue  # Если не нашли подходящий канал, продолжаем искать
            break  # Выходим из внешнего цикла, если подключились
    else:
        voice_client = bot.voice_clients[0]  # Берем первого голосового клиента
        if voice_client.is_connected() and not voice_client.is_playing():
            # Получаем список файлов в папке random
            audio_files = [f for f in os.listdir(RANDOM_FOLDER) if f.endswith('.mp3')]
            if audio_files:
                random_file = random.choice(audio_files)  # Выбираем случайный файл
                await play_file(voice_client, os.path.join("random", random_file))  # Воспроизводим файл

@bot.command(name="shika")
async def play_shika(ctx):
    """Воспроизводит заранее определенный MP3-файл по команде /shika."""
    if ctx.author.voice is None:
        await ctx.send("Вы должны быть в голосовом канале, чтобы воспроизвести музыку!")
        return

    voice_channel = ctx.author.voice.channel

    # Проверка, подключен ли бот к голосовому каналу
    if ctx.voice_client is None:
        await voice_channel.connect()

    # Воспроизводим файл по команде
    await play_file(ctx.voice_client, SHIKA_FILENAME)
    
@bot.command(name="penis")
async def play_shika(ctx):
    """Воспроизводит заранее определенный MP3-файл по команде /penis."""
    if ctx.author.voice is None:
        await ctx.send("Вы должны быть в голосовом канале, чтобы воспроизвести музыку!")
        return

    voice_channel = ctx.author.voice.channel

    # Проверка, подключен ли бот к голосовому каналу
    if ctx.voice_client is None:
        await voice_channel.connect()

    # Воспроизводим файл по команде
    await play_file(ctx.voice_client, PENIS_FILENAME)
    
@bot.command(name="shikastop")
async def stop_music(ctx):
    """Останавливает воспроизведение музыки по команде /shikastop."""
    if ctx.voice_client is None:
        await ctx.send("Бот не подключен к голосовому каналу.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Останавливаем воспроизведение
        await ctx.send("Музыка остановлена.")
    else:
        await ctx.send("Музыка не воспроизводится в данный момент.")
        
@bot.event
async def on_voice_state_update(member, before, after):
    try:
        # Проверяем, вошел ли пользователь в голосовой канал
        if before.channel is None and after.channel is not None and member != bot.user:
            print(f"{member.name} вошел в голосовой канал: {after.channel.name}")
            await after.channel.send(f"{member.name} присоединился к каналу {after.channel.name}!")

            # Подключаемся к голосовому каналу, если бот не подключен
            if not bot.voice_clients:
                voice_client = await after.channel.connect()
                await play_file(voice_client, ENTRY_FILENAME)
            else:
                voice_client = bot.voice_clients[0]  # Берем существующего голосового клиента
                if voice_client.channel != after.channel:
                    await voice_client.move_to(after.channel)
                    await play_file(voice_client, ENTRY_FILENAME)  # Воспроизводим файл при переходе

        # Проверяем, вышел ли пользователь из голосового канала
        if after.channel is None and before.channel is not None and member != bot.user:
            print(f"{member.name} вышел из голосового канала: {before.channel.name}")
            await before.channel.send(f"{member.name} покинул канал {before.channel.name}!")

            # Останавливаем воспроизведение, если никто не остался в канале
            if len(before.channel.members) == 1:  # Только бот остался
                voice_client = bot.voice_clients[0]
                await voice_client.disconnect()

        # Проверяем, если пользователь переместился в другой канал
        if before.channel is not None and after.channel is not None and before.channel != after.channel and member != bot.user:
            print(f"{member.name} переместился из {before.channel.name} в {after.channel.name}.")
            await before.channel.send(f"{member.name} переместился из канала {before.channel.name} в {after.channel.name}!")

            # Если бот подключен к каналу, из которого пользователь вышел, перемещаем его в новый канал
            if bot.voice_clients:
                voice_client = bot.voice_clients[0]
                if voice_client.channel == before.channel:
                    await voice_client.move_to(after.channel)
                    if voice_client.is_connected():
                        await play_file(voice_client, ENTRY_FILENAME)  # Воспроизводим файл при переходе
                    else:
                        print("Бот не подключен к голосовому каналу.")
        
        # Проверяем, если бот отключен и пользователь заходит в канал
        if not bot.voice_clients and after.channel is not None and member != bot.user:
            voice_client = await after.channel.connect()
            await play_file(voice_client, ENTRY_FILENAME)

    except Exception as e:
        print(f"Произошла ошибка в on_voice_state_update: {e}")

async def play_file(voice_client, filename):
    """Воспроизводит указанный MP3-файл."""
    file_path = os.path.join(MUSIC_FOLDER, filename)

    # Проверка, существует ли файл
    if not os.path.isfile(file_path):
        print(f"Файл {filename} не найден.")
        return

    # Останавливаем текущее воспроизведение, если оно идет
    if voice_client.is_playing():
        voice_client.stop()

    # Начинаем воспроизведение музыки
    voice_client.play(discord.FFmpegPCMAudio(file_path), after=lambda e: print(f'Finished playing: {e}'))
    print(f"Теперь воспроизводится: {filename}")

@bot.command(name="join")
async def join(ctx):
    """Команда для подключения бота к голосовому каналу."""
    if ctx.author.voice is None:
        await ctx.send("Вы должны быть в голосовом канале, чтобы подключить бота!")
        return

    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()

@bot.command(name="leave")
async def leave(ctx):
    """Команда для отключения бота от голосового канала."""
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Бот отключился от голосового канала.")
    else:
        await ctx.send("Бот не подключен к голосовому каналу.")

bot.run(TOKEN)

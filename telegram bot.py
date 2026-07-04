
"""from os import getenv
import asyncio
from aiogram import Bot,Dispatcher, Router
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message()
async def hello(message):
    await message.answer("Hello")

async def main():
    bot = Bot(token=TOKEN)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())"""



# ============================================================
# YouTube → Telegram Bot
# ============================================================
# Установка зависимостей:
#   pip install yt-dlp aiogram apscheduler
#
# Запуск:
#   python bot.py
# ============================================================

import asyncio
import json
import os
import logging

import yt_dlp
from aiogram import Bot
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler   #pip install yt-dlp aiogram apscheduler


# ============================================================
# 🔧 НАСТРОЙКИ — заполни эти значения
# ============================================================

TELEGRAM_TOKEN      = "8800346156:AAHHwVq77ayEPHTlvgEV1w31BVZdPJYyITA"
CHANNEL_ID          = "-1002443277897"
YOUTUBE_CHANNEL_URL = "http://www.youtube.com/@Cherry-24-i1h"
CHANNEL_NAME        = "Cherry"  # отображается в подписи

CHECK_INTERVAL_MINUTES = 30   # как часто проверять новые видео
MAX_VIDEOS_TO_CHECK    = 5    # сколько последних видео проверять
VIDEO_FILENAME         = "temp_video.mp4"
POSTED_IDS_FILE        = "posted_videos.json"
MAX_FILE_SIZE_MB       = 50


# ============================================================
# ЛОГИ
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================
# ХРАНЕНИЕ ОПУБЛИКОВАННЫХ ВИДЕО
# ============================================================

def load_posted_ids():
    if os.path.exists(POSTED_IDS_FILE):
        with open(POSTED_IDS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_posted_id(video_id):
    ids = load_posted_ids()
    ids.append(video_id)
    with open(POSTED_IDS_FILE, 'w') as f:
        json.dump(ids, f, indent=2)


# ============================================================
# YouTube
# ============================================================

def get_latest_videos():
    """Получает список последних видео с канала (без скачивания)"""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlist_end': MAX_VIDEOS_TO_CHECK,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(YOUTUBE_CHANNEL_URL, download=False)
            return info.get('entries', [])
    except Exception as e:
        logger.error(f"Ошибка получения списка видео: {e}")
        return []


def get_video_info(video_url):
    """Получает полную информацию о видео"""
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            return ydl.extract_info(video_url, download=False)
    except Exception as e:
        logger.error(f"Ошибка получения инфо о видео: {e}")
        return {}


def download_video(video_url):
    """Скачивает видео. Возвращает True если успешно"""
    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': VIDEO_FILENAME,
        'max_filesize': MAX_FILE_SIZE_MB * 1024 * 1024,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return os.path.exists(VIDEO_FILENAME)
    except Exception as e:
        logger.error(f"Ошибка скачивания: {e}")
        return False


# ============================================================
# TELEGRAM
# ============================================================

def make_caption(video_info):
    """Формирует подпись: название + ссылка на видео + ссылка на канал"""
    title = video_info.get('title', 'Без названия')
    url   = video_info.get('webpage_url', '')

    caption = (
        f"🎬 *{title}*\n\n"
        f"🔗 [Смотреть на YouTube]({url})\n"
        f"📺 [Канал — {CHANNEL_NAME}]({YOUTUBE_CHANNEL_URL})"
    )
    return caption[:1024]  # лимит Telegram — 1024 символа


async def send_to_channel(bot, video_info, downloaded):
    """Отправляет видео или превью+ссылку в канал"""
    caption   = make_caption(video_info)
    thumbnail = video_info.get('thumbnail', '')
    url       = video_info.get('webpage_url', '')

    try:
        if downloaded and os.path.exists(VIDEO_FILENAME):
            # Отправляем файл
            await bot.send_video(
                chat_id=CHANNEL_ID,
                video=FSInputFile(VIDEO_FILENAME),
                caption=caption,
                parse_mode="Markdown",
            )
            logger.info("Отправлено как файл")
        else:
            # Видео больше 50MB — отправляем превью + ссылку
            if thumbnail:
                await bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=thumbnail,
                    caption=caption,
                    parse_mode="Markdown",
                )
            else:
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=caption,
                    parse_mode="Markdown",
                )
            logger.info("Отправлено превью + ссылка")
        return True

    except Exception as e:
        logger.error(f"Ошибка отправки в Telegram: {e}")
        return False


# ============================================================
# ГЛАВНАЯ ЛОГИКА
# ============================================================

async def check_and_post(bot):
    """Проверяет новые видео и публикует их"""
    logger.info("Проверяю новые видео...")

    posted_ids = load_posted_ids()
    videos     = get_latest_videos()

    if not videos:
        logger.info("Видео не найдено")
        return

    # Идём от старых к новым (reversed), чтобы постить в хронологическом порядке
    for video in reversed(videos):
        video_id = video.get('id')
        if not video_id or video_id in posted_ids:
            continue

        logger.info(f"Новое видео: {video_id}")
        video_url  = f"https://www.youtube.com/watch?v={video_id}"
        video_info = get_video_info(video_url)

        if not video_info:
            continue

        downloaded = download_video(video_url)
        success    = await send_to_channel(bot, video_info, downloaded)

        # Удаляем временный файл
        if os.path.exists(VIDEO_FILENAME):
            os.remove(VIDEO_FILENAME)

        if success:
            save_posted_id(video_id)
            logger.info(f"✅ Опубликовано: {video_id}")
        else:
            logger.error(f"❌ Не удалось опубликовать: {video_id}")

        # Пауза между постами чтобы не спамить
        await asyncio.sleep(5)


# ============================================================
# ЗАПУСК
# ============================================================

async def main():
    bot       = Bot(token=TELEGRAM_TOKEN)
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        func=check_and_post,
        trigger='interval',
        minutes=CHECK_INTERVAL_MINUTES,
        args=[bot],
    )
    scheduler.start()
    logger.info(f"✅ Бот запущен. Проверка каждые {CHECK_INTERVAL_MINUTES} минут.")

    # Сразу проверяем при старте
    await check_and_post(bot)

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
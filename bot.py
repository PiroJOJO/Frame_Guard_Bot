import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile
from aiogram import types, F, Router, Dispatcher

import os
import shutil

import config
from handlers import dp
from Real_ESRGAN.BSRGAN.main_test_bsrgan import main as BSRGAN_main
from Real_ESRGAN.inference_realesrgan import main as ESRGAN_main
from Real_ESRGAN.SwinIR.main_test_swinir import main as Swin_main

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)

async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
@dp.message(F.text == "BSRGAN")
async def with_bsrgan(message: types.Message):
    await message.answer("Подождите немного. \nВаше изображение скоро будет готово.", reply_markup=types.ReplyKeyboardRemove())
    BSRGAN_main() 
    res = os.listdir('Real_ESRGAN/BSRGAN/testsets/RealSRSet_results_x4')
    shutil.move(os.path.join('Real_ESRGAN/BSRGAN/testsets/RealSRSet_results_x4', res[0]), config.RESULT_PATH)
    shutil.rmtree('Real_ESRGAN/BSRGAN/testsets/RealSRSet_results_x4')
    size = os.path.getsize(os.path.join(config.RESULT_PATH, res[0]))
    if size < 5 * 1000 * 1000:
        await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(os.path.join(config.RESULT_PATH, res[0])))
    else: 
        await bot.send_document(chat_id=messege.chat.id, document=FSInputFile(os.path.join(config.RESULT_PATH, res[0])))
    await message.answer(f"Ваше улучшенное изображение готово! \nЧтобы попробовать снова перезапустите бота: /start")
    
@dp.message(F.text == "Real-ESRGAN")
async def with_esrgan(message: types.Message):
    await message.answer("Подождите немного. \nВаше изображение скоро будет готово.", reply_markup=types.ReplyKeyboardRemove())
    ESRGAN_main() 
    res = os.listdir(config.RESULT_PATH)
    size = os.path.getsize(os.path.join(config.RESULT_PATH, res[0]))
    if size < 5 * 1000 * 1000:
        await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(os.path.join(config.RESULT_PATH, res[0])))
    else: 
        await bot.send_document(chat_id=messege.chat.id, document=FSInputFile(os.path.join(config.RESULT_PATH, res[0])))
    await message.answer(f"Ваше улучшенное изображение готово! \nЧтобы попробовать снова перезапустите бота: /start")

@dp.message(F.text == "SwinIR")
async def with_swinir(message: types.Message):
    await message.answer("Подождите немного. \nВаше изображение скоро будет готово.", reply_markup=types.ReplyKeyboardRemove())
    Swin_main() 
    res = os.listdir('results/swinir_real_sr_x4')
    shutil.move(os.path.join('results/swinir_real_sr_x4', res[0]), config.RESULT_PATH)
    shutil.rmtree('results')
    size = os.path.getsize(os.path.join(config.RESULT_PATH, res[0]))
    if size < 5 * 1000 * 1000:
        await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(os.path.join(config.RESULT_PATH, res[0])))
    else: 
        await bot.send_document(chat_id=messege.chat.id, document=FSInputFile(os.path.join(config.RESULT_PATH, res[0])))
    await message.answer(f"Ваше улучшенное изображение готово! \nЧтобы попробовать снова перезапустите бота: /start")
if __name__ == "__main__":
    asyncio.run(main())


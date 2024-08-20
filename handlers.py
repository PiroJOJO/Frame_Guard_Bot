from aiogram import types, F, Router, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

import shutil
import os
import config

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Загрузить изображение"),
            types.KeyboardButton(text="Информация о боте")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    if os.path.exists('Real_ESRGAN/BSRGAN/testsets/RealSRSet/test.jpg'):
        os.remove('Real_ESRGAN/BSRGAN/testsets/RealSRSet/test.jpg')
    shutil.rmtree('Real_ESRGAN/results')
    os.mkdir('Real_ESRGAN/results')
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! \nДанный бот может улучшить качество твоей фотографии с помощью различных нейронных сетей.✨\nСкорей отправляй своё изображение и оцени результат!", reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.message(F.text == "Информация о боте")
async def with_info(message: types.Message):
    await message.answer("Данный бот создан для демонстрации работы таких моделей, как: \n \n🔹 BSRGAN \n🔹 Real_ESRGAN, \n🔹 SwinIr \n \nНеобходимо в начале запустить бота, затем загрузить изображение и выбрать модель, которую Вы хотите опробывать.")

@dp.message(F.text == "Загрузить изображение")
async def with_start(message: types.Message):
    config.GET_IMAGE = True
    await message.answer("Загрузите любое изображение", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.photo)
async def get_photo(message: types.Message):
    if config.GET_IMAGE:
        config.GET_IMAGE = False
        await message.bot.download(file=message.photo[-1].file_id, destination=config.TEST_NAME)
        shutil.move(config.TEST_NAME, config.UPLOAD_PATH)
        kb = [
            [
                types.KeyboardButton(text="BSRGAN"),
                types.KeyboardButton(text="Real-ESRGAN"),
                types.KeyboardButton(text="SwinIR")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите модель"
        )
        await message.answer("Ваше изображение получено. \nВыберите модель для обработки.", reply_markup=keyboard)
    else:
        await message.answer("На данный момент вы не можете отправить изображение.")
        


# @dp.message(F.text == "Real-ESRGAN")
# async def with_puree(message: types.Message):
    # cd BSRGAN
    # %python main_test_bsrgan.py
    # %cd ..
    # ESRGAN_main() # chec
    # photo = open(os.path.join(config.RESULT_PATH, config.TEST_NAME), 'rb')
    # await message.send_photo(chat_id=message.chat.id, photo=photo)
    # await message.answer("Данный бот создан для демонстрации работы 
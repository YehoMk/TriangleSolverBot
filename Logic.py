import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from math import cos, acos, radians, degrees


# Ідея: https://pythonhow.com/how/check-if-a-string-is-a-float/#:~:text=To%20check%20if%20a%20string%20is%20a%20number%20(float)%20in,casted%20to%20float%20or%20not.
def value_check(value):
    incorrect_value = False
    for element in value.replace(".", ""):
        if element not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            incorrect_value = True
    if value == "0":
        incorrect_value = True
    if value.count(".") not in [0, 1]:
        incorrect_value = True
    if incorrect_value is False or value == "x":
        return True
    else:
        return False


TOKEN = "your_telegram_token"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = [1814281350]


@dp.message_handler(commands="start")
async def start(message: types.message):
    action_choice = InlineKeyboardMarkup()
    action_choice.add(InlineKeyboardButton(text="Теорема Піфагора", callback_data="Теорема Піфагора"))
    action_choice.add(InlineKeyboardButton(text="Теорема косинусів", callback_data="Теорема косинусів"))
    await message.answer(text="Привіт. Я калькулятор трикутників. Оберіть вашу дію.", reply_markup=action_choice)


@dp.callback_query_handler(text="Теорема Піфагора")
async def t1_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ви обрали теорему Піфагора!")
    with open("t1_media.jpg", "rb") as photo:
        await bot.send_photo(call.message.chat.id, photo)
    await call.message.answer("Введіть <b>катет (1)</b>:", parse_mode="html")
    await state.set_state("t1_insert_cathetus_a")


t1_cathetus_a = 0


@dp.message_handler(state="t1_insert_cathetus_a")
async def t1_cathetus_a_handler(message: types.message, state: FSMContext):
    global t1_cathetus_a
    t1_cathetus_a = message.text
    if value_check(t1_cathetus_a):
        print(f"t1_cathetus_a: {t1_cathetus_a}")
        await message.answer(text="Введіть <b>катет (2)</b>:", parse_mode="html")
        await state.set_state("t1_insert_cathetus_b")
    else:
        print('t1_cathetus_a: Помилка')
        await message.answer(text="<i>Помилка! Введіть правельне значення.</i>", parse_mode="html")

t1_cathetus_b = 0


@dp.message_handler(state="t1_insert_cathetus_b")
async def t1_cathetus_b_handler(message: types.message, state: FSMContext):
    global t1_cathetus_b
    t1_cathetus_b = message.text
    if value_check(t1_cathetus_b):
        print(f"t1_cathetus_b: {t1_cathetus_b}")
        await message.answer(text="Введіть <b>гіпотенузу</b>:", parse_mode="html")
        await state.set_state("t1_insert_hypotenuse")
    else:
        print('t1_cathetus_b: Помилка')
        await message.answer(text="<i>Помилка! Введіть правельне значення.</i>", parse_mode="html")


t1_hypotenuse = 0


@dp.message_handler(state="t1_insert_hypotenuse")
async def t1_hypotenuse_handler(message: types.message, state: FSMContext):
    global t1_hypotenuse
    t1_hypotenuse = message.text
    if value_check(t1_hypotenuse):
        print(f"t1_hypotenuse: {t1_hypotenuse}")
        await state.set_state("t1_calculate")
        await message.answer(text="<i>Підтвердити?</i>", parse_mode="html")
    else:
        print('t1_hypotenuse : Помилка')
        await message.answer(text="<i>Помилка! Введіть правельне значення.</i>", parse_mode="html")


@dp.message_handler(state="t1_calculate")
async def t1_calculator(message: types.message, state: FSMContext):
    global t1_cathetus_a, t1_cathetus_b, t1_hypotenuse

    t1_variable_count = 0
    if t1_cathetus_a == "x":
        t1_variable_count += 1
    if t1_cathetus_b == "x":
        t1_variable_count += 1
    if t1_hypotenuse == "x":
        t1_variable_count += 1
    if t1_variable_count == 0:
        await message.answer(text="<i>Помилка! Ви не позначили жодного x.</i>", parse_mode="html")
        await state.finish()
    elif t1_variable_count == 2:
        await message.answer(text="<i>Помилка! Ви позначили два x.</i>", parse_mode="html")
        await state.finish()
    elif t1_variable_count == 3:
        await message.answer(text="<i>Помилка! Ви позначили три x.</i>", parse_mode="html")
        await state.finish()
    elif t1_variable_count == 1:
        if t1_cathetus_a == "x":
            if float(t1_hypotenuse) > float(t1_cathetus_b):
                answer = (float(t1_hypotenuse)**2 - float(t1_cathetus_b)**2)**0.5
                await message.answer(text=f"Приблизна довжина <b>катету (1)</b>:\n<b><i>{answer}</i></b>", parse_mode="html")
                await state.finish()
            else:
                await message.answer(text="<i>Помилка! Ви ввели не дійсні значення.</i>", parse_mode="html")
                await state.finish()
        elif t1_cathetus_b == "x":
            if float(t1_hypotenuse) > float(t1_cathetus_a):
                answer = (float(t1_hypotenuse)**2 - float(t1_cathetus_a)**2)**0.5
                await message.answer(text=f"Приблизна довжина <b>катету (2)</b>:\n<b><i>{answer}</i></b>", parse_mode="html")
                await state.finish()
            else:
                await message.answer(text="<i>Помилка! Ви ввели не дійсні значення.</i>", parse_mode="html")
                await state.finish()
        elif t1_hypotenuse == "x":
            answer = (float(t1_cathetus_a)**2 + float(t1_cathetus_b)**2)**0.5
            await message.answer(text=f"Приблизна довжина <b>гіпотенузи</b>:\n<b><i>{answer}</i></b>", parse_mode="html")
            await state.finish()
    else:
        await state.finish()


@dp.callback_query_handler(text="Теорема косинусів")
async def t2_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ви обрали теорему косинусів!")
    with open("t2_media.jpg", "rb") as photo:
        await bot.send_photo(call.message.chat.id, photo)
    await call.message.answer("Введіть <b>сторону прилеглу до кута (1)</b>:", parse_mode="html")
    await state.set_state("t2_insert_angleside_a")


t2_angleside_a = 0


@dp.message_handler(state="t2_insert_angleside_a")
async def t2_angleside_a_handler(message: types.message, state: FSMContext):
    global t2_angleside_a
    t2_angleside_a = message.text
    if value_check(t2_angleside_a):
        print(f"t2_angleside_a: {t2_angleside_a}")
        await message.answer("Введіть <b>сторону прилеглу до кута (2)</b>:", parse_mode="html")
        await state.set_state("t2_insert_angleside_b")
    else:
        print('t2_angleside_a: Помилка')
        await message.answer(text="<i>Помилка! Введіть правельне значення</i>.", parse_mode="html")


t2_angleside_b = 0


@dp.message_handler(state="t2_insert_angleside_b")
async def t2_angleside_b_handler(message: types.message, state: FSMContext):
    global t2_angleside_b
    t2_angleside_b = message.text
    if value_check(t2_angleside_b):
        print(f"t2_angleside_b: {t2_angleside_b}")
        await message.answer("Введіть градусну міру <b>кута</b>:", parse_mode="html")
        await state.set_state("t2_insert_angle")
    else:
        print('t2_angleside_b: Помилка')
        await message.answer(text="<i>Помилка! Введіть правельне значення.</i>", parse_mode="html")

t2_angle = 0


@dp.message_handler(state="t2_insert_angle")
async def t2_angle_handler(message: types.message, state: FSMContext):
    global t2_angle
    t2_angle = message.text
    if value_check(t2_angle):
        if t2_angle != "x":
            if 180 > float(t2_angle) > 0:
                print(f"t2_angle: {t2_angle}")
                await message.answer("Введіть <b>сторну проти кута</b>:", parse_mode="html")
                await state.set_state("t2_insert_side")
            else:
                print('t2_angle: Помилка')
                await message.answer(text="<i>Помилка! Введіть правельне значення.</i>", parse_mode="html")
        elif t2_angle == "x":
            print(f"t2_angle: {t2_angle}")
            await message.answer("Введіть <b>сторну проти кута</b>:", parse_mode="html")
            await state.set_state("t2_insert_side")
    else:
        print('t2_angle: Помилка')
        await message.answer(text="<i>Помилка! Введіть правельне значення.</i>", parse_mode="html")


t2_side = 0


@dp.message_handler(state="t2_insert_side")
async def t2_side_handler(message: types.message, state: FSMContext):
    global t2_side
    t2_side = message.text
    if value_check(t2_side):
        print(f"t2_side: {t2_side}")
        await state.set_state("t2_calculate")
        await message.answer(text="<i>Підтвердити?</i>", parse_mode="html")
    else:
        print('t2_angle: Помилка')
        await message.answer(text="<i>Помилка! Введіть правельне значення.</i>", parse_mode="html")


@dp.message_handler(state="t2_calculate")
async def t2_calculator(message: types.message, state: FSMContext):
    global t2_angleside_a, t2_angleside_b, t2_angle, t2_side

    t2_variable_count = 0
    if t2_angleside_a == "x":
        t2_variable_count += 1
    if t2_angleside_b == "x":
        t2_variable_count += 1
    if t2_angle == "x":
        t2_variable_count += 1
    if t2_side == "x":
        t2_variable_count += 1
    if t2_variable_count == 0:
        await message.answer(text="<i>Помилка! Ви не позначили жодного x.</i>", parse_mode="html")
        await state.finish()
    elif t2_variable_count == 2:
        await message.answer(text="<i>Помилка! Ви позначили два x.</i>", parse_mode="html")
        await state.finish()
    elif t2_variable_count == 3:
        await message.answer(text="<i>Помилка! Ви позначили три x.</i>", parse_mode="html")
        await state.finish()
    elif t2_variable_count == 4:
        await message.answer(text="<i>Помилка! Ви позначили чотири x.</i>", parse_mode="html")
        await state.finish()
    elif t2_variable_count == 1:
        if t2_side == "x":
            answer = (float(t2_angleside_a)**2 + float(t2_angleside_b)**2 - 2 * float(t2_angleside_a) * float(t2_angleside_b) * cos(radians(float(t2_angle))))**0.5
            await message.answer(text=f"Приблизна довжина <b>сторони проти кута</b>:\n<b><i>{round(answer, 13)}</i></b>", parse_mode="html")
        elif t2_angle == "x":
            angle_measure = -((float(t2_side)**2 - float(t2_angleside_a)**2 - float(t2_angleside_b)**2)/(2 * float(t2_angleside_a) * float(t2_angleside_b)))
            if 180 > degrees(angle_measure) > 0:
                answer = degrees(acos(angle_measure))
                await message.answer(text=f"Приблизна градусна міра <b>кута</b>:\n<b><i>{round(answer, 13)}</i></b>", parse_mode="html")
            else:
                await message.answer(text=f"<i>Помилка! Ви ввели некоректні значення.</i>", parse_mode="html")
        elif t2_angleside_a == "x":
            t2_quadratic_coefficient = 1
            t2_linear_coefficient = -(2 * float(t2_angleside_b) * cos(radians(float(t2_angle))))
            t2_constant_coefficient = float(t2_angleside_b)**2 - float(t2_side)**2
            t2_discriminant = float(t2_linear_coefficient)**2 - 4 * float(t2_quadratic_coefficient) * float(t2_constant_coefficient)
            if t2_discriminant > 0:
                t2_solution_1 = (-float(t2_linear_coefficient) + t2_discriminant**0.5)/2
                t2_solution_2 = (-float(t2_linear_coefficient) - t2_discriminant**0.5)/2
                if t2_solution_1 > 0:
                    answer = t2_solution_1
                    await message.answer(text=f"Приблизна довжина <b>сторони прилеглої до кута (1)</b>:\n<b><i>{round(answer, 13)}</i></b>", parse_mode="html")
                elif t2_solution_2 > 0:
                    answer = t2_solution_2
                    await message.answer(text=f"Приблизна довжина <b>сторони прилеглої до кута (1)</b>:\n<b><i>{round(answer, 13)}</i></b>", parse_mode="html")
                else:
                    await message.answer(text=f"<i>Помилка! Ви ввели некоректні значення.</i>", parse_mode="html")
        elif t2_angleside_b == "x":
            t2_quadratic_coefficient = 1
            t2_linear_coefficient = -(2 * float(t2_angleside_a) * cos(radians(float(t2_angle))))
            t2_constant_coefficient = float(t2_angleside_a)**2 - float(t2_side)**2
            t2_discriminant = float(t2_linear_coefficient)**2 - 4 * float(t2_quadratic_coefficient) * float(t2_constant_coefficient)
            if t2_discriminant > 0:
                t2_solution_1 = (-float(t2_linear_coefficient) + t2_discriminant**0.5)/2
                t2_solution_2 = (-float(t2_linear_coefficient) - t2_discriminant**0.5)/2
                if t2_solution_1 > 0:
                    answer = t2_solution_1
                    await message.answer(text=f"Приблизна довжина <b>сторони прилеглої до кута (2)</b>:\n<b><i>{round(answer, 13)}</b></i>", parse_mode="html")
                elif t2_solution_2 > 0:
                    answer = t2_solution_2
                    await message.answer(text=f"Приблизна довжина <b>сторони прилеглої до кута (2)</b>:\n<b><i>{round(answer, 13)}</b></i>", parse_mode="html")
                else:
                    await message.answer(text=f"<i>Помилка! Ви ввели некоректні значення.</i>", parse_mode="html")
            else:
                await message.answer(text=f"<i>Помилка! Ви ввели некоректні значення.</i>", parse_mode="html")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp)

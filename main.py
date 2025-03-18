import os
import json
import asyncio
import timer
import move_engine
from quart import Quart, request, render_template, redirect, url_for

# Визначення шляху до папки для збереження аудіофайлів "music"
UPLOAD_FOLDER = os.path.join(os.getcwd(), "music")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Шлях до файлу конфігурації
CONFIG_FILE = os.path.join(os.getcwd(), "config.json")


def load_config():
    """Завантажує конфігурацію з файлу. Якщо файлу немає — створює його із значенням за замовчуванням."""
    if not os.path.exists(CONFIG_FILE):
        config = {"steps_per_revolution": 400}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        return config
    else:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)


def update_config(new_config):
    """Оновлює конфігураційний файл."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(new_config, f)


# Завантажуємо конфігурацію при старті застосунку
config_data = load_config()
# Глобальна змінна, яку можна імпортувати в інші модулі
steps_per_revolution = config_data.get("steps_per_revolution", 400)

app = Quart(__name__)



@app.route('/upload_melodiya', methods=['POST'])
async def upload_melodiya():
    files = await request.files
    melodiya_file = files.get('melodiya')
    if melodiya_file:
        fixed_filename = "melodiya_audio.mp3"
        file_path = os.path.join(UPLOAD_FOLDER, fixed_filename)
        await melodiya_file.save(file_path)
        return redirect(url_for('index'))
    else:
        return {"error": "No melody sound file provided"}, 400


@app.route('/upload_stuk', methods=['POST'])
async def upload_stuk():
    files = await request.files
    stuk_file = files.get('stuk')
    if stuk_file:
        fixed_filename = "stuk_audio.mp3"
        file_path = os.path.join(UPLOAD_FOLDER, fixed_filename)
        await stuk_file.save(file_path)
        return redirect(url_for('index'))
    else:
        return {"error": "No knock sound file provided"}, 400


@app.route('/')
async def index():
    return await render_template('index.html')


@app.route('/set_steps', methods=['POST'])
async def set_steps():
    form_data = await request.form
    try:
        new_steps = int(form_data['steps_per_revolution'])
    except ValueError:
        return "Invalid input", 400

    # Оновлюємо глобальну змінну та конфігураційний файл
    global steps_per_revolution, config_data
    steps_per_revolution = new_steps
    config_data["steps_per_revolution"] = new_steps
    update_config(config_data)

    return redirect(url_for('index'))


@app.route('/calibrate_fact', methods=['POST'])
async def calibrate_fact():
    @app.route('/calibrate_fact', methods=['POST'])
    async def calibrate_fact():
        # Отримуємо дані форми
        form_data = await request.form
        # Очікуємо, що поле називається "calibration_time" (при використанні <input type="time" name="calibration_time">)
        calibration_time_str = form_data.get('calibration_time')
        if not calibration_time_str:
            return {"error": "Не вказано час для калібрування."}, 400

        # Очікуємо формат "HH:MM"
        try:
            entered_hour, entered_minute = map(int, calibration_time_str.split(':'))
        except ValueError:
            return {"error": "Некоректний формат часу. Очікується формат HH:MM."}, 400

        # Отримуємо поточний час за допомогою модуля time
        now = time.localtime()
        current_hour = now.tm_hour
        current_minute = now.tm_min

        # Перетворення часу у години та хвилини в загальну кількість хвилин від початку доби
        entered_total = entered_hour * 60 + entered_minute
        current_total = current_hour * 60 + current_minute

        # Різниця = введений час - поточний час
        difference = entered_total - current_total
        move_engine.step(difference)



@app.route('/calibrate', methods=['POST'])
async def calibrate():
    form_data = await request.form
    calibration_value = form_data.get('calibration_steps', '')
    if not calibration_value.strip():
        return "Помилка: поле 'Кількість кроків для калібрування' не може бути пустим.", 400

    try:
        calibration_steps = int(calibration_value)
    except ValueError:
        return "Помилка: введене значення не є числом.", 400

    await move_engine.step(calibration_steps)
    return redirect(url_for('index'))


async def background_timer():
    """Фоновий таск, який періодично викликає timer.run()."""
    try:
        while True:
            await timer.run()  # Функція timer.run() має бути реалізована асинхронно
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Background timer cancelled properly.")
        raise


@app.before_serving
async def startup():
    global background_task
    background_task = asyncio.create_task(background_timer())


@app.after_serving
async def shutdown():
    global background_task
    if background_task is not None:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            print("Background task successfully cancelled.")


if __name__ == '__main__':
    from hypercorn.config import Config
    import hypercorn.asyncio

    config = Config()
    config.bind = ["192.168.1.243:5000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))

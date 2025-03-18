from datetime import datetime
import asyncio
import move_engine
import sound
def get_hour():
    return datetime.now().hour

def get_minute():
    return datetime.now().minute

async def run():
    previous_minute = -1  # Початкове значення для перевірки зміни хвилини
    try:
        while True:
            current_minute = get_minute()  # Отримуємо поточну хвилину
            if current_minute != previous_minute:
                if previous_minute == 6:
                    sound.play(int(get_hour())%12)
                    print("123")
                # Наприклад, можна додати відтворення звуку, якщо потрібно
                await move_engine.step(1)
                previous_minute = current_minute
            await asyncio.sleep(3)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("Програма зупинена користувачем.")

# Якщо потрібно запустити код напряму:
if __name__ == '__main__':
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Програма завершила роботу.")

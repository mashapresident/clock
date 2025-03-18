import vlc
import asyncio
import time


def play_sound(filename):
    """
    Синхронна функція для відтворення MP3-файлу за допомогою VLC.
    Функція блокує виконання, поки медіа не завершить відтворення.
    """
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(filename)
    player.set_media(media)

    player.play()
    # Дамо плеєру кілька сотих секунди для старту відтворення
    time.sleep(0.2)
    while True:
        state = player.get_state()
        if state in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
            break
        time.sleep(0.1)


async def play(hour):
    """
    Асинхронна функція, яка послідовно:
      1. Відтворює мелодію.
      2. Потім відтворює звук клаку hour разів.
    """
    # Спочатку запускаємо відтворення мелодії.
    await asyncio.to_thread(play_sound, "music/melodiya_audio.mp3")

    # Потім, для кожної ітерації, відтворюємо звук клаку.
    for i in range(1, hour + 1):
        print(f"Відтворення звуку клаку — ітерація {i}")
        await asyncio.to_thread(play_sound, "music/stuk_audio.mp3")


# Приклад використання:
if __name__ == '__main__':
    # Наприклад, потрібно відтворити звук клаку 3 рази після мелодії
    asyncio.run(play(3))

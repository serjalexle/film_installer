import librosa
import numpy as np

async def get_epic_time_on_audio(audio_path: str = "output_audio.mp3", num_segments: int = 10, segment_duration: float = 10.0):
    # Завантажуємо аудіофайл
    y, sr = librosa.load(audio_path)

    # Переводимо 5 хвилин у секунди
    min_time = 5 * 60
    max_time = (len(y) / sr) - 5 * 60

    # Довжина сегмента в фреймах
    segment_length_in_frames = int(segment_duration * sr)

    # Ділимо аудіо на фрейми з потрібною довжиною і обчислюємо середню амплітуду в кожному фреймі
    frames = librosa.util.frame(y, frame_length=segment_length_in_frames, hop_length=segment_length_in_frames)
    avg_amplitudes = np.mean(np.abs(frames), axis=0)

    # Визначаємо, де може грати музика, використовуючи метод для обчислення мел-кепстральних коефіцієнтів (MFCC)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_avg = np.mean(mfcc, axis=0)

    # Визначаємо індекси відрізків, які можуть відповідати музиці (нижчий поріг 60-й перцентиль)
    music_indices = np.where(mfcc_avg > np.percentile(mfcc_avg, 60))[0]

    # Знаходимо індекси найгучніших фреймів, де також може бути музика
    combined_indices = [i for i in np.argsort(avg_amplitudes)[-num_segments * 3:] if i in music_indices]

    # Конвертуємо індекси в час і фільтруємо їх за обмеженням 5 хвилин
    top_times = []
    for i in combined_indices:
        time_in_seconds = (i * segment_length_in_frames) / sr
        if min_time <= time_in_seconds <= max_time:
            top_times.append(time_in_seconds)

    # Відбираємо найкращі `num_segments` моментів
    top_times = sorted(top_times, key=lambda x: avg_amplitudes[int(x * sr / segment_length_in_frames)], reverse=True)[:num_segments]

    # Повертаємо список часових відрізків
    return [{"start_time": float(time), "duration": segment_duration} for time in top_times]

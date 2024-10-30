from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
    concatenate_audioclips,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    CompositeAudioClip,
)
from loguru import logger

import numpy as np


# Завантаження фільму
def load_movie(video_path):
    logger.info(f"Loading movie from {video_path}")
    return VideoFileClip(video_path)


# Вибір сцен на основі фіксованих тайм-кодів
def select_key_scenes(
    video, start_offset=5 * 60, end_offset=5 * 60, min_duration=60, max_duration=90
):
    logger.info("Selecting key scenes...")
    duration = video.duration

    key_moments = [start_offset, start_offset + 600, start_offset + 1200]

    selected_scenes = []
    total_duration = 0

    for moment in key_moments:
        if moment < start_offset or moment > (duration - end_offset):
            continue
        start_time = moment
        end_time = min(moment + 10, duration - end_offset)
        scene_duration = end_time - start_time
        selected_scenes.append((start_time, end_time))
        total_duration += scene_duration

        if total_duration >= min_duration:
            break

    if total_duration < min_duration:
        last_scene_start, last_scene_end = selected_scenes[-1]
        selected_scenes[-1] = (
            last_scene_start,
            last_scene_start + (min_duration - total_duration),
        )
        total_duration = min_duration

    logger.info(f"Total selected scenes duration: {total_duration} seconds")
    return selected_scenes


# Обрізаємо вибрані сцени
def cut_scenes(video, scenes):
    if not scenes:
        logger.warning("No scenes to cut.")
        return []

    logger.info("Cutting selected scenes from the movie...")
    clips = [video.subclip(start, end) for start, end in scenes]
    return clips


# Обрізаємо відповідне аудіо з фільму для вибраних сцен
def cut_audio_for_scenes(video, scenes):
    logger.info("Cutting audio for selected scenes...")
    audio_clips = [video.audio.subclip(start, end) for start, end in scenes]
    return concatenate_audioclips(audio_clips) if audio_clips else None


# Додаємо фонову музику та забезпечуємо її довжину
def add_music_to_trailer(music_path, trailer_duration):
    if music_path:
        logger.info("Adding background music to the trailer...")
        music = AudioFileClip(music_path)
        music_duration = music.duration

        # Якщо музика коротша за трейлер, повторюємо її
        if music_duration < trailer_duration:
            loops = int(np.ceil(trailer_duration / music_duration))
            music = concatenate_audioclips([music] * loops).subclip(0, trailer_duration)
        else:
            music = music.subclip(0, trailer_duration)

        return music
    return None


# Об'єднуємо фонову музику та приглушений оригінальний звук
def combine_audio(video_audio, background_music):
    logger.info("Combining movie audio with background music...")
    # Використовуємо CompositeAudioClip для об'єднання
    combined_audio = CompositeAudioClip(
        [video_audio.volumex(0.3), background_music.volumex(0.7)]
    )
    return combined_audio


# Додаємо текстові вставки (назва фільму, дати)
def add_text_to_trailer(trailer, film_title, release_date):
    logger.info("Adding title and release date to the trailer...")
    title_clip = (
        TextClip(film_title, fontsize=70, color="white")
        .set_duration(3)
        .set_position("center")
    )
    date_clip = (
        TextClip(f"Coming: {release_date}", fontsize=50, color="white")
        .set_duration(3)
        .set_position("center")
    )

    final_trailer = CompositeVideoClip(
        [
            trailer,
            title_clip.set_start(0).set_duration(3),
            date_clip.set_start(3).set_duration(3),
        ]
    )
    return final_trailer


# Експорт трейлера
def export_trailer(trailer, output_path):
    logger.info(f"Exporting trailer to {output_path}...")
    trailer.write_videofile(output_path, codec="libx264")


# Основна функція створення трейлера
def create_trailer(video_path, music_path, output_path, film_title, release_date):
    # 1. Завантаження фільму
    video = load_movie(video_path)

    # 2. Вибір сцен (мінімум 1 хвилина, максимум 1.5 хвилини)
    selected_scenes = select_key_scenes(video, min_duration=60, max_duration=90)

    # 3. Обрізаємо сцени
    clips = cut_scenes(video, selected_scenes)

    if not clips:
        logger.error("No clips were selected for the trailer. Exiting.")
        return

    # 4. З'єднання сцен
    trailer = concatenate_videoclips(clips)

    # 6. Обрізаємо звук фільму
    video_audio = cut_audio_for_scenes(video, selected_scenes)

    # 7. Додаємо фонову музику
    trailer_duration = trailer.duration
    background_music = add_music_to_trailer(music_path, trailer_duration)

    # 8. Поєднуємо аудіо фільму та музику за допомогою CompositeAudioClip
    combined_audio = combine_audio(video_audio, background_music)
    trailer = trailer.set_audio(combined_audio)

    # 9. Фінальне редагування: назва фільму, дати
    trailer = add_text_to_trailer(trailer, film_title, release_date)

    # 10. Експорт трейлера
    export_trailer(trailer, output_path)


# Викликаємо функцію для створення трейлера
create_trailer(
    video_path="film.mp4",
    music_path="sound.mp3",
    output_path="trailer.mp4",
    film_title="Epic Movie",
    release_date="December 2024",
)



import pygame

pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=256
)

pygame.init()

pygame.mixer.set_num_channels(32)

#Menu sounds and music
sounds = {
    "m": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/deltarune-menu-move-2-0.mp3"
    ),
    "s": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/deltarune-menu-select.mp3"
    ),
    "mm": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/man_2.ogg"
    ),
    "mf": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/34. NORTHERNLIGHT (DELTARUNE Chapter 3+4 Soundtrack) - Toby Fox.mp3"
    ),
    "mfr": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/imagefriend.mp3"
    ),
    "s1": pygame.mixer.Sound(
        "assets/Sounds and music/HERO_SWORD/snd_board_sword1.wav"
    ),
    "s2": pygame.mixer.Sound(
        "assets/Sounds and music/HERO_SWORD/snd_board_sword2.wav"
    ),
    "s3": pygame.mixer.Sound(
        "assets/Sounds and music/HERO_SWORD/snd_board_sword3.wav"
    ),
    "ed": pygame.mixer.Sound(
        "assets/Sounds and music/MUS/37. ERAM (DELTARUNE Chapter 3+4 Soundtrack) - Toby Fox.mp3"
    ),
    "eb": pygame.mixer.Sound(
        "assets/Sounds and music/MUS/38. BURNING EYES (DELTARUNE Chapter 3+4 Soundtrack.MP3"
    ),
    "el": pygame.mixer.Sound(
        "assets/Sounds and music/ERAM/snd_board_mantle_laugh_fast.ogg"
    ),
    "kd": pygame.mixer.Sound(
        "assets/Sounds and music/HERO_SWORD/snd_board_playerhurt.ogg"
    ),
    "md": pygame.mixer.Sound(
        "assets/Sounds and music/ERAM/snd_board_bosshit.ogg"
    ),
    "bt": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/snd_board_throw.wav"
    ),
    "bb": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/snd_board_bomb.wav"
    ),
    "bf": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/snd_board_torch.wav"
    ),
    "msd": pygame.mixer.Sound(
        "assets/Sounds and music/ERAM/snd_board_mantle_dash_slow.wav"
    ),
    "fa": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/snd_board_summon.wav"
    ),
    "h": pygame.mixer.Sound(
        "assets/Sounds and music/OTHERS/heal.wav"
    ),
}


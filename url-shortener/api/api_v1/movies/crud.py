from schemas.movie import Movie

MOVIES = [
    Movie(
        slug="Чтиво",
        title="Криминальное чтиво",
        description="Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса Марселласа Уоллеса.",
        year=1995,
        duration=154,
    ),
    Movie(
        slug="Рассвет",
        title="От заката до рассвета",
        description="Спасаясь от полиции после ограбления банка, два брата-преступника берут в заложники священника с двумя детьми и бегут в Мексику. Там они должны дождаться подельника, а для этого всей компании нужно переждать ночь в баре дальнобойщиков.",
        year=1995,
        duration=108,
    ),
    Movie(
        slug="Уб",
        title="Бесславные ублюдки",
        description="Вторая мировая война. В оккупированной немцами Франции группа американских солдат-евреев наводит страх на нацистов, жестоко убивая и скальпируя солдат.",
        year=2009,
        duration=153,
    ),
]

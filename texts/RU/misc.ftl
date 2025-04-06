currency_symbol_by_enum = { $currency ->
    [RUB] ₽
    [USD] $
    [EUR] €
    [UAH] ₴
    *[other] unexpected
}

close = X Закрыть

back = < Назад

refresh = 🔄 Обновить

skip = Пропустить

upload = { $content_type ->
    [photo] <b>📷 Подгружаю фото...</b>
    [video] <b>📼 Подгружаю видео...</b>
    [animation] <b>💾 Подгружаю GIF...</b>
    *[other] <b>Неизвестный тип</b>
}

null-username = Юзер
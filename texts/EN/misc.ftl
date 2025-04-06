currency_symbol_by_enum = { $currency ->
    [RUB] ₽
    [USD] $
    [EUR] €
    [UAH] ₴
    *[other] unexpected
}

close = X Close

back = < Back

refresh = 🔄 Refresh

skip = Skip

upload = { $content_type ->
    [photo] <b>📷 Uploading photo...</b>
    [video] <b>📼 Uploading video...</b>
    [animation] <b>💾 Uploading GIF...</b>
    *[other] <b>Unknown type</b>
}

null-username = User

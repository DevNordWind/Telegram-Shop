user-info = { $is_username ->
    [True] 👤 Пользователь: <b>@{$username}</b> | <a href='tg://user?id={$user_id}'>{$first_name}</a> | <code>{$user_id}</code>
    *[other] 👤 Пользователь: <a href='tg://user?id={$user_id}'>{$first_name}</a> | <code>{$user_id}</code>
}

user-notify-payment = <b>💰 Вы пополнили баланс на сумму <code>{$amount}{currency_symbol_by_enum}</code>. Удачи ❤️
    🧾 Чек: <code>#{$payment_id}</code></b>

admin-notify-payment = { user-info }
        💰 Сумма пополнения: <code>{$amount}{currency_symbol_by_enum}</code> <code>({$payment_method})</code>
        🧾 Чек: <code>#{$payment_id}</code>
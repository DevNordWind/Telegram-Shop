user-info = { $is_username ->
    [True] 👤 User: <b>@{$username}</b> | <a href='tg://user?id={$user_id}'>{$first_name}</a> | <code>{$user_id}</code>
    *[other] 👤 User: <a href='tg://user?id={$user_id}'>{$first_name}</a> | <code>{$user_id}</code>
}

user-notify-payment = <b>💰 You have topped up your balance by <code>{$amount}{currency_symbol_by_enum}</code>. Good luck ❤️
    🧾 Receipt: <code>#{$payment_id}</code></b>

admin-notify-payment = { user-info }
        💰 Top-up Amount: <code>{$amount}{currency_symbol_by_enum}</code> <code>({$payment_method})</code>
        🧾 Receipt: <code>#{$payment_id}</code>
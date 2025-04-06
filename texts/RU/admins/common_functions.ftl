common-functions = <b>🔆 Общие функции бота</b>
    .find-btn = 🔍 Поиск
    .mailing-btn = 📢 Рассылка

find = <b>🔍 Отправьте айди/логин пользователя или номер чека</b>
    .not-found = <b>❌ Данные не были найдены</b>

user-name = { $username ->
    [None] {null-username}
    *[other] {$username}
}

user-profile = 👤 Профиль пользователя: { $first_name}
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ ID: <code>{$user_id}</code>
    ▪️ Логин: @{ $username}
    ▪️ Регистрация: <code>{ $reg_time }</code>

    ▪️ Рублёвый баланс: <code>{ $rub_wallet_amount }₽</code>
    ▪️ Долларвый баланс: <code>{ $usd_wallet_amount }$</code>
    ▪️ Всего выдано: {$total_give}{currency_symbol_by_enum}
    ▪️ Всего пополнено: {$total_refill}{currency_symbol_by_enum}
    ▪️ Куплено товаров: { $items_amount}
    .change-balance-btn = 💰 Уменьшить баланс
    .give-balance-btn = 💰 Прибавить баланс
    .items-btn =  🎁 Покупки
    .send-msg-btn = 💌 Отправить сообщение

refill-find = <b>🧾 Чек: <code>#{$id}</code></b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Пользователь: @{$username} | <code>{$user_id}</code>
        ▪️ Сумма пополнения: <code>{$amount}{currency_symbol_by_enum}</code>
        ▪️ Способ пополнения: <code>{$payment_method}</code>
        ▪️ Комментарий: <code>{$comment}</code>
        ▪️ Дата пополнения: <code>{$created_at}</code>

purchase-find = <b>🧾 Чек: <code>#{$id}</code></b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Пользователь: @{$username} | <code>{$user_id}</code>

        ▪️ Название позиции: <code>{$position_name}</code>
        ▪️ Куплено товаров: <code>{$items_count}шт</code>
        ▪️ Цена одного товара: <code>{$item_amount}{currency_symbol_by_enum}</code>
        ▪️ Сумма покупки: <code>{$items_amount}{currency_symbol_by_enum}</code>

        ▪️ Баланс до покупки: <code>{$balance_before}{currency_symbol_by_enum}</code>
        ▪️ Баланс после покупки: <code>{$balance_after}{currency_symbol_by_enum}</code>

        ▪️ Дата покупки: <code>{$created_at}</code>
    .unload-items-btn = 🎁 Выгрузить товары


select-currency = <b>💱 Выберите валюту кошелька</b>

input-amount-change-balance = <b>✏️ Введи сумму</b>
    .notify-refill = <b>💰 Вам было выдано <code>{ $amount }{currency_symbol_by_enum}</code></b>
    .notify-withdraw = <b>💰 Администратор снял с вашего баланса <code>{$amount}{currency_symbol_by_enum}</code></b>

input-message = <b>✏️ Введи сообщение для пользователя</b>
    .notify-user = <b>💌 Сообщение от администрации:</b>
        <code>{$msg}</code>
    .notify-admin-success = <b>✅ Сообщение было успешно отправлено</b>
    .notify-admin-fail = <b>❌ Сообщение было отправлено с ошибкой! Похоже, пользователь удалил чат с ботом</b>


mailing = <b>📢 Отправьте пост для рассылки пользователям</b>

    <i>ℹ️ Поддерживаются: <code>Видео, Анимациия(GIF), Фото</code></i>
    .en = <b>✏️ Введите текст на английском, либо пропустите этот шаг(все пользователи получат рассылку на русском языке)</b>

mailing-approve = <b>📢 Отправить { $users_count } юзерам пост?</b>
    .approve-btn = ✅ Отправить
    .cancel-btn = ❌ Отменить

mailing-start = <b>📢 Рассылка началась... ({ $sent_messages }/{ $users_count})</b>
    .done =  <b>📢 Рассылка была завершена</b>
            ➖➖➖➖➖➖➖➖➖➖
            👤 Всего пользователей: <code>{ $users_count}</code>
            ✅ Пользователей получило сообщение: <code>{ $success_msg}</code>
            ❌ Пользователей не получило сообщение: <code>{ $error_msg}</code>


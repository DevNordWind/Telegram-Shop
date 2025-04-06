profile = <b>👤 Ваш профиль</b>
        ➖➖➖➖➖➖➖➖➖➖
        🆔 ID: <code>{ $user_id }</code>
        🎁 Покупок: <code>{ $count_items }шт</code>
        ➖➖➖➖➖➖➖➖➖➖
        💰 Баланс: <code>{ $amount }{ currency_symbol_by_enum }</code>
        ├ Всего: ~<code>{$total_amount}{currency_symbol_by_enum}</code>

        🕰 Регистрация: <code>{ $reg_time }</code>
    .refill-btn = 💰 Пополнить
    .purchases-btn = 🎁 Мои покупки
    .ch-lg-btn = 🇷🇺🇬🇧 Сменить язык
    .ch-currency-btn = 💱 Сменить валюту

purchases = <b>🎁 Покупки</b>
    .btn = 🎁 {$amount}{currency_symbol_by_enum} | {$item_count} Товаров | {$created_at}
    .none = <b>❌ Покупки отсутствуют :( </b>

relation-removed = Удалена ❌

purchase-details = <b>🎁 Покупка от <code>{$created_at}</code></b>
    ➖➖➖➖➖➖➖➖➖➖
    🗃 Категория: <code>{ $category_name }</code>
    📁 Позиция: <code>{ $position_name }</code>
    ➖➖➖➖➖➖➖➖➖➖
    💰 Сумма: <code>{$amount}{currency_symbol_by_enum}</code>
    🎁 Товаров: <code>{$item_count}шт.</code>
    🧾 Чек: <code>{ $id }</code>
    .unload-items-btn = 🎁 Выгрузить товары

ch-lg = <b>🇷🇺🇬🇧 Change language</b>
    .ch-kb = <b>🤖 Changing keyboard...</b>

ch-cur = <b>💱 Сменить валюту</b>

    <i> ℹ️ Выбранная валюта будет использоваться при пополнении баланса и покупке товаров</i>
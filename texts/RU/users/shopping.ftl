select-category = <b>🗃️ Выберите категорию</b>
    .unavailable = <B>⛔️ Покупки временно недоступны</b>

select-position = <b>📁 Выберите позицию</b>



position-details = <b>🎁 Покупка товара</b>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Название: <code>{ $position_name }</code>
    ▪️ Категория: <code>{ $category_name }</code>
    ▪️ Стоимость: <code>{ $price}{currency_symbol_by_enum}</code>
    ▪️ Количество: <code>{ $items_count}шт.</code>
    .description = ▪️ ️️Описание: { $description }
    .buy-btn = 💰 Купить
    .items-missing = ❗️ Товары отсутствуют

not-enough-money = ❗️ На вашем счёту недостаточно баланса.

    💰 <b>Перейти к пополнению</b>
    .refill-btn = 💰 Пополнить

input-amount-item = <b>🎁 Введите количество товаров для покупки</b>
    ❕ От <code>1</code> до <code>{ $max_possible_count}</code>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Товар: <code>{ $position_name}</code> - <code>{ $position_price}{currency_symbol_by_enum}</code>
    ▪️ Ваш баланс: <code>{ $balance }{currency_symbol_by_enum}</code>
    .not-enough-money = <b>❗️ На вашем счёту недостаточно баланса.</b>

approve-buy = <b>🎁 Вы действительно хотите купить товар(ы)?</b>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Товар: <code>{ $position_name }</code>
    ▪️ Количество: <code>{ $count_to_buy }шт.</code>
    ▪️ Сумма к покупке: <code>{ $amount_to_buy}{currency_symbol_by_enum}</code>
    .buy-btn = 💰 Купить

receipt = <b>✅ Успешная покупка</b>
    ➖➖➖➖➖➖➖➖➖➖
    💰 Сумма: <code>{$amount}{currency_symbol_by_enum}</code>
    🎁 Товаров: <code>{$item_count}шт.</code>
    🧾 Чек: <code>{ $id }</code>

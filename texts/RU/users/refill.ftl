refill = <b>💰 Введите сумму пополнения</b>

payment-system-by-enum = { $payment_method ->
    [CRYPTOBOT] 🤖 CryptoBot
    *[other] Unexpected
}

refill-disable = <b>❌ Пополнения временно недоступны</b>

select-payment-method = <b>💰 Выберите способ пополнения баланса</b>
    .cryptobot-btn = 🤖 CryptoBot


payment-instruction = { $payment_method ->
    [CRYPTOBOT] Для пополнения баланса, нажмите на кнопку ниже <code>Перейти к оплате</code> и оплатите выставленный вам счёт
    *[other] Неизвестно
}
payment-warning = { $payment_method ->
    [CRYPTOBOT] ℹ️ Если оплата не зачислилась автоматически, нажмите на <code>Проверить оплату</code>
    *[other] Неизвестно
}

invoice = <b>💰 Пополнение баланса</b>
    ➖➖➖➖➖➖➖➖➖➖
    {payment-instruction}
    ▪️ У вас имеется 3 часа на оплату счета
    ▪️ Сумма пополнения: <code>{ $amount }{ currency_symbol_by_enum }</code>
    ➖➖➖➖➖➖➖➖➖➖
    {payment-warning}
    .pay-btn = 🌀 Перейти к оплате
    .check-btn = 🔄 Проверить оплату
    .payment-not-found = ❌ Оплата не найдена

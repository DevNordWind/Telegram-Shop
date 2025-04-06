refill = <b>💰 Enter the top-up amount</b>

payment-system-by-enum = { $payment_method ->
    [CRYPTOBOT] 🤖 CryptoBot
    *[other] Unexpected
}

refill-disable = <b>❌ Top-up is temporarily unavailable</b>

payment-instruction = { $payment_method ->
    [CRYPTOBOT] ▪️ Purchase a Steam top-up card with an amount matching the amount to be purchased, and enter the activation code after pressing the <code>Enter code</code> button
    *[other] ▪️ To top up your balance, click the button below <code>Proceed to payment</code> and pay the invoice
}

payment-warning = { $payment_method ->
    [CRYPTOBOT] ℹ️ If payment is not automatically credited, click <code>Check payment</code>
    *[other] Unknown
}

invoice = <b>💰 Balance top-up</b>
    ➖➖➖➖➖➖➖➖➖➖
    {payment-instruction}
    ▪️ You have 3 hours to pay the invoice
    ▪️ Top-up amount: <code>{ $amount }{ currency_symbol_by_enum }</code>
    ➖➖➖➖➖➖➖➖➖➖
    {payment-warning}
    .pay-btn = 🌀 Proceed to payment
    .enter-code-btn = ✏️ Enter code
    .check-btn = 🔄 Check payment
    .payment-not-found = ❌ Payment not found
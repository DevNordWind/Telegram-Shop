select-category = <b>🗃 Select a category</b>
    .unavailable = <b>⛔️ Purchases are temporarily unavailable</b>

select-position = <b>📁 Select a position</b>

position-details = <b>🎁 Product purchase</b>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Name: <code>{ $position_name }</code>
    ▪️ Category: <code>{ $category_name }</code>
    ▪️ Price: <code>{ $price}{currency_symbol_by_enum}</code>
    ▪️ Quantity: <code>{ $items_count}pcs.</code>
    .description = ▪️ Description: { $description }
    .buy-btn = 💰 Buy
    .items-missing = ❗️ Items are missing

not-enough-money = ❗️ You do not have enough balance.

    💰 <b>Proceed to top up</b>
    .refill-btn = 💰 Top Up

input-amount-item = <b>🎁 Enter the quantity of items to purchase</b>
    ❕ From <code>1</code> to <code>{ $max_possible_count}</code>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Item: <code>{ $position_name}</code> - <code>{ $position_price}{currency_symbol_by_enum}</code>
    ▪️ Your balance: <code>{ $balance }{currency_symbol_by_enum}</code>
    .not-enough-money = <b>❗️ You do not have enough balance.</b>

approve-buy = <b>🎁 Do you really want to buy the item(s)?</b>
    ➖➖➖➖➖➖➖➖ ➖➖
    ▪️ Item: <code>{ $position_name }</code>
    ▪️ Quantity: <code>{ $count_to_buy }pcs.</code>
    ▪️ Total purchase amount: <code>{ $amount_to_buy}{currency_symbol_by_enum}</code>
    .buy-btn = 💰 Buy

receipt = <b>✅ Successful Purchase</b>
    ➖➖➖➖➖➖➖➖➖➖
    💰 Amount: <code>{$amount}{currency_symbol_by_enum}</code>
    🎁 Items: <code>{$itemcount}pcs.</code>
    🧾 Receipt: <code>{ $id }</code>
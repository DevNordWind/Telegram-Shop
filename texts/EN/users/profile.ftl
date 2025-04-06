profile = <b>👤 Your Profile</b>
        ➖➖➖➖➖➖➖➖➖➖
        🆔 ID: <code>{ $user_id }</code>
        🎁 Purchases: <code>{ $count_items }pcs</code>
        ➖➖➖➖➖➖➖➖➖➖
        💰 Balance: <code>{ $amount }{ currency_symbol_by_enum }</code>
        ├ Total: ~<code>{$total_amount}{currency_symbol_by_enum}</code>

        🕰 Registration: <code>{ $reg_time }</code>
    .refill-btn = 💰 Top Up
    .purchases-btn = 🎁 My Purchases
    .ch-lg-btn = 🇷🇺🇬🇧 Change Language
    .ch-currency-btn = 💱 Change Currency

purchases = <b>🎁 Purchases</b>
    .btn = 🎁 {$amount}{currency_symbol_by_enum} | {$item_count} Items | {$created_at}
    .none = <b>❌ No purchases available :( </b>

relation-removed = Removed ❌

purchase-details = <b>🎁 Purchase from <code>{$created_at}</code></b>
    ➖➖➖➖➖➖➖➖➖➖
    🗃 Category: <code>{ $category_name }</code>
    📁 Position: <code>{ $position_name }</code>
    ➖➖➖➖➖➖➖➖➖➖
    💰 Amount: <code>{$amount}{currency_symbol_by_enum}</code>
    🎁 Items: <code>{$item_count}pcs</code>
    🧾 Receipt: <code>{ $id }</code>
    .unload-items-btn = 🎁 Unload products

ch-lg = <b>🇷🇺🇬🇧 Change Language</b>
    .ch-kb = <b>🤖 Changing keyboard...</b>

ch-cur = <b>💱 Change Currency</b>

    <i> ℹ️ The selected currency will be used for balance top-ups and purchasing goods.</i>
common-functions = <b>🔆 Bot's Common Functions</b>
    .find-btn = 🔍 Search
    .mailing-btn = 📢 Mailing

find = <b>🔍 Send the user ID/login or receipt number</b>
    .not-found = <b>❌ Data not found</b>

user-name = { $username ->
    [None] {null-username}
    *[other] {$username}
}

user-profile = 👤 User Profile: { $first_name}
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ ID: <code>{$user_id}</code>
    ▪️ Username: @{ $username}
    ▪️ Registration: <code>{ $reg_time }</code>

    ▪️ Ruble Balance: <code>{ $rub_wallet_amount }₽</code>
    ▪️ Dollar Balance: <code>{ $usd_wallet_amount }$</code>
    ▪️ Total Given: {$total_give}{currency_symbol_by_enum}
    ▪️ Total Refilled: {$total_refill}{currency_symbol_by_enum}
    ▪️ Items Purchased: { $items_amount}
    .change-balance-btn = 💰 Decrease Balance
    .give-balance-btn = 💰 Increase Balance
    .items-btn = 🎁 Purchases
    .send-msg-btn = 💌 Send Message

select-currency = <b>💱 Select Wallet Currency</b>

input-amount-change-balance = <b>✏️ Enter Amount</b>
    .notify-refill = <b>💰 You have been credited <code>{ $amount }{currency_symbol_by_enum}</code></b>
    .notify-withdraw = <b>💰 The administrator withdrew <code>{$amount}{currency_symbol_by_enum}</code> from your balance</b>

input-message = <b>✏️ Enter message for the user</b>
    .notify-user = <b>💌 Message from Admin:</b>
        <code>{$msg}</code>
    .notify-admin-success = <b>✅ Message was successfully sent</b>
    .notify-admin-fail = <b>❌ The message was sent with an error! It seems the user deleted the chat with the bot</b>

mailing = <b>📢 Send the post for user mailing</b>

    <i>ℹ️ Supported: <code>Video, Animation (GIF), Photo</code></i>
    .en = <b>✏️ Enter the text in English or skip this step (all users will receive the post in Russian)</b>

mailing-approve = <b>📢 Send post to { $users_count } users?</b>
    .approve-btn = ✅ Send
    .cancel-btn = ❌ Cancel

mailing-start = <b>📢 Mailing started... ({ $sent_messages }/{ $users_count})</b>
    .done = <b>📢 Mailing was completed</b>
            ➖➖➖➖➖➖➖➖➖➖
            👤 Total users: <code>{ $users_count}</code>
            ✅ Users received the message: <code>{ $success_msg}</code>
            ❌ Users did not receive the message: <code>{ $error_msg}</code>
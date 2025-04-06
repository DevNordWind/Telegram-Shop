product-management = <b>🎁 Product Management</b>
    .create-position-btn = 📁 Create Position ➕
    .edit-position-btn = 📁 Edit Position 🖍
    .create-category-btn = 🗃 Create Category ➕
    .edit-category-btn = 🗃 Edit Category 🖍
    .add-item-btn = 🎁 Add Items ➕
    .deleting-btn = ❌ Deletion

input-category-name = <b>🗃 Enter category name in Russian</b>
    .en = <b>🗃 Enter category name in English</b>

edit-category = <b>🗃 Editing Category</b>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Category: <code>{ $category_name }</code>
    ▪️ Number of Positions: <code>{ $position_count }</code>
    ▪️ Number of Items: <code>{ $item_amount } pcs</code>
    ▪️ Creation Date: <code>{ $created_at }</code>

    💸 Sales per Day: <code>{ $purchase_day_count }</code> - <code>{ $purchase_day_amount }{ currency_symbol_by_enum }</code>
    💸 Sales per Week: <code>{ $purchase_week_count }</code> - <code>{ $purchase_week_amount }{ currency_symbol_by_enum }</code>
    💸 Sales per Month: <code>{ $purchase_month_count }</code> - <code>{ $purchase_month_amount }{ currency_symbol_by_enum }</code>
    💸 Sales All Time: <code>{ $purchase_all_count }</code> - <code>{ $purchase_all_amount }{ currency_symbol_by_enum }</code>
    .edit-name-btn = ▪️ Edit Name
    .add-position-btn = ▪️ Add Position
    .copy-link-btn = ▪️ Copy Link
    .delete-btn = ▪️ Delete
    .another-lang-btn = 🇬🇧 Name in English
    .back-another-lang-btn = 🇷🇺 Back to Russian

delete-category = <b>❗️ Are you sure you want to delete the category and all its data?</b>
    .approve-btn = ✅ Yes, delete

categories-list = { $is_category ->
    [True]<b>🗃 Select a category to edit</b>
    *[other] <b>❌ No categories available</b>
}

delete = <b>🎁 Select the section you want to delete ❌</b>
    .delete-categories-btn = 🗃 Delete all categories
    .delete-positions-btn = 📁 Delete all positions
    .delete-items-btn = 🎁 Delete all items

approve-delete-categories = <b>❌ Are you sure you want to delete all categories, positions, and items?</b>
    🗃 Categories: <code>{ $categories_count }</code>
    📁 Positions: <code>{ $positions_count } pcs</code>
    🎁 Items: <code>{ $items_count } pcs</code>
    .approve-btn = ✅ Yes, delete
    .success-delete = <b>✅ You have successfully deleted all categories</b>
    🗃 Categories: <code>{ $categories_count }</code>
    📁 Positions: <code>{ $positions_count } pcs</code>
    🎁 Items: <code>{ $items_count } pcs</code>

approve-delete-positions = <b>❌ Are you sure you want to delete all positions and items?</b>
    📁 Positions: <code>{ $positions_count } pcs</code>
    🎁 Items: <code>{ $items_count } pcs</code>
    .approve-btn = ✅ Yes, delete
    .success-delete = <b>✅ You have successfully deleted all positions</b>
    📁 Positions: <code>{ $positions_count } pcs</code>
    🎁 Items: <code>{ $items_count } pcs</code>

approve-delete-items = ❌ Are you sure you want to delete all items?
    🎁 Items: <code>{ $items_count } pcs</code>
    .approve-btn = ✅ Yes, delete
    .success-delete = <b>✅ You have successfully deleted all items</b>
    🎁 Items: <code>{ $items_count } pcs</code>

select-category-add-position = { $is_category ->
    [True] <b>🗃 Select a category for the position ➕</b>
    *[other] <b>❌ No categories available to create a position</b>
    }

add-position = add position
    .ru-name = <b>📁 Enter the position name in Russian</b>
    .en-name = <b>📁 Enter the position name in English</b>
    .ru-price = <b>📁 Enter the position price in rubles</b>
    .en-price = <b>📁 Enter the position price in dollars</b>
    .ru-description = 📁 Enter a description for the position in Russian, or skip this step
        ❕ You can use HTML markup
    .en-description = 📁 Enter a description for the position in English
        ❕ You can use HTML markup

    .media = 📁 Send media for the position, or skip this step.
        ℹ️ Supported: <code>Video, Animation (GIF), Photo</code>

is-media = { $is_media ->
    [True] Available ✅
    *[other] Not Available ❌
}
is-description = { $is_description ->
    [True] { $description }
    *[other] Not Available ❌
}

edit-position = <b>📁 Editing Position</b>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Category: <code>{ $category_name }</code>
    ▪️ Position: <code>{ $position_name }</code>
    ▪️ Price: <code>{ $price }{ currency_symbol_by_enum}</code>
    ▪️ Number of Items: <code>{ $item_count }</code>
    ▪️ Media: <code>{ is-media }</code>
    ▪️ Creation Date: <code>{ $created_at }</code>
    ▪️ Description: <code>{ is-description }</code>

    💸 Sales per Day: <code>{ $purchase_day_count }</code> - <code>{ $purchase_day_amount }{ currency_symbol_by_enum }</code>
    💸 Sales per Week: <code>{ $purchase_week_count }</code> - <code>{ $purchase_week_amount }{ currency_symbol_by_enum }</code>
    💸 Sales per Month: <code>{ $purchase_month_count }</code> - <code>{ $purchase_month_amount }{ currency_symbol_by_enum }</code>
    💸 Sales All Time: <code>{ $purchase_all_count }</code> - <code>{ $purchase_all_amount }{ currency_symbol_by_enum }</code>
    .edit-name-btn = ▪️ Edit Name
    .edit-price-btn = ▪️ Edit Price
    .edit-media-btn = ▪️ Edit Media
    .edit-description-btn = ️▪️ Edit Description
    .add-items-btn = ▪️ Add Items
    .upload-items-btn = ▪️ Upload Items
    .clear-items-btn = ▪️ Clear Items
    .delete-item-btn = ▪️ Delete Item
    .copy-link-btn = ▪️ Copy Link
    .delete-btn = ▪️ Delete
    .another-lang-btn = 🇬🇧 Text in English
    .back-another-lang-btn = 🇷🇺 Back to Russian

select-category-edit-position = { $is_category ->
    [True] <b>🗃 Select a category to edit the position</b>
    *[other] <b>❌ No categories available for editing positions</b>
    }

positions-list = { $is_position ->
    [True] <b>📁 Select a position</b>
    *[other] <b>❌ No positions available</b>
    }
    .position-btn = 📁 {$name} | {$price}{currency_symbol_by_enum} | {$item_count} pcs

delete-position = <b>❗️ Are you sure you want to delete the position?</b>
    .approve-btn = ✅ Yes, delete

clear-items = <b>❗️ Are you sure you want to delete all items?</b>
    .approve-btn = ✅ Yes, delete

select-category-add-items = { $is_category ->
    [True] <b>🗃 Select a category for the items ➕</b>
    *[other] <b>❌ No categories available for creating a position</b>
    }

select-position-add-items = { $is_position ->
    [True] <b>📁 Select a position</b>
    *[other] <b>❌ No positions available</b>
    }
    .position-btn = 📁 {$name} | {$price}{currency_symbol_by_enum} | {$item_count} pcs

input-items = <b>🎁 Send item data</b>

    <pre>ℹ️ Items are separated by a blank line. Example:</pre>

    <code>Item data...</code>

    <code>Item data...</code>

    <code>Item data...</code>
    .success-input = <b>🎁 Item upload successfully completed ✅
        🎁 Items uploaded: <code>{ $count_items } pcs</code></b>
    .complete-download-btn = ✅ Complete Upload

items-list = <b>🎁 Select an item to delete</b>
    .items-list-empty = <b>❌ No items available</b>
    .details = <b>🎁 Item Deletion</b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Category: <code>{ $category_name }</code>
        ▪️ Position: <code>{ $position_name }</code>
        ▪️ Date Added: <code>{ $created_at }</code>
        ▪️ Item:
        <pre>{ $content }</pre>
    .delete-btn = ❌ Delete

delete-item = <b>❗️ Are you sure you want to delete the item?</b>
    .approve-btn = ✅ Yes, delete

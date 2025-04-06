product-management = <b>🎁 Редактирование товаров</b>
    .create-position-btn = 📁 Создать позицию ➕
    .edit-position-btn = 📁 Изменить позицию 🖍
    .create-category-btn = 🗃 Создать категорию ➕
    .edit-category-btn = 🗃 Изменить категорию 🖍
    .add-item-btn = 🎁 Добавить товары ➕
    .deleting-btn = ❌ Удаление

input-category-name = <b>🗃 Введите название для категории на русском</b>
    .en = <b>🗃 Введите название для категории на английском</b>

edit-category = <b>🗃️ Редактирование категории</b>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Категория: <code>{ $category_name }</code>
    ▪️ Кол-во позиций: <code>{ $position_count}</code>
    ▪️ Кол-во товаров: <code>{ $item_amount }шт</code>
    ▪️ Дата создания: <code>{ $created_at}</code>

    💸 Продаж за День: <code>{ $purchase_day_count}</code> - <code>{ $purchase_day_amount}{ currency_symbol_by_enum }</code>
    💸 Продаж за Неделю: <code>{ $purchase_week_count}</code> - <code>{ $purchase_week_amount}{ currency_symbol_by_enum }</code>
    💸 Продаж за Месяц: <code>{ $purchase_month_count}</code> - <code>{ $purchase_month_amount}{ currency_symbol_by_enum }</code>
    💸 Продаж за Всё время: <code>{ $purchase_all_count}</code> - <code>{ $purchase_all_amount}{ currency_symbol_by_enum }</code>
    .edit-name-btn = ▪️ Изм. Название
    .add-position-btn = ▪️ Добавить позицию
    .copy-link-btn = ▪️ Скопировать ссылку
    .delete-btn = ▪️ Удалить
    .another-lang-btn = 🇬🇧 Название на англ
    .back-another-lang-btn = 🇷🇺 Вернуть на русский

delete-category = <b>❗️ Вы действительно хотите удалить категорию и все её данные?</b>
    .approve-btn = ✅ Да, удалить

categories-list = { $is_category ->
    [True]<b>🗃 Выберите категорию для изменения</b>
    *[other] <b>❌ Категории отсуствуют</b>
}

delete = <b>🎁 Выберите раздел который хотите удалить ❌</b>
    .delete-categories-btn = 🗃 Удалить все категории
    .delete-positions-btn = 📁 Удалить все позиции
    .delete-items-btn = 🎁 Удалить все товары

approve-delete-categories = <b>❌ Вы действительно хотите удалить все категории, позиции и товары?</b>
    🗃 Категорий: <code>{ $categories_count}</code>
    📁 Позиций: <code>{ $positions_count}шт</code>
    🎁 Товаров: <code>{ $items_count}шт</code>
    .approve-btn = ✅ Да, удалить
    .success-delete = <b>✅ Вы успешно удалили все категории</b>
    🗃 Категорий: <code>{ $categories_count}</code>
    📁 Позиций: <code>{ $positions_count}шт</code>
    🎁 Товаров: <code>{ $items_count}шт</code>

approve-delete-positions = <b>❌ Вы действительно хотите удалить все позиции и товары?</b>
    📁 Позиций: <code>{ $positions_count}шт</code>
    🎁 Товаров: <code>{ $items_count}шт</code>
    .approve-btn = ✅ Да, удалить
    .success-delete = <b>✅ Вы успешно удалили все позиции</b>
    📁 Позиций: <code>{ $positions_count}шт</code>
    🎁 Товаров: <code>{ $items_count}шт</code>


approve-delete-items = ❌ Вы действительно хотите удалить все товары?
    🎁 Товаров: <code>{ $items_count}шт</code>
    .approve-btn = ✅ Да, удалить
    .success-delete = <b>✅ Вы успешно удалили все товары</b>
    🎁 Товаров: <code>{ $items_count}шт</code>

select-category-add-position = { $is_category ->
    [True] <b>🗃 Выберите категорию для позиции ➕</b>
    *[other] <b>❌ Отсутствуют категории для создания позиции</b>
    }

add-position = add position
    .ru-name = <b>📁 Введите название для позиции на русском</b>
    .en-name = <b>📁 Введите название для позиции на английском</b>
    .ru-price = <b>📁 Введите цену для позиции в рублях</b>
    .en-price = <b>📁 Введите цену для позиции в долларах</b>
    .ru-description = 📁 Введите описание для позиции на русском, либо пропустите этот шаг
        ❕ Вы можете использовать HTML разметку
    .en-description = 📁 Введите описание для позиции на английском
        ❕ Вы можете использовать HTML разметку

    .media = 📁 Отправьте медиа для позиции, либо пропустите этот шаг.
        ℹ️ Поддерживаются: <code>Видео, Анимациия(GIF), Фото</code>

is-media = { $is_media ->
    [True] Присутствует ✅
    *[other] Отсутствует ❌
}

is-description = { $is_description ->
    [True] { $description }
    *[other] Отсутствует ❌
}

edit-position = <b>📁 Редактирование позиции</b>
    ➖➖➖➖➖➖➖➖➖➖
    ▪️ Категория: <code>{ $category_name }</code>
    ▪️ Позиция: <code>{ $position_name }</code>
    ▪️ Стоимость: <code>{ $price }{ currency_symbol_by_enum}</code>
    ▪️ Количество товаров: <code>{ $item_count }</code>
    ▪️ Медиа: <code>{ is-media }</code>
    ▪️ Дата создания: <code>{ $created_at}</code>
    ▪️ Описание: <code>{ is-description }</code>

    💸 Продаж за День: <code>{ $purchase_day_count}</code> - <code>{ $purchase_day_amount}{ currency_symbol_by_enum }</code>
    💸 Продаж за Неделю: <code>{ $purchase_week_count}</code> - <code>{ $purchase_week_amount}{ currency_symbol_by_enum }</code>
    💸 Продаж за Месяц: <code>{ $purchase_month_count}</code> - <code>{ $purchase_month_amount}{ currency_symbol_by_enum }</code>
    💸 Продаж за Всё время: <code>{ $purchase_all_count}</code> - <code>{ $purchase_all_amount}{ currency_symbol_by_enum }</code>
    .edit-name-btn = ▪️ Изм. Название
    .edit-price-btn = ▪️ Изм. Цену
    .edit-media-btn = ▪️ Изм. Медиа
    .edit-description-btn = ️▪️Изм. Описание
    .add-items-btn = ▪️ Добавить Товары
    .upload-items-btn = ▪️ Выгрузить Товары
    .clear-items-btn = ▪️ Очистить Товары
    .delete-item-btn = ▪️ Удалить Товар
    .copy-link-btn = ▪️ Скопировать ссылку
    .delete-btn = ▪️ Удалить
    .another-lang-btn = 🇬🇧 Текста на англ
    .back-another-lang-btn = 🇷🇺 Вернуть на русский

select-category-edit-position = { $is_category ->
    [True] <b>🗃 Выберите категорию для изменения позиции</b>
    *[other] <b>❌ Отсутствуют категории для изменения позиции</b>
    }

positions-list = { $is_position ->
    [True] <b>📁 Выберите позицию</b>
    *[other] <b>❌ Позиции отсутствуют</b>
    }
    .position-btn = 📁 {$name} | {$price}{currency_symbol_by_enum} | {$item_count}шт

delete-position = <b>❗️ Вы действительно хотите удалить позицию?</b>
    .approve-btn = ✅ Да, удалить

clear-items = <b>❗️ Вы действительно хотите удалить все товары?</b>
    .approve-btn = ✅ Да, удалить

select-category-add-items = { $is_category ->
    [True] <b>🗃 Выберите категорию для товаров ➕</b>
    *[other] <b>❌ Отсутствуют категории для создания позиции</b>
    }

select-position-add-items = { $is_position ->
    [True] <b>📁 Выберите позицию</b>
    *[other] <b>❌ Позиции отсутствуют</b>
    }
    .position-btn = 📁 {$name} | {$price}{currency_symbol_by_enum} | {$item_count}шт


input-items = <b>🎁 Отправляйте данные товаров</b>

    <pre>ℹ️ Товары разделяются одной пустой строчкой. Пример:</pre>

    <code>Данные товара...</code>

    <code>Данные товара...</code>

    <code>Данные товара...</code>
    .success-input = <b>🎁 Загрузка товаров была успешно завершена ✅
        🎁 Загружено товаров: <code>{ $count_items }шт</code></b>
    .complete-download-btn = ✅ Завершить загрузку

items-list = <b>🎁 Выберите товар для удаления</b>
    .items-list-empty = <b>❌ Товары отсутствуют</b>
    .details = <b>🎁 Удаление товара</b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Категория: <code>{ $category_name }</code>
        ▪️ Позиция: <code>{ $position_name}</code>
        ▪️ Дата добавления: <code>{ $created_at }</code>
        ▪️ Товар:
        <pre>{ $content }</pre>
    .delete-btn = ❌ Удалить

delete-item = <b>❗️ Вы действительно хотите удалить товар?</b>
    .approve-btn = ✅ Да, удалить

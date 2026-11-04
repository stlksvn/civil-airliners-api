from fastapi import Header

TRANSLATIONS = {
    "ru": {
        "not_found": "Лайнер с таким ID не найден",
        "deleted": "Запись о лайнере с ID {record_id} удалена",
        "link_self": "получить",
        "link_create": "создать",
        "link_update": "модификация",
        "link_delete": "удаление",
    },
    "en": {
        "not_found": "Airliner with this ID was not found",
        "deleted": "Airliner record with ID {record_id} has been deleted",
        "link_self": "self",
        "link_create": "create",
        "link_update": "update",
        "link_delete": "delete",
    },
    "cs": {
        "not_found": "Dopravní letadlo s tímto ID nebylo nalezeno",
        "deleted": "Záznam pro linku s ID {record_id} byl smazán",
        "link_self": "získat",
        "link_create": "vytvořit",
        "link_update": "upravit",
        "link_delete": "выmazat",
    },
}


def get_locale(
    accept_language: str = Header(default="ru", alias="Accept-Language")
) -> dict:
    """
    Зависимость для определения языка. Парсит строку заголовка и сопоставляет её с доступными языками. Если совпадений нет — возвращает 'ru'.
    """
    if not accept_language:
        return TRANSLATIONS["ru"]

    primary_lang = accept_language.split(",")[0].split("-")[0].strip().lower()

    if primary_lang in TRANSLATIONS:
        return TRANSLATIONS[primary_lang]
    return TRANSLATIONS["ru"]

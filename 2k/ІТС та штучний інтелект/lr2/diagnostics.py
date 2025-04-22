from knowledge_base import knowledge

def diagnose_aircraft(fuel_level, fuel_consumption):
    if fuel_level < knowledge["aircraft"]["fuel_level_min"]:
        return "[Попередження!] Критичний рівень пального. Потрібно дозаправка.", "red"
    if fuel_consumption > knowledge["aircraft"]["fuel_consumption_max"]:
        return "[Попередження!] Витрати пального перевищують норму. Перевірте двигун та аеродинамічний стан літака.", "red"
    return "[Норма] Параметри у межах норми. Рекомендується оптимізація маршруту.", "green"
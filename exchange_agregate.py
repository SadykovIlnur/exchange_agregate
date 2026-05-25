from datetime import datetime
import json
import logging
from typing import Any, Dict, Optional

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('script_logs.log', encoding='utf-8'),]
)
logger = logging.getLogger(__name__)

url = "https://api.exchangerate-api.com/v4/latest/USD"


def get_exchange_rates_data(url: str) -> Optional[Dict[str, Any]]:
    """Получает данные из api."""
    logger.info("Начало запроса к API.")
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Получены данные из API.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return None


def get_filename() -> str:
    """Формирует имя файла из текущего времени."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"exchange_rates_backup_{timestamp}.json"


def backup_api_data(data: Dict[str, Any]) -> None:
    """Делает бекап данных из ответа в json формате."""
    filename = get_filename()
    logger.info("Начало создания бэкапа в файл.")
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        logger.info("Бэкап создан.")
    except Exception as e:
        logger.error(f"Ошибка при создании бэкапа: {e}")


def create_dataframe(data: Optional[Dict[str, Any]]) -> Optional[pd.DataFrame]:
    """Парсинг данных в pandas.DataFrame."""
    logger.info("Начало создания DataFrame.")
    if not data or 'rates' not in data:
        logger.warning("Данные не содержат ключ 'rates' или пустые")
        return None

    rates = data['rates']
    data_rows = []

    for currency, rate_to_USD in rates.items():
        data_rows.append({
            'Currency': currency,
            'Rate_to_USD': rate_to_USD
        })
    data_frame = pd.DataFrame(data_rows)
    logger.info("DataFrame создан.")
    return data_frame


def get_dataframe_name() -> str:
    """Формирует имя файла из текущего времени."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"exchange_rates_{timestamp}"


def save_to_csv_file(data_frame: pd.DataFrame) -> None:
    """Сохраняет DataFrame в CSV файл."""
    base_filename = get_dataframe_name()
    csv_filename = f"{base_filename}.csv"
    logger.info("Начало сохранения DataFrame в CSV файл")
    try:
        data_frame.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        logger.info("CSV файл сохранен.")
    except Exception as e:
        logger.error(f"Ошибка при сохранении CSV-файла: {e}")


def save_to_excel_file(data_frame: pd.DataFrame) -> None:
    """Сохраняет DataFrame в Excel файл."""
    base_filename = get_dataframe_name()
    excel_filename = f"{base_filename}.xlsx"
    logger.info("Начало сохранения DataFrame в Excel файл")
    try:
        data_frame.to_excel(
            excel_filename, index=False, sheet_name='Exchange Rates'
        )
        logger.info("Excel файл сохранен.")
    except Exception as e:
        logger.error(f"Ошибка при сохранении Excel-файла: {e}")


def main():
    logger.info("Запуск скрипта.")
    data = get_exchange_rates_data(url)
    if not data:
        logger.error("Не удалось получить данные.")
        return
    backup_api_data(data)
    data_frame = create_dataframe(data)
    if data_frame is None:
        logger.error("Не удалось создать DataFrame.")
        return
    save_to_csv_file(data_frame)
    save_to_excel_file(data_frame)
    logger.info("Скрипт завершил работу.")


if __name__ == "__main__":
    main()

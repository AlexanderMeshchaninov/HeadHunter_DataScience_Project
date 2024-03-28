import numpy as np

def get_education_categories(data):
    """Данная функция направлена на то, чтобы выделить из общих данных таблицы категории образования:
    - неоконченное высшее;
    - высшее;
    - среднее специальное;
    - среднее

    Args:
        data (pandas.DataFrame): набор данных

    Returns:
        str: строка-категория
    """
    try:
        parse_lst = data.split()
        
        if ('Неоконченное' in parse_lst[0]) or (parse_lst[1] in 'специальное'):
            return parse_lst[0].lower() + ' ' + parse_lst[1].lower()
        else:
            return parse_lst[0].lower()
    except IndexError as ex:
        pass
    
def get_job_experience(data):
    """Данная функция направлена на то, чтобы выделить из общих данных таблицы месяц и год

    Args:
        data (pandas.DataFrame): набор данных

    Returns:
        float: количество месяцев
    """
    if data is np.nan or data == 'Не указано': return np.nan
    
    years = 0
    months = 0
    exp = data.split(' ')[2:7]
    years_lst = ['год', 'года', 'лет']
    months_lst = ['месяца', 'месяцев', 'месяц']
 
    for indx, elem in enumerate(exp):
        if elem in years_lst:
            years = int(exp[indx-1])
        if elem in months_lst:
            months = int(exp[indx-1])
    
    return int(years*12 + months)
    
def get_city(data):
    """Данная функция направлена на то, чтобы выделить из общих данных следующие категории:
    - Москва;
    - Санкт-Петербург;
    - город-миллионник;
    - другие

    Args:
        data (pandas.DataFrame): набор данных
    
    Returns:
        str: строка-категория
    """
    
    city = data.split(' , ')[0]
    million_cities = [
        'Новосибирск', 'Екатеринбург','Нижний Новгород','Казань', 'Челябинск','Омск', 
        'Самара', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Воронеж','Волгоград'
        ]
    if ('Москва' in city) or ('Санкт-Петербург' in city):
        return city
    if city in million_cities:
        return 'город-миллионник'
    else:
        return 'другие'

def get_ready_to_relocate(data):
    """Данная функция направлена на то, чтобы определить готовность/не готовность к переезду

    Args:
        data (DataFrame): набор данных
    
    Returns:
        bool: True/False
    """
    if ('не готов к переезду' in data) or ('не готова к переезду' in data):
        return False
    elif 'хочу' in data:
        return True
    else:
        return True

def get_ready_to_bussiness_trip(data):
    
    """Данная функция направлена на то, чтобы определить готовность/не готовность к командировкам

    Args:
        data (pandas.DataFrame): набор данных
        
    Returns:
        bool: True/False
    """
    if ('командировка' in data):
        if ('не готов к командировкам' in data) or ('не готова к командировкам' in data):
            return False
        else:
            return True
    else:
        return False


    """Данная функция преобразовывает категориальные признаки в числовые (True/False):
    - гибкий график;
    - полный день;
    - сменный график; 
    - вахтовый метод; 
    - удаленная работа.

    Args:
        data (DataFrame): входные данные
        
    Returns:
        bool: True/False
    """
    # Таблица которую мы заполняем
    categories_map = [False, False, False, False, False]
    # Список категорий которые нужно преобразовать
    categories_list = ['гибкий график', 'полный день', 'сменный график', 'вахтовый метод', 'удаленная работа']
    
    for i, cat in enumerate(categories_list):
        if (cat) in data: categories_map[i] = True
    return categories_map

def convert_currency_to_iso(data):
    """Данная функция приводит строку с валютой к стандарту ISO

    Args:
        data (pandas.DataFrame): набор данных
        
    Returns:
        str: строка в формате ISO
    """    
    currency_dict = {
        'USD': 'USD', 'KZT': 'KZT',
        'грн': 'UAH', 'белруб': 'BYN',
        'EUR': 'EUR', 'KGS': 'KGS',
        'сум': 'UZS', 'AZN': 'AZN'
    }
    
    currency = data.split(' ')[1].replace('.', '')
    
    if currency == 'руб':
        return 'RUB'
    else:
        return currency_dict[currency]
    
def find_outliers_z_score(data, feature, left=3, right=3, log_scale=False):
    """
    Находит выбросы в данных, используя метод z-отклонений. 
    Классический метод модифицирован путем добавления:
    * возможности логарифмирования распредления
    * ручного управления количеством стандартных отклонений в обе стороны распределения
    Args:
        data (pandas.DataFrame): набор данных
        feature (str): имя признака, на основе которого происходит поиск выбросов
        left (float, optional): количество стандартных отклонений в левую сторону распределения. По умолчанию 1.5.
        right (float, optional): количество стандартных в правую сторону распределения. По умолчанию 1.5.
        log_scale (bool, optional): режим логарифмирования. По умолчанию False - логарифмирование не применяется.

    Returns:
        pandas.DataFrame: наблюдения, попавшие в разряд выбросов
        pandas.DataFrame: очищенные данные, из которых исключены выбросы
    """
    if log_scale: # логарифмический масштаб (если установить, то будет прибавлять единицу)
        x = np.log(data[feature] + 1)
    else:
        x = data[feature]
        
    mu = x.mean() # мю - среднее значение
    sigma = x.std() # сигма - стандартное отклонение
    bound_lower = mu - left * sigma # левая граница графика (нижняя граница) U - 3Q
    bound_upper = mu + right * sigma # правая граница графика (верхняя граница) U + 3Q
    outliers = data[(x < bound_lower) | (x > bound_upper)]
    cleaned = data[(x >= bound_lower) & (x <= bound_upper)]
    
    return outliers, cleaned
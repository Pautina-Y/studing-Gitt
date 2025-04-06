import numpy as np

def analyze_discrete_distribution(values, frequencies):
    """
    Анализирует дискретное распределение частот, вычисляя основные статистические характеристики.

    Параметры:
        values (np.array): Массив возможных значений случайной величины
        frequencies (np.array): Массив частот наблюдений соответствующих значений

    Возвращает:
        dict: Словарь с вычисленными характеристиками:
            - 'total_obs' - общее количество наблюдений
            - 'mean' - математическое ожидание
            - 'variance' - дисперсия
            - 'std_dev' - стандартное отклонение
    """
    # Проверка входных данных
    if len(values) != len(frequencies):
        raise ValueError("Длины массивов values и frequencies должны совпадать")
    if any(f < 0 for f in frequencies):
        raise ValueError("Частоты не могут быть отрицательными")

    total_obs = np.sum(frequencies)
    mean = np.sum(values * frequencies) / total_obs
    variance = np.sum((values - mean) ** 2 * frequencies) / total_obs
    std_dev = np.sqrt(variance)

    return {
        'total_obs': total_obs,
        'mean': mean,
        'variance': variance,
        'std_dev': std_dev
    }


def print_statistics(stats):
    """Выводит статистические характеристики в читаемом формате."""
    print("\nАнализ дискретного распределения:")
    print(f"{'Количество наблюдений (N)':<30}: {stats['total_obs']}")
    print(f"{'Среднее значение (μ)':<30}: {stats['mean']:.4f}")
    print(f"{'Дисперсия (σ²)':<30}: {stats['variance']:.4f}")
    print(f"{'Стандартное отклонение (σ)':<30}: {stats['std_dev']:.4f}")


values = np.array([0, 1, 2, 3, 4, 5, 6, 7])
frequencies = np.array([199, 169, 87, 31, 9, 3, 1, 1])
stats = analyze_discrete_distribution(values, frequencies)

print_statistics(stats)
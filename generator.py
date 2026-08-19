"""
Простой генератор словарей
Что умеет:
- Добавлять годы (2025, 2026...)
- Менять регистр (admin, Admin, ADMIN)
- Leet-замены
- Добавлять префиксы/суффиксы (admin123, !admin)
- Удалять дубликаты
"""

import itertools


def generate_wordlist(base_words, output_file):
    """
    Основная функция генерации
    base_words: список слов (например, ['admin', 'user'])
    output_file: куда сохранить результат
    """

    result = set()

    for word in base_words:
        word = word.strip().lower()
        if not word:
            continue

        result.add(word)

        # 2. варианты регистра
        result.add(word.upper())
        result.add(word.capitalize())
        result.add(word.title())

        # 3. добавляем годы
        for year in ['2024', '2025', '2026']:
            result.add(word + year)
            result.add(word + '_' + year)
            result.add(year + word)

        # 4. добавляем простые суффиксы
        for suffix in ['123', '!', '@', '#', '2024']:
            result.add(word + suffix)
            result.add(suffix + word)

        # 5. leet-замены
        if len(word) <= 8:
            leet_words = apply_leet(word)
            for lw in leet_words:
                result.add(lw)

        # 6. комбинации (слово + год + символ)
        for year in ['2024', '2025']:
            for symbol in ['!', '@']:
                result.add(word + year + symbol)
                result.add(word + symbol + year)

    with open(output_file, 'w', encoding='utf-8') as f:
        for word in sorted(result):
            f.write(word + '\n')

    return len(result)


def apply_leet(word):
    """Leet-замены"""
    leet_map = {
        'a': '@',
        'e': '3',
        'o': '0',
        's': '$',
        'i': '1'
    }

    results = []

    positions = []
    for i, char in enumerate(word):
        if char in leet_map:
            positions.append(i)

    # генерируем все комбинации замен
    if len(positions) > 10: # можно поменять до генерации необходимого числа комбинаций
        positions = positions[:10]

    # создаем все возможные комбинации
    for r in range(len(positions) + 1):
        for combo in itertools.combinations(positions, r):
            chars = list(word)
            for pos in combo:
                chars[pos] = leet_map[word[pos]]
            results.append(''.join(chars))

    return results


def main():
    print("-" * 35)
    print("ГЕНЕРАТОР СЛОВАРЕЙ v1.0")
    print("-" * 35)

    # 1: ввести слова вручную
    print("\n1: Ввести слова вручную")
    words_input = input("Введите слова через запятую (например: admin,user,root): ")
    base_words = [w.strip() for w in words_input.split(',') if w.strip()]

    # 2: загрузить из файла
    print("\n2: Загрузить из файла (каждое слово на новой строке)")
    file_path = input("Путь к файлу (оставьте пустым если не нужно): ")
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                base_words = [line.strip() for line in f if line.strip()]
            print(f"Загружено {len(base_words)} слов из файла")
        except FileNotFoundError:
            print("Файл не найден, используем введенные вручную слова")

    if not base_words:
        print("Нет слов для генерации!")
        return

    output_file = input("\nИмя выходного файла (по умолчанию wordlist.txt): ") or "wordlist.txt"

    print(f"\nГенерация словаря из {len(base_words)} слов...")
    count = generate_wordlist(base_words, output_file)

    print(f"\n[!] ГОТОВО!")
    print(f"   Сгенерировано слов: {count}")
    print(f"   Сохранено в файл: {output_file}")


if __name__ == "__main__":
    main()
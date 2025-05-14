import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

def download_webpage(url):
    """Загружает HTML по указанному URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return None

def extract_chapter1_text(html):
    """Извлекает текст первой главы 'Улисса' между <a id='chap01'> и <a id='chap02'>."""
    soup = BeautifulSoup(html, 'html.parser')

    start_anchor = soup.find(id="chap01")
    end_anchor = soup.find(id="chap02")

    if not start_anchor or not end_anchor:
        print("Не удалось найти границы первой главы.")
        return None

    chapter_parts = []
    current = start_anchor.find_next()

    while current and current != end_anchor:
        if current.name is None:
            text = current.strip()
            if text:
                chapter_parts.append(text)
        elif current.name in ['p', 'br', 'div', 'h1', 'h2', 'h3', 'span']:
            text = current.get_text(separator=' ', strip=True)
            if text:
                chapter_parts.append(text)
        current = current.find_next()

    full_text = ' '.join(chapter_parts)
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    return full_text

def count_word_frequencies(text):
    """Подсчитывает частоту слов в тексте."""
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def count_word_occurrences(text, word):
    """Возвращает количество вхождений заданного слова (без учёта регистра)."""
    return len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', text.lower()))

def find_word_contexts(text, target_word, left_len, right_len, cut_length=False, filename="contexts.txt"):
    """
    Находит контексты употребления слова.

    Args:
        text (str): Текст документа.
        target_word (str): Слово для поиска.
        left_len (int): Длина левого контекста.
        right_len (int): Длина правого контекста.
        cut_length (bool): Если True — искать контекст только в пределах одного предложения.
        filename (str): Имя файла для сохранения результатов.
    """
    target_word = target_word.lower()
    results = []

    if cut_length:

        sentences = re.split(r'(?<=[.!?])\s+', text)
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            indices = [i for i, w in enumerate(words) if w == target_word]
            for idx in indices:
                l_start = max(0, idx - left_len)
                r_end = min(len(words), idx + right_len + 1)
                context = ' '.join(words[l_start:r_end])
                results.append(context)
    else:

        words = re.findall(r'\b\w+\b', text.lower())
        indices = [i for i, word in enumerate(words) if word == target_word]
        for idx in indices:
            l_start = max(0, idx - left_len)
            r_end = min(len(words), idx + right_len + 1)
            context = ' '.join(words[l_start:r_end])
            results.append(context)


    with open(filename, "w", encoding="utf-8") as f:
        for context in results:
            print(context)
            f.write(context + "\n")

    print(f"\nНайдено {len(results)} вхождений слова '{target_word}'. Результаты записаны в '{filename}'.")

if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/4300/4300-h/4300-h.htm"
    html = download_webpage(url)

    if html:
        chapter1_text = extract_chapter1_text(html)
        if chapter1_text:
            print("Текст первой главы успешно извлечён.")


            freqs = count_word_frequencies(chapter1_text)
            print("\nТоп-20 слов по частоте:")
            for word, count in freqs.most_common(20):
                print(f"{word}: {count}")


            search_word = input("\nВведите слово для поиска контекста: ").strip()
            if search_word:

                occurrences = count_word_occurrences(chapter1_text, search_word)
                print(f"\nСлово '{search_word}' встречается в тексте {occurrences} раз(а).")

                left_len = int(input("Введите длину левого контекста (кол-во слов): "))
                right_len = int(input("Введите длину правого контекста (кол-во слов): "))
                cut_choice = input("Ограничить контекст одним предложением? (да/нет): ").strip().lower()
                cut_length = cut_choice in ['да', 'yes', 'y']


                filename = f"{search_word}_contexts.txt"


                find_word_contexts(chapter1_text, search_word, left_len, right_len, cut_length, filename)
            else:
                print("Слово не введено.")
        else:
            print("Не удалось извлечь текст первой главы.")
    else:
        print("Не удалось загрузить страницу.")
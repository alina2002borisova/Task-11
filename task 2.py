import math
from collections import Counter
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

class TFIDFProcessor:

    stopwords_ru = set(stopwords.words('russian'))
    stopwords_en = set(stopwords.words('english'))

    stopwords = stopwords_ru.union(stopwords_en)

    def __init__(self, documents):
        """
        Инициализация с документами.
        :param documents: список строк (документов), каждый содержит минимум 2 слова.
        """
        self.documents = [doc.strip().lower().split() for doc in documents]

    def get_tf(self, word, doc_number):
        """
        Возвращает Term Frequency (TF) для указанного слова в указанном документе.
        :param word: слово
        :param doc_number: номер документа (начиная с 0)
        :return: значение TF
        """
        words = self.documents[doc_number]
        total_words = len(words)
        word_count = words.count(word.lower())
        return word_count / total_words if total_words > 0 else 0

    def get_idf(self, word, doc_number=None):
        """
        Возвращает Inverse Document Frequency (IDF) для указанного слова.
        :param word: слово
        :param doc_number: не используется, но оставлено для совместимости
        :return: значение IDF
        """
        word = word.lower()
        num_docs_with_word = sum(1 for doc in self.documents if word in doc)
        total_docs = len(self.documents)
        return math.log(total_docs / (num_docs_with_word + 1)) + 1  # сглаживание

    def get_tf_idf(self, word, doc_number, ignore_stopwords=True):
        """
        Возвращает TF-IDF для указанного слова и документа.
        :param word: слово
        :param doc_number: номер документа (начиная с 0)
        :param ignore_stopwords: если True и слово — стопслово, возвращается 0.0
        :return: значение TF-IDF
        """
        word = word.lower()

        if ignore_stopwords and word in self.stopwords:
            return 0.0

        tf = self.get_tf(word, doc_number)
        idf = self.get_idf(word)
        return tf * idf

def main():
    print("Введите строки текста (минимум 2 слова в каждой). Введите пустую строку, чтобы закончить.")

    documents = []
    index = 1

    while True:
        line = input(f"Строка {index}: ").strip()
        if not line:
            if len(documents) < 1:
                print("Вы не ввели ни одной строки. Пожалуйста, введите хотя бы одну.")
            else:
                break
        elif len(line.split()) < 2:
            print("Каждая строка должна содержать минимум 2 слова. Повторите ввод.")
        else:
            documents.append(line)
            index += 1

    print("\nСоздаем обработчик TF-IDF...")
    processor = TFIDFProcessor(documents)

    print("\nДоступные документы:")
    for i, doc in enumerate(documents):
        print(f"Документ {i}: {doc}")

    try:
        doc_num = int(input("\nВведите номер документа (начиная с 0): "))
        if not (0 <= doc_num < len(documents)):
            print("Неверный номер документа.")
            return

        word = input("Введите слово для анализа: ").strip().lower()

        print("\nИгнорировать стопслова?")
        print("1. Да")
        print("2. Нет")
        choice = input("Выберите 1 или 2: ").strip()

        while choice not in ('1', '2'):
            print("Ошибка ввода. Введите 1 или 2.")
            choice = input("Выберите 1 или 2: ").strip()

        ignore_sw = (choice == '1')

        tf = processor.get_tf(word, doc_num)
        idf = processor.get_idf(word)
        tf_idf = processor.get_tf_idf(word, doc_num, ignore_stopwords=ignore_sw)

        print(f"\nРезультаты для слова '{word}' в документе {doc_num}:")
        print(f"TF: {tf:.4f}")
        print(f"IDF: {idf:.4f}")
        print(f"TF-IDF: {tf_idf:.4f}")

    except ValueError:
        print("Ошибка ввода. Номер документа должен быть целым числом.")

if __name__ == "__main__":
    main()
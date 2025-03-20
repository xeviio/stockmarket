Opis kodu:
Analiza Kapitalizacji Rynkowej i Dynamiki Cen Akcji
Ten kod w Pythonie pobiera dane o największych firmach giełdowych za pomocą Yahoo Finance (yfinance), przetwarza je równocześnie przy użyciu wielowątkowości (ThreadPoolExecutor), a następnie wyświetla w interfejsie Tkinter. Program pokazuje 10 firm o największej kapitalizacji rynkowej oraz 10 firm o największym wzroście ceny akcji w ostatnim tygodniu.

📌 Jak działa kod?
Lista spółek

Zdefiniowana jest lista 48 symboli giełdowych firm takich jak Apple, Microsoft, Amazon itp.
Pobieranie danych giełdowych

Funkcja fetch_data(symbol) pobiera informacje dla danej firmy:
Kapitalizacja rynkowa
Zmiana procentowa ceny akcji w ostatnim tygodniu
Pełna nazwa firmy
Jeśli brakuje danych, firma jest pomijana.
Równoczesne pobieranie danych

Program używa ThreadPoolExecutor, aby przyspieszyć pobieranie danych poprzez wielowątkowość.
Sortowanie firm

Top 10 największych firm według kapitalizacji rynkowej
Top 10 najszybciej rosnących firm według procentowej zmiany ceny akcji
Wyświetlenie wyników w GUI

Tkinter wyświetla wyniki w tabeli Treeview, podzielonej na dwie sekcje:
Największe firmy (pod względem kapitalizacji)
Najszybciej rosnące firmy (pod względem wzrostu ceny akcji)
Emoji 🔥 dla lidera wzrostu

Firma z największym tygodniowym wzrostem otrzymuje 🔥 jako wizualne wyróżnienie.
🛠 Zastosowane technologie
✅ yfinance – pobieranie danych giełdowych
✅ Tkinter – GUI do wyświetlania wyników
✅ ThreadPoolExecutor – wielowątkowe pobieranie danych
✅ Sortowanie i filtrowanie danych – Pythonic sposób na analizę

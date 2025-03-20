import yfinance as yf
import tkinter as tk
from tkinter import ttk
import concurrent.futures

# Lista symboli firm do pobrania (do obliczenia kapitalizacji i zmian procentowych)
companies = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "BRK.B", "NVDA", "JPM", "JNJ", 
    "V", "WMT", "XOM", "PG", "MA", "UNH", "HD", "BAC", "PFE", "KO", "DIS", 
    "CSCO", "PEP", "INTC", "MRK", "CMCSA", "ORCL", "NKE", "T", "ABT", "LLY", 
    "MCD", "CVX", "ADBE", "NFLX", "CRM", "PM", "VZ", "WFC", "BMY", "COST", 
    "TXN", "UPS", "NEE", "LIN", "UNP", "QCOM", "MDT"
]

# Funkcja do pobierania danych dla jednej firmy
def fetch_data(symbol):
    data = {"symbol": symbol, "market_cap": 0, "change_percent": 0, "name": "", "valid": False}
    try:
        stock = yf.Ticker(symbol)
        
        # Pobieranie kapitalizacji rynkowej
        info = stock.info
        market_cap = info.get("marketCap", 0)
        if market_cap == 0:
            return data  # Pomiń, jeśli brak kapitalizacji rynkowej
        
        # Pobieranie danych historycznych
        history = stock.history(period="7d")
        if len(history) < 2:
            return data  # Pomiń, jeśli brakuje danych historycznych
        
        # Zamknięcie z ostatniego dnia i sprzed tygodnia
        last_close = history["Close"].iloc[-1]
        prev_close = history["Close"].iloc[0]

        # Oblicz procentową zmianę ceny
        change_percent = ((last_close - prev_close) / prev_close) * 100
        
        # Pobieranie nazwy firmy
        name = info.get("longName", symbol)
        
        data["market_cap"] = market_cap
        data["change_percent"] = change_percent
        data["name"] = name
        data["valid"] = True  # Oznaczenie, że dane są prawidłowe

    except Exception as e:
        print(f"Błąd pobierania danych dla {symbol}: {e}")
    
    return data

# Tworzenie okna GUI
window = tk.Tk()
window.title("Top 10 Największych Firm i Najszybciej Rosnących")

# Tworzenie widżetu Treeview (tabela)
tree = ttk.Treeview(window, columns=("Firma", "Kapitalizacja rynkowa (Bln USD)", "Zmiana (%)"), show="headings")
tree.heading("Firma", text="Firma")
tree.heading("Kapitalizacja rynkowa (Bln USD)", text="Kapitalizacja rynkowa (Bln USD)")
tree.heading("Zmiana (%)", text="Zmiana (%)")
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Równoczesne pobieranie danych
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(fetch_data, companies))

# Filtrujemy i sortujemy dane
valid_results = [result for result in results if result["valid"]]  # Tylko prawidłowe dane

market_cap = {result["symbol"]: result["market_cap"] for result in valid_results}
weekly_changes = {result["symbol"]: result["change_percent"] for result in valid_results}

# Sortowanie firm według kapitalizacji rynkowej (top 10)
sorted_market_cap = sorted(market_cap.items(), key=lambda x: x[1], reverse=True)[:10]

# Sortowanie firm według procentowej zmiany ceny (top 10 najszybciej rosnących)
sorted_changes = sorted(weekly_changes.items(), key=lambda x: x[1], reverse=True)[:10]

# Dodawanie danych do tabeli
tree.insert("", "end", values=("Top 10 Największych Firm na Podstawie Kapitalizacji Rynkowej", "", ""))
for symbol, cap in sorted_market_cap:
    name = next(result["name"] for result in valid_results if result["symbol"] == symbol)
    tree.insert("", "end", values=(name, f"{cap/1e9:.2f}", ""))

tree.insert("", "end", values=("Top 10 Najszybciej Rosnących Firm w Ciągu Ostatniego Tygodnia", "", ""))
for symbol, change_percent in sorted_changes:
    name = next(result["name"] for result in valid_results if result["symbol"] == symbol)
    fire_emoji = "🔥" if change_percent == sorted_changes[0][1] else ""
    tree.insert("", "end", values=(name, "", f"{change_percent:+.2f}% {fire_emoji}"))

# Uruchomienie aplikacji GUI
window.mainloop()

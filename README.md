
# Kaktus Newsletter Scraper a Email Notifier

Tento skript seškrábe nejnovější příspěvky z webové stránky Kaktus Newsletter a v případě nalezení nového příspěvku odešle e-mailové oznámení. Zabraňuje odesílání duplicitních e-mailů během hodiny.

Předpoklady:

- Python 3.x
- Potřebné balíčky lze nainstalovat pomocí: V případě potřeby můžete použít následující nástroje: `pip install requests beautifulsoup4`

## Konfigurace
```
1. Nahraďte zástupné znaky v sekci konfigurace e-mailu skutečnými přihlašovacími údaji k e-mailu Seznam.cz:
   
   ```python
   sender_email = "your_sender_email@seznam.cz"
   receiver_email = "your_receiver_email@example.com"
   smtp_server = "smtp.seznam.cz"
   smtp_port = 465
   smtp_username = "your_sender_email@seznam.cz"
   smtp_password = "your_email_password"
   ```

2. Upravte proměnnou URL (`url`) tak, aby odpovídala adrese URL stránky newsletteru, kterou chcete sledovat.

## Jak to funguje

1. Skript vyškrábe nejnovější příspěvek ze zadané adresy URL a extrahuje z něj název, obsah, datum a čas.

2. Zkontroluje, zda byl během poslední hodiny odeslán e-mail a zda je obsah posledního příspěvku stejný jako obsah posledního odeslaného e-mailu.

3. Pokud uplynula hodina a obsah příspěvku se liší, skript odešle zadanému příjemci e-mail s podrobnostmi o příspěvku. Zároveň uloží časové razítko a obsah e-mailu do souboru, aby se zabránilo duplicitním e-mailům.

4. Skript běží v nekonečné smyčce a kontroluje nové příspěvky každých 5 minut (nastavitelné).

## Použití

1. Nainstalujte požadované balíčky pomocí následujícího příkazu:
   
   ```
   pip install requests beautifulsoup4
   ```

2. Nahraďte zástupné znaky konfigurace e-mailu svými přihlašovacími údaji k e-mailu Seznam.cz.

3. Upravte proměnnou URL (`url`) tak, aby odpovídala URL adrese newsletteru, kterou chcete sledovat.

4. Spusťte skript pomocí příkazu:
   
   ```
   python main.py
   ```

5. Skript bude každých 5 minut kontrolovat nové příspěvky a podle potřeby odesílat e-mailová oznámení.

## Poznámky

- Udržujte své e-mailové přihlašovací údaje v bezpečí. Pro lepší zabezpečení se doporučuje používat hesla specifická pro danou aplikaci.
- Skript ukládá informace o e-mailu do textového souboru s názvem `poslední_email_info.txt`. Odstranění tohoto souboru bude předpokládat, že předtím nebyly odeslány žádné e-maily.
- Pokud narazíte na problémy nebo chyby, zkontrolujte chybová hlášení a ověřte konfiguraci e-mailu.

---

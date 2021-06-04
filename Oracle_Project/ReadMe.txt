Plik ExportDBFromSQLDeveloper jest exportem całej bazy danych przy użyciu opcji export database z Oracle SQL Developera
w stanie w którym skończyłem pracę nad projektem. Pozostałe pliki są plikami użytymi do stworzenia bazy danych w stanie
początkowym. W pliku OtherQuerry znajdują się zapytania, które nie znalazły swojego zastosowania w ramach projektu, ale
zostały utworzone w celu przedstawienia działania określonych w wymaganiach projektu klauzul. 

W pliku Oracle_Procedures znajdują się kody źródłowe procedur składowanych stworzonych w ramach projektu, niestety nie
udało mi się znaleźć sposobu na ich podzielenie tak jak w przypadku MySQL poprzez użycie zmiany delimitera. Z tego
powodu konieczne jest uruchamianie każdej części skryptu odpowiedzialnej za stworzenie jednej procedury osobno.

W celu uruchomienia cruda konieczne jest zbudowanie projektu w Pythonie 3.8 /3.9 dodanie plików .py i uzupełnenie
koniecznych informacji w pliku config.py
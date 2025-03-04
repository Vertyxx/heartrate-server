# heartrate-server

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Vertyxx/heartrate-server.git
    ```

2. Navigate into the project directory:
    ```bash
    cd heartrate-server
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    .venv\Scripts\activate  # Windows
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the application:
    ```bash
    python run.py
    ```

The application will be available at http://127.0.0.1:5000/.

# Nastavení a spuštění MariaDB s phpMyAdmin v Dockeru

## Požadavky
- Docker
- Docker Compose

## Spuštění databáze
1. Ujisti se, že jsi ve složce s `docker-compose.yml`.
2. Spusť databázi:
   ```sh
   docker-compose up -d
   ```
3. Otevři phpMyAdmin v prohlížeči:
   ```
   http://localhost:8080
   ```
4. Přihlašovací údaje:
   - **Server:** `mariadb`
   - **Uživatel:** `uzivatel` (nebo `root` pro administrátora)
   - **Heslo:** `heslo` (nebo `root` pro root)

## Zastavení databáze
```sh
docker-compose down
```

## Smazání databázových dat (reset)
```sh
docker volume rm docker_mariadb_data
```



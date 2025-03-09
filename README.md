# heartrate-server

# Nastavení a spuštění MariaDB s phpMyAdmin v Dockeru

## Požadavky
- Docker
- Docker Compose

## Spuštění databáze + flask
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

5. Flask běží na:
   ```
   http://localhost:5001
   ```

## Zastavení databáze
```sh
docker-compose down
```

## Smazání databázových dat (reset)
```sh
docker volume rm docker_mariadb_data
```



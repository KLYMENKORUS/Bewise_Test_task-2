<h1>Тестовое задание №2 Bewise.ai</h1>
  <h2>Задание</h2>
  <h3>Необходимо реализовать веб-сервис, выполняющий следующие функции:</h3>
  <p>Создание пользователя<p>
  <ul>
    <li>для каждого пользователя - сохранение аудиозаписи в формате wav</li>
    <li>преобразование её в формат mp3 и запись в базу данных</li>
    <li>предоставление ссылки для скачивания аудиозаписи></li>
  </ul>

<p>Детализация задачи:<p>

<h4>С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL).
Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД,
а также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера
(то есть - использовать volume-ы для хранения файлов СУБД на хост-машине.</h4>
<p>Реализовать веб-сервис со следующими REST методами:<p>
<ol>
  <li>Создание пользователя, POST:</li>
    <ul>
      <li>Принимает на вход запросы с именем пользователя;</li>
      <li>Создаёт в базе данных пользователя заданным именем, так же генерирует уникальный идентификатор пользователя и UUID токен доступа (в виде строки) для данного пользователя;</li>
      <li>Возвращает сгенерированные идентификатор пользователя и токен.</li>
    </ul>
  <li>Добавление аудиозаписи, POST:</li>
    <ul>
      <li>Принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в формате wav;</li>
      <li>Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе данных;</li>
      <li>Возвращает URL для скачивания записи вида http://host:port/record?id=id_записи&user=id_пользователя.</li>
    </ul>
  <li>Доступ к аудиозаписи, GET:</li>
    <ul>
      <li>Предоставляет возможность скачать аудиозапись по ссылке</li>
    </ul>
</ol>

<p>Для всех сервисов метода должна быть предусмотрена предусмотрена обработка различных ошибок, возникающих при выполнении запроса, с возвращением соответствующего HTTP статуса.
Модель данных (таблицы, поля) для каждого из заданий можно выбрать по своему усмотрению.
В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисами из пп. 2. и 3., их настройке и запуску. А также пример запросов к методам сервиса.
Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAlchemy,  пользоваться аннотацией типов.</p>
  <h2>Технологии</h2>
  <div>
    <img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white&color=9cf" alt="Postgresql Badge"/>
    <img src="https://img.shields.io/badge/FastAPI-blue?style=for-the-badge&logo=fastapi&logoColor=white&color=brightgreen" alt="FastAPI Badge"/>
    <img src="https://img.shields.io/badge/Postgres-green?style=for-the-badge&logo=postgresql&logoColor=white&color=informational" alt="Postgresql Badge"/>
    <img src="https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker&logoColor=white&color=blue" alt="Docker Badge"/>
  </div>
  <h2>Запуск проекта</h2>
  <ul>
  <li>Скачать и установить <a href='https://docs.docker.com/get-docker/'>Docker</a></li>
  <li>Клонировать репозиторий: <code> git clone https://github.com/KLYMENKORUS/Bewise_Test_task-2.git</code></li>
  <li>В корне проекта создать файл .env и заполнить его по примеру .env.example</li>
  <li>Выполнить команду <code>docker-compose up -d --build</code> в корне проекта</li>
  </ul>

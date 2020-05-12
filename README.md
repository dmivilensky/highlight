![alt text][logo]

[logo]: https://github.com/dmivilensky/highlight/blob/master/logo.png

## Установка

**_Скачайте:_**
- [python 3](https://www.python.org/downloads/release/python-382/)
- [mongodb](https://docs.mongodb.com/manual/installation/)
- [apache](https://httpd.apache.org/download.cgi)
- [git](https://git-scm.com/downloads)
- [mod_wsgi для apache](https://pypi.org/project/mod-wsgi/#installation-into-apache)

**_Напишите в консоле:_**
```shell script
git clone "https://github.com/dmivilensky/highlight.git"
```

**_Настройте:_**
- [Выполните инструкции из туториала по созданию виртуального хоста](https://medium.com/@JohnFoderaro/how-to-set-up-apache-in-macos-sierra-10-12-bca5a5dfffba#5f65)
- В качестве виртуального хоста укажите:
    ```editorconfig
  <VirtualHost *:80>
      ServerAdmin webmaster@[имя сервера]
      ServerName # имя сервера
      ServerAlias # имя сервера без www
      DirectoryIndex index.php index.html # или другой файл, который является стартовой страницей
      DocumentRoot path/to/folder/highlight
      LogLevel warn
      ErrorLog /var/log/httpd/highlight.spb.ru_error.log
      CustomLog /var/log/httpd/highlight.spb.ru_access.log combined
        
      ProxyPass "/api" "http://localhost:9000/"
      ProxyPassReverse "/api" "http://localhost:9000/"
        
      <Directory path/to/folder/highlight>
          AllowOverride All
          Require all granted
      </Directory>
    
  </VirtualHost>
    ```
- Убедитесь, что линия load proxy_module в httpd.conf: LoadModule proxy_module modules/mod_proxy.so есть и разкомментарена (нет # в начале)
- Убедитесь, что линия load proxy_http_module в httpd.conf: LoadModule proxy_http_module modules/mod_proxy_http.so есть и разкомментарена (нет # в начале)

**_Измените:_**
- shell_scripts/start_django параметр USER на юзера под которым запускается apache
    ```shell script
  ps -Aj | grep httpd # Узнать юзера, если апач запущен (юзер это 1 колонка)
    ```
- shell_scripts/start_server параметр apachectl на имя apache (обычно apache2)

## Запуск

```shell script
shell_scripts/setup           # Сетап
shell_scripts/start_server    # Запуск сервера
```

## Обслуживание

```shell script
shell_scripts/stфке_django     # Запуск бэкграунда сервера
shell_scripts/restart_django   # Перезапуск бэкграунда сервера
shell_scripts/stop_django      # Остановка бэкграунда сервера
```
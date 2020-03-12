# Лог изменений / статус
+ Добавлены тесты, актуальная версия в master-ветке.
+ Оформлено 2 issues: https://github.com/ilaure/qa_task/issues?q=is%3Aissue+is%3Aclosed
+ Внесены исправление в app.py, актуальная версия в master-ветке.

# Тестовое задание
Требуется написать тесты на веб приложение, залить в свой репозиторий и отправить нам ссылку.
<br>Если будут обнаружены ошибки - написать по ним баг репорты

Плюсом будет, если кроме тестов будут также исправления.


# Описание приложения
В API на Flask реализовано два хэндлера:

`GET: /minutes/<count>` - Принимает количество минут. 
Возвращает предложение "Вы ввели: <count> минут/минуты/минуту", в зависимости от числа.

Пример: 
```
curl -X GET http://0.0.0.0:5000/minutes/5

Вы ввели: 5 минут
```  

`POST: /check_ident` - Проверка контрольного числа идентификатора.
<br>Идентификатор имеет вид "XXXXX-XXXXX Y", где XXXXX-XXXXX - номер, а Y - контрольное число.
<br>Контрольное число идентификатора рассчитывается следующим образом:
- нумерация позиций в номере начинается с конца;
- каждая цифра номера возводится в квадрат и делится по модулю на номер своей
позиции;
- полученные значения суммируются;
- если сумма больше 10, то сумма делится на 10 до тех пор, пока остаток от деления не
будет меньше 10, контрольное число будет равно остатку от деления;
- если сумма меньше 10, то контрольное число равно самой сумме.

Хэндлер принимает данные в JSON вида: `{"ident": "00000-00000 0"}`.
<br>Возвращает `{"result": true}` или `{"result": false}`
Пример: 
``` bash
curl -X POST http://0.0.0.0:5000/check_ident \
                          -H 'Accept: */*' \
                          -H 'Content-Type: application/json' \
                          -H 'Host: 0.0.0.0:5000' \
                          -d '{"ident": "00000-00000 0"}'

{"result":true}
```  



## Запуск приложения

Запустить можно несколькими способами

1) Из Makefile (требуется Docker):

    ```shell script
    > make build
    
    > make run
    
    ```

2) Из Docker:

    ```shell script
    > docker build -t flask-sample-one:latest .
    
    > docker run -d --name flask-proj -p 5000:5000 flask-sample-one
    
    ```


# Sound_recorder

Назначение: запись аудиопотока с Input устройств компьютера и сохранение их в аудиофайл формата MP3.
Это позволит при необходимости записывать разговоры в скайпе и прочее подобное.

### Использование
Для использования кода потребуются установленные модули:
1) pyaudio (для сохранения временного файла в wav используем wave);
2) pydub (для конфертации аудиофайла в MP3 посредством набора библиотек ffmpeg(ставится отдельно));
3) pyQt (интерфейс на нем);

Внимание: Также потребуется в списке аудиоустройств включить стереомикшер (https://sovetclub.ru/kak-vklyuchit-miksher)

Для запуска кода нужно запустить выполнение файла main_window.py.
Далее в открывшемся окне выбираем устройства с которых будет захватываться аудиопоток. Важно выбирать только устройства ввода.
Оптимальным выбором в первом боксе будет микрофон (любой, хоть на камере), а во-втором - стереомикшер.
В третьем боксе решаем нужен звук только с микрофона или же звук с двух выбранных устройств.
После нажатия кнопки "Запись" становится активной кнопка "Стоп", а все остальные элементы блокируются. Также запускается необходимое количество потоков и начинается их сохранение.
При нажатии кнопки "Стоп" разблокируется все, что было заблокировано, при этом сама кнопка "Стоп" блокируется. 
В это время идет сохранение звука в .wav файл и его последующая конвертация в mp3. При выборе двух потоков эти два файла объединяются в один звуковой поток
По итогу создается три файла (два, если выбрали запись только с одного устройства) в корневом катологе утилиты. 
Итоговый MP3 именуется датой и временем запуска записи для облегчения поиска. Остальные файлы оставлены для удобства определения нужного устройства в списке.

Важно: не прописано ограничение на максимальную продолжительность записи.

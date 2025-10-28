# Инструкция по добавлению звуков

## Расположение звуковых файлов

Все звуковые файлы должны быть размещены в папке:
```
/app/frontend/public/sounds/
```

## Необходимые звуковые файлы

Вам нужно добавить 4 звуковых файла с следующими именами:

1. **keypress.mp3** - Звук при нажатии любой клавиши
2. **correct.mp3** - Звук при правильном вводе символа
3. **incorrect.mp3** - Звук при неправильном вводе символа
4. **complete.mp3** - Звук при завершении теста

## Формат файлов

- Формат: MP3 (можно также использовать WAV, OGG)
- Рекомендуемая длительность: 0.1-0.5 секунд для keypress/correct/incorrect, 1-3 секунды для complete
- Громкость будет автоматически установлена на 50%

## Примеры источников звуков

### Бесплатные библиотеки звуков:
1. **Freesound.org** - https://freesound.org/
2. **Zapsplat** - https://www.zapsplat.com/
3. **Mixkit** - https://mixkit.co/free-sound-effects/

### Рекомендуемые поисковые запросы:
- Для keypress: "keyboard click", "key press", "mechanical keyboard"
- Для correct: "success beep", "positive notification", "correct"
- Для incorrect: "error beep", "wrong", "negative notification"
- Для complete: "success", "achievement", "complete"

## Как добавить файлы

### Вариант 1: Через терминал
```bash
# Скопируйте ваши файлы в папку
cp /path/to/your/keypress.mp3 /app/frontend/public/sounds/
cp /path/to/your/correct.mp3 /app/frontend/public/sounds/
cp /path/to/your/incorrect.mp3 /app/frontend/public/sounds/
cp /path/to/your/complete.mp3 /app/frontend/public/sounds/
```

### Вариант 2: Создать свои звуки
Вы можете создать простые beep-звуки с помощью онлайн-генераторов:
- https://onlinetonegenerator.com/
- https://www.szynalski.com/tone-generator/

## После добавления файлов

После того, как вы добавите звуковые файлы:
1. Обновите страницу в браузере (F5)
2. Звуки начнут работать автоматически
3. Вы можете включить/выключить звуки кнопкой в футере

## Текущее состояние

Сейчас в приложении показываются предупреждения о том, что звуковые файлы не найдены.
Это нормально - просто добавьте файлы как описано выше, и предупреждения исчезнут.

## Настройка громкости

Если нужно изменить громкость звуков, отредактируйте файл:
```
/app/frontend/src/shared/composables/useSound.ts
```

Найдите строку:
```typescript
clone.volume = 0.5  // 50% громкости
```

Измените значение от 0.0 (тишина) до 1.0 (максимум)

## Изменение путей к звукам

Если вы хотите использовать другие имена файлов или добавить больше звуков,
отредактируйте объект SOUND_URLS в файле:
```
/app/frontend/src/shared/composables/useSound.ts
```

```typescript
export const SOUND_URLS = {
  keypress: '/sounds/keypress.mp3',     // Измените здесь
  correct: '/sounds/correct.mp3',       // Измените здесь
  incorrect: '/sounds/incorrect.mp3',   // Измените здесь
  complete: '/sounds/complete.mp3',     // Измените здесь
}
```

## Устранение проблем

### Звуки не воспроизводятся
1. Проверьте, что файлы находятся в `/app/frontend/public/sounds/`
2. Проверьте имена файлов (они должны совпадать точно)
3. Убедитесь, что звук включен в приложении (кнопка в футере)
4. Обновите страницу (F5)

### Звуки воспроизводятся слишком громко/тихо
Измените значение volume в useSound.ts как описано выше

### Хочу использовать другой формат (не MP3)
Поддерживаются: MP3, WAV, OGG, WEBM
Просто измените расширение в SOUND_URLS

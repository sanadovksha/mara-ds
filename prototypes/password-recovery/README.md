# Password recovery prototype

Интерактивный прототип восстановления пароля, собранный на основе токенов и component contracts из `mara-ds`.

## Flow

1. **E-mail** — ввод адреса, локальная проверка формата.
2. **Проверьте почту** — нейтральное подтверждение без раскрытия существования аккаунта; повторная отправка.
3. **Новый пароль** — новый пароль + подтверждение, видимые требования, show/hide password.
4. **Готово** — подтверждение смены и возврат к обычному входу.

В правом нижнем углу есть prototype navigation для быстрого просмотра всех состояний.

## Mara DS mapping

- `components/text-field` — Empty / Active / Filled / Error states.
- `components/button` — 44 / M, Primary / Secondary, Normal / Disabled states.
- `components/password-create-block` — password requirements, success/error/active states, show password.
- `components/link` — back/support/resend actions.
- Light COM palette from `tokens/core/light.json`.
- Brand/accent colors from `tokens/semantic/accents.json`.

## UX/security decisions

- После отправки используется одинаковое сообщение независимо от того, зарегистрирован e-mail или нет. Это снижает риск user-enumeration.
- Reset должен выполняться через одноразовый, ограниченный по времени token в side-channel (обычно e-mail).
- Новый пароль вводится дважды.
- После успешной смены пользователь возвращается к обычному экрану входа; автоматический login не предполагается.
- Поля используют `autocomplete="email"` и `autocomplete="new-password"`, чтобы не мешать браузерам и password managers.
- Повторная отправка визуально блокируется после клика; production-реализация должна дополнительно иметь server-side rate limiting.

## Prototype-only notes

- Кнопка `Открыть ссылку из письма` существует только для демонстрации перехода между состояниями. В production пользователь приходит на экран нового пароля по ссылке из письма.
- Политика пароля в прототипе (`8+`, буква, цифра) демонстрационная. В production следует подключить актуальную password policy продукта и тот же набор правил, что используется при регистрации/смене пароля.
- Логотип в prototype — упрощённый CSS placeholder; продуктовый header/logo следует подключить из реального приложения.

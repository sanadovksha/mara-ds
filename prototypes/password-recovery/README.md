# Password recovery prototype

Интерактивный прототип восстановления пароля, собранный по опубликованным данным `mara-ds` для режима **Light • COM**.

## Flow

1. **E-mail** — ввод адреса и состояние ошибки.
2. **Проверьте почту** — нейтральное подтверждение без раскрытия существования аккаунта и повторная отправка.
3. **Новый пароль** — новый пароль, подтверждение, show/hide и состояния требований.
4. **Готово** — подтверждение смены и возврат к обычному входу.

Внизу прототипа есть navigation для быстрого переключения между состояниями.

## Точное соответствие Mara DS

### Components

- `components/text-field/contract.json`
  - Size: `medium`, `large`, `xlarge`;
  - State: `Empty`, `Empty Hover`, `Active`, `Filled`, `Filled Hover`, `Error`, `Error Filled`, `Disable`.
- `components/button/contract.json`
  - размер CTA: `44 / M`;
  - State: `Normal`, `Disabled`;
  - Style: Brand/Primary-equivalent solid action in Light COM.
- `components/password-create-block/contract.json`
  - используются состояния требований к паролю и show/hide password;
  - в DS подтверждены `State`, `Show Password`, `Show Requirement`.
- `components/link/contract.json`
  - back, support и resend actions.

### Typography

Все основные текстовые стили заменены на значения из `styles/file-snapshot/typography-*.json`:

- заголовок: `Static/Heading H2 24px/Semibold` — Inter Semi Bold, 24/32, letter-spacing -0.5px;
- основной текст: `Static/Large Paragraph 15px/Regular` — Inter Regular, 15/24;
- label: `Static/Text Small 14px/Semibold` — Inter Semi Bold, 14/18;
- CTA: `Static/Text Large 16px/Semibold` — Inter Semi Bold, 16/20;
- helper/error: `Static/Caption Middle 12px/Regular` — Inter Regular, 12/16;
- meta text: `Static/Caption Large 13px/Regular` — Inter Regular, 13/16.

### Semantic tokens — Light • COM

Из `tokens/semantic/foundation.json`:

- `Base/Back` → `#ECECF4`;
- `Base/On Back` → `#FFFFFF`;
- `Base/Surface` → `#F1F1F8`;
- `Base/Surface Light` → `#F6F6FC`;
- `Text or Icons/Primary` → `#272536`;
- `Text or Icons/Secondary` → `#79789E`;
- `Text or Icons/Secondary Dark` → `#626187`;
- `Text or Icons/Tertiary` → `#8C8BB2`;
- `Text or Icons/Accent Blue` → `#4150F7`;
- `Line/Secondary 2` → `#DAD9E7`.

Из `tokens/semantic/ui-controls.json`:

- `Button/Solid/Brand` → `#F32539`;
- `Button/Solid/Brand Hover` → `#DB172A`;
- `Button/Solid/Brand Active` → `#BD091A`;
- `Button/Solid/Secondary` → `#DAD9E7`;
- `Button/Solid/Secondary Hover` → `#CDCADD`;
- `Button/Solid/Secondary Active` → `#C0BDD3`;
- `Input/Primary/Back` → `#FFFFFF`;
- input stroke uses the DS Light COM neutral control stroke `#DAD9E7`, hover `#CDCADD`.

Из `tokens/semantic/components.json`:

- `Password Requirement/Default Back` → `#DFDFEB`;
- `Password Requirement/Success Back` → `#24A9001A`;
- `Password Requirement/Error Back` → `#F325391A`;
- `Password Requirement/Default Color` → `#626187`;
- `Password Requirement/Success Color` → `#01B462`;
- `Password Requirement/Error Color` → `#F32539`.

## Что не утверждается как DS token

Репозиторий хранит контракты вариантов компонентов, но для `Text Field` не экспортирует геометрию каждого размера. Поэтому высота поля `52px`, радиусы и layout-отступы в HTML помечены как **prototype composition values**, а не как подтверждённые токены дизайн-системы. Их нужно заменить на реальные component dimensions, если они станут доступны в экспорте/Figma API.

Упрощённый логотип в header также является prototype placeholder, а не компонентом DS.

## UX/security decisions

- После отправки используется одинаковое сообщение независимо от того, зарегистрирован e-mail или нет, чтобы не раскрывать существование аккаунта.
- Reset должен выполняться через одноразовый ограниченный по времени token в side-channel, обычно e-mail.
- Новый пароль вводится дважды.
- После успешной смены пользователь возвращается к обычному экрану входа; автоматический login не предполагается.
- Поля используют `autocomplete="email"` и `autocomplete="new-password"`.
- Повторная отправка визуально блокируется после клика; production должен дополнительно иметь server-side rate limiting.

## Prototype-only notes

- `Открыть ссылку из письма` существует только для демонстрации перехода. В production пользователь приходит на новый пароль по ссылке из письма.
- Политика пароля (`8+`, буква, цифра) демонстрационная. В production используется фактическая password policy продукта и те же правила, что при регистрации/смене пароля.

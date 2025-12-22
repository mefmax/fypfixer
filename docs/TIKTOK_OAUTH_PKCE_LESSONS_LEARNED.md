# TikTok OAuth PKCE — Lessons Learned

> **КРИТИЧЕСКИ ВАЖНО**: TikTok Desktop Apps используют НЕСТАНДАРТНУЮ реализацию PKCE!
> Этот документ сохранит вам часы/дни отладки.

**Дата:** 22 декабря 2025
**Проект:** FYPFixer/FYPGlow
**Статус:** РЕШЕНО

---

## Симптомы проблемы

- OAuth авторизация в TikTok проходит успешно
- При обмене code на access_token возвращается **502 Bad Gateway**
- PKCE параметры выглядят корректно
- Redirect URI совпадает везде

---

## Корневая причина

### TikTok НЕ следует стандарту RFC 7636!

| Параметр | RFC 7636 (стандарт) | TikTok Desktop Apps |
|----------|---------------------|---------------------|
| **code_challenge** | BASE64URL(SHA256(verifier)) | HEX(SHA256(verifier)) |
| **Длина challenge** | ~43 символа | **64 символа** |
| **client_secret** | Не нужен при PKCE | **ОБЯЗАТЕЛЕН!** |

---

## Решение

### 1. Frontend: pkce.ts — HEX вместо Base64URL

```typescript
// НЕПРАВИЛЬНО (RFC 7636):
return base64UrlEncode(digest);

// ПРАВИЛЬНО (TikTok):
return arrayBufferToHex(digest);

function arrayBufferToHex(buffer: ArrayBuffer): string {
  const byteArray = new Uint8Array(buffer);
  return Array.from(byteArray)
    .map(byte => byte.toString(16).padStart(2, '0'))
    .join('');
}
```

### 2. Backend: oauth.py — ВСЕ 6 параметров

```python
token_data_payload = {
    'client_key': OAuthConfig.TIKTOK_CLIENT_KEY,
    'client_secret': OAuthConfig.TIKTOK_CLIENT_SECRET,  # ОБЯЗАТЕЛЕН!
    'code': code,
    'grant_type': 'authorization_code',
    'redirect_uri': OAuthConfig.TIKTOK_REDIRECT_URI,
    'code_verifier': code_verifier,
}
```

---

## Чеклист для TikTok OAuth Desktop

- [ ] code_challenge использует HEX (64 символа), НЕ Base64URL
- [ ] code_challenge_method = S256
- [ ] Token exchange включает ВСЕ 6 параметров (включая client_secret!)
- [ ] Redirect URI совпадает ПОБАЙТОВО везде
- [ ] Тестовый пользователь добавлен в TikTok Portal (Sandbox)

---

## Официальная документация

> "Create the code challenge by hashing the code verifier using **hex encoding of SHA256**"
> — [TikTok Login Kit for Desktop](https://developers.tiktok.com/doc/login-kit-desktop)

---

## Быстрая диагностика

```javascript
console.log('Challenge length:', challenge.length);
// ~43 символа → Base64URL (НЕПРАВИЛЬНО для TikTok)
// 64 символа → HEX (ПРАВИЛЬНО)
```

from django.test import override_settings

test_settings = {
    'STOCK_ALERT_EMAIL': 'test@example.com',
    'DEFAULT_FROM_EMAIL': 'noreply@example.com',
    'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
}

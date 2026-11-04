FROM php:8.3-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends git unzip libsqlite3-dev \
    && docker-php-ext-install pdo_sqlite \
    && a2enmod rewrite \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

ENV APACHE_DOCUMENT_ROOT=/var/www/html/public

RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf \
    && sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf \
    && sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf

WORKDIR /var/www/html

COPY composer.json composer.lock ./
RUN composer install --no-dev --no-interaction --prefer-dist --optimize-autoloader --no-scripts

COPY . .

RUN rm -f bootstrap/cache/*.php \
    && mkdir -p \
        storage/framework/cache/data \
        storage/framework/sessions \
        storage/framework/views \
        storage/logs \
        bootstrap/cache \
        database \
    && chown -R www-data:www-data storage bootstrap/cache database \
    && chmod -R 775 storage bootstrap/cache database \
    && composer dump-autoload --no-dev --optimize

EXPOSE 80

CMD ["sh", "-c", "if [ -z \"$APP_KEY\" ]; then unset APP_KEY; fi; if [ ! -f .env ]; then if [ -f .env.example ]; then cp .env.example .env; else touch .env; fi; fi; if ! grep -q '^APP_KEY=base64:' .env && [ -z \"$APP_KEY\" ]; then php artisan key:generate --force; fi; mkdir -p storage/framework/cache/data storage/framework/sessions storage/framework/views storage/logs bootstrap/cache database; touch database/database.sqlite; chown -R www-data:www-data storage bootstrap/cache database; chmod -R 775 storage bootstrap/cache database; php artisan migrate --force; exec apache2-foreground"]

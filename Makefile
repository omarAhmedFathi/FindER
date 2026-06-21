.PHONY: start stop logs migrate test-backend test-flutter build-android build-ios clean

start:
	docker-compose up -d --build

stop:
	docker-compose down

logs:
	docker-compose logs -f backend

migrate:
	docker-compose exec backend alembic upgrade head

test-backend:
	docker-compose exec backend pytest tests/ -v

test-flutter:
	cd mobile && flutter test

build-android:
	cd mobile && flutter build apk --release

build-ios:
	cd mobile && flutter build ipa --release

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	cd mobile && flutter clean

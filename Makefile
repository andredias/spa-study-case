SHELL=/bin/bash -Eeuo pipefail

run:
	cd server && $(MAKE) run

test:
	for path in backend/fastapi_api backend/quart_api backend/tornado_api backend server; do \
		echo -e "\n\n$${path}\n--------------------"; \
		cd $${path}; \
		poetry run make test; \
		cd -; \
	done

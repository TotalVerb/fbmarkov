quotes:
	cp fbm.py build/fbm.py; \
	cd build; \
	python3 fbm.py; \
	cd ..; \
	cp quotes.html build/quotes.html; \
	python3 easy-build.py;

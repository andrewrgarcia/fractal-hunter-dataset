.PHONY: all spectral mixed rename clean

all: spectral mixed clean rename

spectral:
	uv run python scripts/gen_fft.py

mixed:
	uv run python scripts/gen_mixed.py

clean:
	rm -rf spectral/

rename:
	uv run python scripts/rename_data.py
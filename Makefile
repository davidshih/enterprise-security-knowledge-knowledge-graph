.PHONY: test lint demo site site-serve clean

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

lint:
	python3 -m compileall -q src tests

demo:
	PYTHONPATH=src python3 -m security_graph ingest \
		--input data/sample/records.jsonl \
		--output data/out/canonical_graph.json

site:
	python3 scripts/build_site.py --output build/site

site-serve: site
	python3 -m http.server 8000 --directory build/site

clean:
	rm -f data/out/canonical_graph.json
	rm -rf build/site

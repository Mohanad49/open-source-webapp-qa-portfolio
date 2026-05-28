.PHONY: install smoke regression report clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

smoke:
	python -m pytest -m smoke --browser chrome --html=reports/pytest-report.html --self-contained-html --alluredir=reports/allure-results

regression:
	python -m pytest --browser chrome --html=reports/pytest-report.html --self-contained-html --alluredir=reports/allure-results

report:
	allure generate reports/allure-results --clean -o reports/allure-report
	allure open reports/allure-report

clean:
	rm -rf reports downloads .pytest_cache __pycache__ */__pycache__

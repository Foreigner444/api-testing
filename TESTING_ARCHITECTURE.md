
# Testing Framework Architecture

This document outlines the architecture of the API testing framework. The framework is built on Python and leverages several popular open-source libraries to provide a robust, scalable, and maintainable testing solution.

## 1. Core Technology Stack

- **Test Runner:** [Pytest](https://pytest.org/) is the core of the framework, used for test discovery, execution, and fixture management.
- **HTTP Client:** [HTTPX](https://www.python-httpx.org/) is used for sending asynchronous and synchronous HTTP requests to the API under test.
- **Reporting:** [Allure Framework](https://allurereport.org/) is used for generating detailed and interactive test reports. It's integrated with pytest via the `allure-pytest` plugin.
- **Data Validation & Schemas:** [Pydantic](https://pydantic-docs.helpmanual.io/) is used for data validation and defining the schemas for API requests and responses. This ensures that the data being sent and received conforms to the expected structure.
- **Test Data Generation:** [Faker](https://faker.readthedocs.io/) is used to generate realistic test data (e.g., emails, names).
- **Assertions:** The framework uses a combination of custom assertion helpers and the [AssertPy](https://github.com/assertpy/assertpy) library for making fluent and readable assertions.

## 2. Project Structure

The project is organized into the following key directories:

- **`/tests`**: The root directory for all automated tests.
  - **`/tests/<feature>`**: Tests are grouped by feature or service (e.g., `tests/users`, `tests/courses`). This modular structure makes it easy to locate and manage tests for specific parts of the application.
- **`/clients`**: This directory contains the API client modules. Each client is responsible for interacting with a specific set of API endpoints (e.g., `PublicUsersClient`). This encapsulates the logic for making API calls and abstracts away the details of the HTTP requests.
- **`/fixtures`**: This directory holds the pytest fixtures. Fixtures are used to provide a fixed baseline upon which tests can reliably and repeatedly execute. They are organized by feature to match the structure of the tests.
- **`/testdata`**: This directory is intended for storing static test data that can be used across multiple tests.
- **`/tools`**: This directory contains various utility modules and helper functions that support the tests.
  - **`/tools/allure`**: Helpers for Allure reporting, such as custom tags, epics, and features.
  - **`/tools/assertions`**: Custom assertion functions that provide domain-specific validation logic (e.g., `assert_create_user_response`).

## 3. Configuration

- **`pytest.ini`**: This file contains the main configuration for pytest. It defines:
  - Test discovery patterns (`python_files`, `python_classes`, `python_functions`).
  - Custom markers for categorizing tests (e.g., `smoke`, `regression`, `users`).
  - Default command-line options (`addopts`).
- **`conftest.py`**: This file is used for pytest's configuration and fixture discovery. In this framework, it's primarily used to load all the fixture modules from the `/fixtures` directory using the `pytest_plugins` mechanism.

## 4. Test Implementation Style

- **Object-Oriented Structure:** Tests are organized into classes (e.g., `TestUsers`), which group related tests for a specific feature.
- **Data-Driven Testing:** The framework uses `pytest.mark.parametrize` to run the same test with different sets of data, which helps to increase test coverage with less code.
- **Schema-Based Validation:** Pydantic models are used to define the expected JSON schemas for API requests and responses. The `validate_json_schema` helper function is used to validate the actual API responses against these schemas.
- **Descriptive Naming:** Test functions and classes are given descriptive names that clearly indicate their purpose.
- **Rich Reporting:** Tests are heavily decorated with Allure decorators (`@allure.epic`, `@allure.feature`, `@allure.story`, etc.) to provide a hierarchical and well-organized test report.

## 5. Execution and Reporting

- **Test Execution:** Tests are run from the command line using the `pytest` command. Markers can be used to selectively run a subset of tests (e.g., `pytest -m smoke`).
- **Allure Reports:** After a test run, an Allure report can be generated from the `allure-results` directory. This report provides a detailed, interactive dashboard of the test results, including steps, attachments, and historical data.

This architecture promotes a clean separation of concerns, making the test suite easy to understand, maintain, and extend.

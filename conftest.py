pytest_plugins = (
    "fixtures.users",
    "fixtures.files",
    "fixtures.courses",
    "fixtures.exercises",
    "fixtures.authentication",

    "fixtures.allure"
)

def pytest_sessionfinish(session):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # This hook is called by each worker.
    # We need to run our code only from the master.
    if not hasattr(session.config, "workerinput"):
        from tools.allure.environment import create_allure_environment_file
        create_allure_environment_file()

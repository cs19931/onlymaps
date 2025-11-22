from invoke import task

@task
def asyncio(c):
    format(c)
    print("Generating async source code...")
    c.run("python gen_async.py")
    format(c)

@task
def format(c):
    print("Formatting source code...")
    c.run("black onlymaps")
    c.run("isort onlymaps")
    c.run("black tests")
    c.run("isort tests")

@task
def check(c):
    print("Checking for formatting issues...")
    c.run("black --check onlymaps tests")
    c.run("isort --check onlymaps tests")
    print("Running mypy...")
    c.run("mypy onlymaps tests")
    print("Running pylint...")
    c.run("pylint onlymaps")
    c.run("pylint --rcfile=tests/.pylintrc tests")


@task
def test(c):
    asyncio(c)
    c.run("coverage run -m pytest -vvv")

@task
def coverage(c):
    c.run("coverage report -m")

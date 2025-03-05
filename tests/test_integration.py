import subprocess

def execute_command(command):
    return subprocess.run(command, capture_output=True, text=True)

def verify_process_succeeded_without_error(results):
    assert results.returncode == 0, f"Process failed with error:\n{results.stderr}"

def verify_result_contains_text(expected, actual, message=f"Output:"):
    assert expected in actual, f"{message}: {actual}"

def verify_result_does_not_contain_text(not_expected, actual):
    assert not_expected not in actual, f"Unexpected error in:\n{actual}"

def test_city_state_happy_path():
    """
    Ensure a valid city/state returns lat/lon without errors.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", "Madison, WI"
    ]

    result = execute_command(cmd)

    verify_process_succeeded_without_error(results=result)

    stdout = result.stdout
    verify_result_contains_text(expected="Madison, WI -> Lat:", actual=stdout)
    verify_result_does_not_contain_text(not_expected="Error:", actual=stdout)

def test_zip_happy_path():
    """
    Ensure a valid zip returns lat/lon without errors.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", "83686"
    ]
    result = execute_command(cmd)

    verify_process_succeeded_without_error(results=result)

    stdout = result.stdout
    verify_result_contains_text(expected="83686 -> Lat:", actual=stdout)
    verify_result_does_not_contain_text(not_expected="Error:", actual=stdout)

def test_invalid_city_state():
    """
    Ensure an invalid city/state resturns an error.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", "Nopeville, XX"
    ]

    result = execute_command(cmd)

    verify_process_succeeded_without_error(results=result)

    stdout = result.stdout
    verify_result_contains_text(expected="ERROR:", actual=stdout, message="Expected error for invalid city/state")

def test_multiple_locations():
    """
    Ensure multiple locations can be processed in one command.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations",
        "Madison, WI", "99999", "Chicago, IL", "Nope, XX"
    ]

    result = execute_command(cmd)

    verify_process_succeeded_without_error(results=result)

    stdout = result.stdout

    verify_result_contains_text(expected="Madison, WI -> Lat:", actual=stdout)
    verify_result_contains_text(expected="99999 -> Lat:", actual=stdout)
    verify_result_contains_text(expected="Chicago, IL -> Lat:", actual=stdout)
    verify_result_contains_text(expected="Nope, XX -> ERROR:", actual=stdout)

def test_blank_input():
    """
    Ensure error message appears when location is left blank.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", ""
    ]

    result = execute_command(cmd)

    stdout = result.stdout
    verify_result_contains_text(expected="ERROR:", actual=stdout, message="Expected an error for blank input.")

def test_missing_comma_city_state():
    """
    Ensure error message if the city/state doesn't include a comma.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", "Madison WI"
    ]
    result = execute_command(cmd)
    stdout = result.stdout

    verify_process_succeeded_without_error(results=result)
    verify_result_contains_text(expected="ERROR:", actual=stdout, message="Expected error about missing comma.")

def test_non_numeric_zip():
    """
    Ensure error message if zip uses non-numeric.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", "ABCDE"
    ]
    result = execute_command(cmd)
    stdout = result.stdout

    verify_process_succeeded_without_error(results=result)
    verify_result_contains_text(expected="ERROR:", actual=stdout, message="Expected error for non-numeric zip.")

def test_short_zip():
    """
    Ensure error message if zip is too-short.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", "1234"
    ]
    result = execute_command(cmd)
    stdout = result.stdout

    verify_process_succeeded_without_error(results=result)
    verify_result_contains_text(expected="ERROR:", actual=stdout, message="Expected error for short zip.")

def test_long_zip():
    """
    Ensure error message if zip is too long.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", "123456"
    ]
    result = execute_command(cmd)
    stdout = result.stdout

    verify_process_succeeded_without_error(results=result)
    verify_result_contains_text(expected="ERROR:", actual=stdout, message="Expected error for long zip.")

def test_real_city_wrong_state():
    """
    Ensure error message if a real city is used with the wrong state abbreviation.
    """
    cmd = [
        "python",
        "-m", "geoloc_util.geoloc_util",
        "--locations", "Madison, XY"
    ]
    result = execute_command(cmd)
    stdout = result.stdout

    verify_process_succeeded_without_error(results=result)
    verify_result_contains_text(expected="ERROR:", actual=stdout, message="Expected error for a real city with an invalid state.")

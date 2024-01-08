import argparse
import json
import subprocess
import sys
import time
from typing import List, Tuple

try:
    from halo import Halo
except ImportError:
    print("Halo is not installed. Install it with 'pip install halo' to get nice spinners.")
    sys.exit(1)

TEST_CASES_FILE = "tests/all.json"
JAVA_PROGRAM = "ToyFestival"


def load_test_cases(file_name: str = TEST_CASES_FILE) -> List[Tuple[str, str]]:
    """
    Load test cases from a JSON file.

    Args:
        file_name (str): The JSON file name.

    Returns:
        List[Tuple[str, str]]: The loaded test cases.
    """
    with open(file_name, encoding="utf-8") as file:
        return json.load(file)


def measure_execution_time(exec_cmd: str, input_arg: str) -> Tuple[str, float]:
    """
    Measure execution time and output of a command.

    Args:
        exec_cmd (str): The command to execute.
        input_arg (str): The input argument for the command.

    Returns:
        Tuple[str, float]: The output and execution time.
    """
    start_time = time.time()
    
    proc = subprocess.Popen(exec_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    try:
        output, error = proc.communicate(input=input_arg.encode())
    except subprocess.CalledProcessError as error:
        output = error.output.decode('utf-8')

    execution_time = time.time() - start_time
    return output.decode('utf-8'), execution_time


def run_test_case(
    exec_cmd: str, input_arg: str, expected_output: str, test_case_num: int,
    track_time: bool, verbose: bool
) -> None:
    """
    Run a test case.

    Args:
        exec_cmd (str): The command to execute.
        input_arg (str): The input argument for the command.
        expected_output (str): The expected output.
        test_case_num (int): The test case number.
        track_time (bool): Whether to track execution time.
        verbose (bool): Whether to print verbose output.
    """
    spinner = Halo(text=f'Running test case {test_case_num}', spinner='dots')
    spinner.start()

    leak_info = ""
    execution_time = None
    mem_msg = ""
    num_nested_test_cases = input_arg.split("\n")[0]
    
    output, _ = measure_execution_time(exec_cmd, input_arg)

    time_msg = ""
    if track_time:
        _, execution_time = measure_execution_time(exec_cmd, input_arg)
        time_msg = f"Execution time: {execution_time} seconds. " if verbose else ""

    in_out_msg = ""
    if output.strip() == expected_output.strip():
        if verbose:
            in_out_msg = f"Input: '{input_arg}'. Output: '{output.strip()}'. "
        spinner_text = f"{num_nested_test_cases} test cases passed! {time_msg}{mem_msg}{in_out_msg}"
        if not verbose and "No memory leaks!" in leak_info:
            spinner_text = f"{num_nested_test_cases} test cases passed with no memory leaks! {mem_msg}"
        if track_time and execution_time is not None:
            spinner_text += f" Execution time: {execution_time} seconds."
        spinner.succeed(spinner_text)
        if verbose and leak_info:
            print(leak_info)
    else:
        print(f"DEBUG: Expected: '{expected_output.strip()}', Got: '{output.strip()}'")
        spinner.fail(
            f"{num_nested_test_cases} test cases failed. Input: '{input_arg}'. Expected output: "
            f"'{expected_output.strip()}', got '{output.strip()}'"
        )

def run_all_test_cases(
    exec_cmd: str, cases: List[Tuple[str, str]], track_time: bool, verbose: bool
) -> None:
    """
    Run all test cases.

    Args:
        exec_cmd (str): The command to execute.
        cases (List[Tuple[str, str]]): The test cases.
        track_time (bool): Whether to track execution time.
        verbose (bool): Whether to print verbose output.
    """
    for i in range(len(cases)):
        input_arg = cases[i].get("input")
        expected_output = cases[i].get("output")
        run_test_case(exec_cmd, input_arg, expected_output, i + 1, track_time, verbose)


def compile_java_program() -> None:
    """
    Compile the Java program.
    """
    with Halo(text='Compiling Java program', spinner='dots') as halo:
        subprocess.check_output(f"javac {JAVA_PROGRAM}.java", shell=True)
        halo.succeed("Java program compiled successfully!")


def main() -> None:
    """
    Main function to parse arguments and run test cases.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--track-time", action="store_true", help="Enable execution time tracking.")
    parser.add_argument("--verbose", action="store_true", help="Print input and output for passed tests.")
    args = parser.parse_args()

    compile_java_program()

    exec_cmd = f"java {JAVA_PROGRAM}"
    try:
        test_cases = load_test_cases()
        run_all_test_cases(exec_cmd, test_cases, args.track_time, args.verbose)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        exit(0)


if __name__ == "__main__":
    main()
    
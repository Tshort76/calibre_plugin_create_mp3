from calibre.gui2.threaded_jobs import ThreadedJob
import subprocess, os

DASHED_LINE = "-" * 50


def _get_book_name(command: list[str]) -> str:
    for p in command:
        for ext in [".txt", ".epub", ".pdf"]:
            if ext in p:
                return os.path.basename(p)
    return " ".join(command)[-60:]


def run_external_script(gui, commands):
    # Passing a vector as a positional argument to ThreadedJob was throwing errors ... so wrap it
    def worker_wrapper(log, abort, notifications):
        return run_script_worker(commands, log=log, abort=abort, notifications=notifications)

    job_name = "Create MP3 : " + ", ".join(map(_get_book_name, commands))

    job = ThreadedJob(
        "external_script_runner",
        job_name,
        worker_wrapper,
        (),
        {},
        callback=Dispatcher(script_finished),
        max_concurrent_count=1,
        killable=True,
    )

    gui.job_manager.run_threaded_job(job)
    gui.status_bar.show_message("MP3 conversion started...", 3000)


def run_script_worker(commands: list[list[str]], log, abort, notifications):

    log(f"Processing {len(commands)} book(s)")
    log(DASHED_LINE)

    results = []

    for idx, command in enumerate(commands):
        _job_id = _get_book_name(command)
        log(f"Running: {_job_id}")

        if abort is not None and abort.is_set():
            log("\n" + DASHED_LINE)
            log("Job aborted by user")
            break

        log(f"\n[Book {idx + 1}/{len(commands)}]\n{DASHED_LINE}")

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                bufsize=1,  # Line buffered
            )

            stdout_lines = []
            stderr_lines = []

            while True:
                if abort is not None and abort.is_set():
                    process.kill()
                    log("\nProcess killed by user abort")
                    break

                line = process.stdout.readline()
                if not line:
                    break

                # Remove trailing newline and log immediately
                line = line.rstrip("\n\r")
                if line:  # Only log non-empty lines
                    log(line)
                    stdout_lines.append(line)

            # Wait for process to complete and get any remaining stderr
            process.wait()
            stderr = process.stderr.read()

            if stderr:
                stderr_lines = stderr.strip().split("\n")
                stderr_lines = list(filter(lambda x: ".venv\Lib" not in x, stderr_lines))
                log("\n--- Error Output ---")
                for err_line in stderr_lines:
                    if err_line and ".venv":
                        log(err_line)

            if process.returncode == 0:
                log(f"\n✓ Successfully processed: {_job_id}")
                results.append((_job_id, True, "\n".join(stdout_lines)))
            else:
                log(f"\n✗ Failed processing: {_job_id}")
                log(f"Return code: {process.returncode}")
                results.append((_job_id, False, stderr))

        except Exception as e:
            log(f"\n✗ Exception while processing {_job_id}")
            log(f"Error: {str(e)}")
            results.append((_job_id, False, str(e)))

    log("\n" + DASHED_LINE)
    log(f"Completed processing {len(results)} book(s)")

    success_count = sum(1 for _, success, _ in results if success)
    failure_count = len(results) - success_count
    log(f"Successful: {success_count}, Failed: {failure_count}")

    return results


class Dispatcher:
    """Callback dispatcher for job completion"""

    def __init__(self, func):
        self.func = func

    def __call__(self, job):
        self.func(job)


def script_finished(job):
    """Called when the job completes"""
    if job.failed:
        from calibre.gui2 import error_dialog

        error_dialog(
            job.gui, "Script Failed", f"The external script failed:\n\n{job.details}", show=True, show_copy_button=True
        )
        return

    results = job.result
    success_count = sum(1 for _, success, _ in results if success)
    failure_count = len(results) - success_count

    from calibre.gui2 import info_dialog

    msg = f"Script execution completed.\n\n"
    msg += f"Successful: {success_count}\n"
    msg += f"Failed: {failure_count}\n\n"
    msg += "Check the job log for details."

    info_dialog(job.gui, "Script Complete", msg, show=True)

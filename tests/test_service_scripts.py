"""Tests to validate service scripts syntax, permissions, and S6-overlay conventions."""

import os
import stat
import subprocess
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADDONS = ["weewx", "radicale"]


class TestServiceScripts(unittest.TestCase):
    """Test suite for S6 service scripts and rootfs."""

    def test_service_directories_exist(self):
        for addon in ADDONS:
            service_dir = os.path.join(REPO_ROOT, addon, "rootfs", "etc", "services.d", addon)
            self.assertTrue(os.path.isdir(service_dir), f"Service directory missing for {addon} at {service_dir}")

            run_script = os.path.join(service_dir, "run")
            finish_script = os.path.join(service_dir, "finish")

            self.assertTrue(os.path.isfile(run_script), f"run script missing for {addon}")
            self.assertTrue(os.path.isfile(finish_script), f"finish script missing for {addon}")

    def test_service_scripts_permissions(self):
        for addon in ADDONS:
            service_dir = os.path.join(REPO_ROOT, addon, "rootfs", "etc", "services.d", addon)
            for script_name in ["run", "finish"]:
                script_path = os.path.join(service_dir, script_name)
                st = os.stat(script_path)
                is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
                self.assertTrue(is_executable, f"{script_path} must have executable permissions")

    def test_service_scripts_syntax(self):
        for addon in ADDONS:
            service_dir = os.path.join(REPO_ROOT, addon, "rootfs", "etc", "services.d", addon)
            for script_name in ["run", "finish"]:
                script_path = os.path.join(service_dir, script_name)
                result = subprocess.run(
                    ["bash", "-n", script_path],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    f"Bash syntax error in {script_path}:\n{result.stderr}",
                )

    def test_service_scripts_shebang(self):
        for addon in ADDONS:
            service_dir = os.path.join(REPO_ROOT, addon, "rootfs", "etc", "services.d", addon)
            run_script = os.path.join(service_dir, "run")
            with open(run_script, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
            self.assertTrue(
                "bashio" in first_line or "bash" in first_line or "sh" in first_line,
                f"Unexpected shebang in {run_script}: {first_line}",
            )


if __name__ == "__main__":
    unittest.main()

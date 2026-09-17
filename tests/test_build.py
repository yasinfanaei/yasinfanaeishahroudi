import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class BuildFoundationTests(unittest.TestCase):
    def test_builder_creates_output_root(self):
        from src.build_site import build_site
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "site"
            build_site(ROOT, out)
            self.assertTrue(out.exists())
            self.assertTrue((out / "index.html").exists())

    def test_builder_supports_documented_direct_script_entrypoint(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "site"
            result = subprocess.run(
                [sys.executable, "src/build_site.py", "--output", str(out)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((out / "index.html").exists())

if __name__ == "__main__": unittest.main()

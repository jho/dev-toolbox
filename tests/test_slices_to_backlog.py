import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
import slices_to_backlog as planner  # noqa: E402


class SlicesToBacklogTests(unittest.TestCase):
    def test_no_relevant_changes_is_not_ready(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(planner, "changed_files", return_value={"README.md": "M"}), patch.object(
                planner, "run_git", return_value="head"
            ):
                graph = planner.build_graph(root, "base")

        self.assertFalse(graph["ready"])
        self.assertIn("No changed Event Model", graph["blockers"][0])

    def test_changed_slice_becomes_work_item(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            model = root / "budgeting.em"
            slice_path = root / "slices" / "categorize.md"
            slice_path.parent.mkdir()
            model.touch()
            slice_path.touch()

            def em_result(_root, args):
                if args[0] == "export":
                    return {
                        "ok": True,
                        "value": {
                            "model": {
                                "slices": [
                                    {
                                        "key": "categorize",
                                        "pattern": "state-change",
                                        "doc": {
                                            "path": "slices/categorize.md",
                                            "status": "ready-to-implement",
                                            "ratifiedOn": "2026-01-01",
                                        },
                                    }
                                ]
                            }
                        },
                    }
                return {"ok": True, "value": {}}

            with patch.object(
                planner,
                "changed_files",
                return_value={"budgeting.em": "M", "slices/categorize.md": "A"},
            ), patch.object(planner, "run_em", side_effect=em_result), patch.object(
                planner, "run_git", return_value="head"
            ):
                graph = planner.build_graph(root, "base")

        self.assertTrue(graph["ready"])
        self.assertEqual(graph["workItems"][0]["id"], "categorize")
        self.assertEqual(graph["workItems"][0]["stage"], "implement")


if __name__ == "__main__":
    unittest.main()

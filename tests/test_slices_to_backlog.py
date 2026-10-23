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
        self.assertEqual(graph["workItems"][0]["pattern"], "state-change")

    def test_nested_model_ignores_deleted_root_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            model_dir = root / "docs" / "event-model"
            slices_dir = model_dir / "slices"
            slices_dir.mkdir(parents=True)
            (model_dir / "budgeting.em").touch()
            (model_dir / ".event-modeling.md").write_text(
                "**Current phase:** slice\n**Current step:** 6\n"
            )
            (slices_dir / "setup.md").touch()

            def em_result(_root, args):
                if args[0] == "export":
                    return {
                        "ok": True,
                        "value": {
                            "model": {
                                "slices": [
                                    {
                                        "key": "setup",
                                        "pattern": "state-change",
                                        "elements": [],
                                        "doc": {
                                            "path": "slices/setup.md",
                                            "status": "draft",
                                            "ratifiedOn": None,
                                        },
                                    }
                                ]
                            }
                        },
                    }
                return {"ok": True, "value": {}}

            changed = {
                ".event-modeling.md": "D",
                "budgeting.em": "D",
                "docs/event-model/.event-modeling.md": "A",
                "docs/event-model/budgeting.em": "A",
                "docs/event-model/slices/setup.md": "A",
            }
            with patch.object(planner, "changed_files", return_value=changed), patch.object(
                planner, "run_em", side_effect=em_result
            ), patch.object(planner, "run_git", return_value="head"):
                graph = planner.build_graph(root, "base")

        self.assertEqual(graph["models"][0]["path"], "docs/event-model/budgeting.em")
        self.assertEqual(graph["eventModelingState"][0]["path"], "docs/event-model/.event-modeling.md")
        self.assertEqual(graph["workItems"][0]["id"], "setup")
        self.assertTrue(any("not ready to implement" in blocker for blocker in graph["blockers"]))

    def test_dependencies_are_derived_from_model_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            model = root / "budgeting.em"
            state = root / ".event-modeling.md"
            first = root / "slices" / "first.md"
            second = root / "slices" / "second.md"
            first.parent.mkdir()
            for path in (model, state, first, second):
                path.touch()

            def em_result(_root, args):
                if args[0] == "export":
                    return {
                        "ok": True,
                        "value": {
                            "model": {
                                "slices": [
                                    {
                                        "key": "first",
                                        "pattern": "state-change",
                                        "elements": [],
                                        "doc": {"path": "slices/first.md", "status": "ready-to-implement", "ratifiedOn": "today"},
                                    },
                                    {
                                        "key": "second",
                                        "pattern": "state-view",
                                        "elements": [],
                                        "doc": {"path": "slices/second.md", "status": "ready-to-implement", "ratifiedOn": "today"},
                                    },
                                ],
                                "arrows": [
                                    {
                                        "fromRef": "first/event.created",
                                        "toRef": "second/view.created",
                                    }
                                ],
                            }
                        },
                    }
                return {"ok": True, "value": {}}

            with patch.object(
                planner,
                "changed_files",
                return_value={"budgeting.em": "M", "slices/first.md": "A", "slices/second.md": "A"},
            ), patch.object(planner, "run_em", side_effect=em_result), patch.object(
                planner, "run_git", return_value="head"
            ):
                graph = planner.build_graph(root, "base")

        self.assertTrue(graph["ready"])
        self.assertEqual(graph["workItems"][1]["dependsOn"], ["first"])

    def test_pinned_pre_commit_command_is_preferred(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".pre-commit-config.yaml").write_text(
                "entry: npx --yes @milehimikey/em@1.13.0 validate docs/event-model/budgeting.em\n"
            )

            resolved = planner.em_command(root)

        self.assertEqual(resolved["command"], ["npx", "--yes", "@milehimikey/em@1.13.0"])
        self.assertEqual(resolved["source"], ".pre-commit-config.yaml")
        self.assertEqual(resolved["version"], "1.13.0")


if __name__ == "__main__":
    unittest.main()

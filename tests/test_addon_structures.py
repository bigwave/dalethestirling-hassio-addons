"""Tests to validate add-on structure, metadata, and configuration schemas."""

import os
import unittest
import yaml
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADDONS = ["weewx", "radicale"]


class TestRepositoryStructure(unittest.TestCase):
    """Test suite for top-level repository files."""

    def test_repository_yaml_exists_and_valid(self):
        repo_yaml_path = os.path.join(REPO_ROOT, "repository.yaml")
        self.assertTrue(os.path.isfile(repo_yaml_path), "repository.yaml must exist")

        with open(repo_yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.assertIsInstance(data, dict)
        self.assertIn("name", data)
        self.assertIn("url", data)
        self.assertIn("maintainer", data)
        self.assertTrue(len(data["name"]) > 0)
        self.assertTrue(len(data["url"]) > 0)

    def test_readme_and_licence_exist(self):
        readme_path = os.path.join(REPO_ROOT, "README.md")
        self.assertTrue(os.path.isfile(readme_path), "Root README.md must exist")

        licence_exists = os.path.isfile(os.path.join(REPO_ROOT, "LICENCE.md")) or os.path.isfile(
            os.path.join(REPO_ROOT, "LICENSE")
        )
        self.assertTrue(licence_exists, "LICENCE.md or LICENSE must exist")

    def test_readme_mentions_all_addons(self):
        readme_path = os.path.join(REPO_ROOT, "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        for addon in ADDONS:
            self.assertIn(addon, content, f"Root README.md should mention add-on '{addon}'")


class TestAddonFilesAndConfig(unittest.TestCase):
    """Test suite for individual add-on directories."""

    def test_addons_exist(self):
        for addon in ADDONS:
            addon_dir = os.path.join(REPO_ROOT, addon)
            self.assertTrue(os.path.isdir(addon_dir), f"Add-on directory '{addon}' must exist")

    def test_addon_config_yaml(self):
        required_fields = ["name", "version", "slug", "description", "arch", "image"]
        valid_arches = ["aarch64", "amd64", "armv7", "armhf", "i386"]

        for addon in ADDONS:
            config_path = os.path.join(REPO_ROOT, addon, "config.yaml")
            self.assertTrue(os.path.isfile(config_path), f"{addon}/config.yaml must exist")

            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            self.assertIsInstance(config, dict, f"{addon}/config.yaml must parse to a dict")

            for field in required_fields:
                self.assertIn(field, config, f"{addon}/config.yaml missing required field '{field}'")

            self.assertEqual(config["slug"], addon, f"Slug in {addon}/config.yaml must match folder name")
            self.assertIsInstance(config["arch"], list, f"{addon}/config.yaml 'arch' must be a list")
            self.assertTrue(len(config["arch"]) > 0, f"{addon}/config.yaml 'arch' list must not be empty")

            for arch in config["arch"]:
                self.assertIn(arch, valid_arches, f"Unknown arch '{arch}' in {addon}/config.yaml")

            if "webui" in config:
                self.assertTrue(
                    config["webui"].startswith("http://") or config["webui"].startswith("https://"),
                    f"webui in {addon}/config.yaml must be a valid URL scheme",
                )

            if "ports" in config and config["ports"] is not None:
                self.assertIsInstance(config["ports"], dict, f"ports in {addon}/config.yaml must be a dict")

    def test_addon_build_yaml(self):
        for addon in ADDONS:
            build_path = os.path.join(REPO_ROOT, addon, "build.yaml")
            self.assertTrue(os.path.isfile(build_path), f"{addon}/build.yaml must exist")

            with open(build_path, "r", encoding="utf-8") as f:
                build = yaml.safe_load(f)

            self.assertIsInstance(build, dict, f"{addon}/build.yaml must parse to a dict")
            self.assertIn("build_from", build, f"{addon}/build.yaml must have 'build_from'")
            self.assertIsInstance(build["build_from"], dict, f"'build_from' in {addon}/build.yaml must be a dict")

            # Check matching architectures
            config_path = os.path.join(REPO_ROOT, addon, "config.yaml")
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            for arch in config["arch"]:
                self.assertIn(
                    arch,
                    build["build_from"],
                    f"Arch '{arch}' enabled in {addon}/config.yaml but missing in {addon}/build.yaml build_from",
                )

    def test_addon_dockerfile(self):
        for addon in ADDONS:
            dockerfile_path = os.path.join(REPO_ROOT, addon, "Dockerfile")
            self.assertTrue(os.path.isfile(dockerfile_path), f"{addon}/Dockerfile must exist")

            with open(dockerfile_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("ARG BUILD_FROM", content, f"{addon}/Dockerfile must declare ARG BUILD_FROM")
            self.assertIn("FROM $BUILD_FROM", content, f"{addon}/Dockerfile must use FROM $BUILD_FROM")
            self.assertIn("COPY rootfs /", content, f"{addon}/Dockerfile must copy rootfs")

    def test_addon_documentation(self):
        for addon in ADDONS:
            docs_path = os.path.join(REPO_ROOT, addon, "DOCS.md")
            readme_path = os.path.join(REPO_ROOT, addon, "README.md")
            changelog_path = os.path.join(REPO_ROOT, addon, "CHANGELOG.md")

            self.assertTrue(os.path.isfile(docs_path), f"{addon}/DOCS.md must exist")
            self.assertTrue(os.path.isfile(readme_path), f"{addon}/README.md must exist")
            self.assertTrue(os.path.isfile(changelog_path), f"{addon}/CHANGELOG.md must exist")

            with open(docs_path, "r", encoding="utf-8") as f:
                self.assertGreater(len(f.read().strip()), 100, f"{addon}/DOCS.md is too short")

            with open(readme_path, "r", encoding="utf-8") as f:
                self.assertGreater(len(f.read().strip()), 50, f"{addon}/README.md is too short")

            with open(changelog_path, "r", encoding="utf-8") as f:
                self.assertIn("##", f.read(), f"{addon}/CHANGELOG.md must have version headings")

    def test_addon_icons(self):
        for addon in ADDONS:
            icon_path = os.path.join(REPO_ROOT, addon, "icon.png")
            logo_path = os.path.join(REPO_ROOT, addon, "logo.png")

            self.assertTrue(os.path.isfile(icon_path), f"{addon}/icon.png must exist")
            self.assertTrue(os.path.isfile(logo_path), f"{addon}/logo.png must exist")

            with Image.open(icon_path) as icon_img:
                self.assertEqual(icon_img.format, "PNG", f"{addon}/icon.png must be PNG format")
                self.assertGreaterEqual(icon_img.width, 128, f"{addon}/icon.png width must be at least 128px")
                self.assertGreaterEqual(icon_img.height, 128, f"{addon}/icon.png height must be at least 128px")

            with Image.open(logo_path) as logo_img:
                self.assertEqual(logo_img.format, "PNG", f"{addon}/logo.png must be PNG format")

    def test_addon_translations(self):
        for addon in ADDONS:
            trans_path = os.path.join(REPO_ROOT, addon, "translations", "en.yaml")
            self.assertTrue(os.path.isfile(trans_path), f"{addon}/translations/en.yaml must exist")

            with open(trans_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            self.assertIsInstance(data, dict)
            self.assertIn("configuration", data)


if __name__ == "__main__":
    unittest.main()

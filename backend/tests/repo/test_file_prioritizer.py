from app.repo.file_prioritizer import get_file_weight


# base

def test_default_weight():
    assert get_file_weight("random/file.txt") == 1


# global rules

def test_readme_has_highest_priority():
    assert get_file_weight("README.md") == 4
    assert get_file_weight("docs/readme.txt") == 4


def test_package_json():
    assert get_file_weight("package.json") == 3
    assert get_file_weight("frontend/package.json") == 3


def test_config_boost():
    assert get_file_weight("config/settings.py") == 2
    assert get_file_weight("app/config.yaml") == 2


# unity

def test_unity_scripts_priority():
    assert get_file_weight("Assets/scripts/player.cs", framework="unity") == 4


def test_unity_ui_priority():
    assert get_file_weight("Assets/ui/menu.cs", framework="unity") == 3


# nuxt

def test_nuxt_pages_priority():
    assert get_file_weight("pages/index.vue", framework="nuxt") == 4


def test_nuxt_components_priority():
    assert get_file_weight("components/Button.vue", framework="nuxt") == 3


def test_nuxt_layouts_priority():
    assert get_file_weight("layouts/default.vue", framework="nuxt") == 3


# fastapi

def test_fastapi_main_priority():
    assert get_file_weight("main.py", framework="fastapi") == 4


def test_fastapi_routers_priority():
    assert get_file_weight("routers/user.py", framework="fastapi") == 3


# priority stacking

def test_config_and_framework_take_max():
    # config gives 2, pages gives 4 → expect 4
    assert get_file_weight("pages/config.vue", framework="nuxt") == 4


def test_config_without_framework():
    assert get_file_weight("config/file.py") == 2


# edge

def test_case_insensitivity():
    assert get_file_weight("README.MD") == 4
    assert get_file_weight("Pages/Index.vue", framework="nuxt") == 4

import flet as ft
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

APP_NAME = "Flet Studio"
ROOT = Path.home() / "FletStudio"
PROJECTS_DIR = ROOT / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


def safe_name(value):
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip()).strip("_").lower()
    return value or "my_flet_app"


def starter_code(title="My Flet App"):
    return f'''import flet as ft


def main(page: ft.Page):
    page.title = "{title}"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text("{title}", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Built with Flet Studio"),
                    ft.Button("Get started"),
                ],
                spacing=16,
            )
        )
    )


ft.run(main)
'''


def read_manifest(folder):
    try:
        return json.loads((folder / "studio.json").read_text(encoding="utf-8"))
    except Exception:
        return {"name": folder.name, "created": ""}


def write_project(folder, name, code=None):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "main.py").write_text(code or starter_code(name), encoding="utf-8")
    (folder / "studio.json").write_text(json.dumps({
        "name": name, "created": datetime.now().isoformat(timespec="seconds")
    }, indent=2), encoding="utf-8")
    (folder / "pyproject.toml").write_text(f'''[project]
name = "{safe_name(name).replace("_", "-")}"
version = "0.1.0"
description = "Created with Flet Studio"
readme = "README.md"
requires-python = ">=3.10"
dependencies = ["flet==1.1.2"]
''', encoding="utf-8")
    (folder / "requirements.txt").write_text("flet==1.1.2\n", encoding="utf-8")
    (folder / "README.md").write_text(
        f"# {name}\n\nCreated with Flet Studio.\n\nRun: `python main.py`\n\nBuild APK on a configured computer: `flet build apk`\n",
        encoding="utf-8"
    )


def main(page: ft.Page):
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.with_opacity(0.04, ft.Colors.BLACK)

    state = {"folder": None, "name": "", "code": "", "items": [], "tab": 0}
    snack = ft.SnackBar(content=ft.Text(""))

    def notify(message):
        snack.content = ft.Text(message)
        if snack not in page.overlay:
            page.overlay.append(snack)
        snack.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def current_code():
        if editor.value is not None:
            state["code"] = editor.value
        return state["code"]

    def save(show=True):
        folder = state["folder"]
        if not folder:
            notify("Create or open a project first.")
            return
        (folder / "main.py").write_text(current_code(), encoding="utf-8")
        if show:
            notify("Project saved.")

    editor = ft.TextField(
        value="", multiline=True, min_lines=18, max_lines=35, expand=True,
        text_size=12, text_style=ft.TextStyle(font_family="monospace"),
        border_color=ft.Colors.with_opacity(0.18, ft.Colors.WHITE),
        focused_border_color=ft.Colors.TEAL_300,
        hint_text="Write Python code here..."
    )
    project_label = ft.Text("No project open", size=12, color=ft.Colors.GREY_400)
    projects_list = ft.Column(spacing=8, expand=True, scroll=ft.ScrollMode.AUTO)
    designer_canvas = ft.Column(spacing=8, expand=True, scroll=ft.ScrollMode.AUTO)
    preview_area = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.AUTO)
    export_output = ft.TextField(multiline=True, read_only=True, min_lines=6, max_lines=12,
                                  text_size=11, text_style=ft.TextStyle(font_family="monospace"))
    pages = []
    body = ft.Container(expand=True, padding=16)

    def refresh_projects():
        projects_list.controls.clear()
        projects = []
        for folder in PROJECTS_DIR.iterdir():
            if folder.is_dir() and (folder / "main.py").exists():
                projects.append((folder, read_manifest(folder)))
        projects.sort(key=lambda item: item[1].get("created", ""), reverse=True)
        if not projects:
            projects_list.controls.append(empty_state("No projects yet", "Create your first Flet app."))
        for folder, manifest in projects:
            name = manifest.get("name", folder.name)
            projects_list.controls.append(ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.FOLDER_CODE, color=ft.Colors.TEAL_200, size=24),
                    ft.Column([
                        ft.Text(name, weight=ft.FontWeight.BOLD),
                        ft.Text(folder.name, size=10, color=ft.Colors.GREY_500)
                    ], expand=True, spacing=3),
                    ft.IconButton(ft.Icons.CHEVRON_RIGHT, on_click=lambda e, f=folder: open_project(f)),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=lambda e, f=folder: delete_project(f)),
                ]),
                padding=10, border_radius=13,
                bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE)
            ))
        page.update()

    def empty_state(title, subtitle):
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.FOLDER_OPEN, size=38, color=ft.Colors.GREY_600),
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=11, color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            padding=24, alignment=ft.Alignment.CENTER
        )

    def open_project(folder):
        state["folder"] = folder
        manifest = read_manifest(folder)
        state["name"] = manifest.get("name", folder.name)
        state["code"] = (folder / "main.py").read_text(encoding="utf-8")
        editor.value = state["code"]
        project_label.value = state["name"]
        refresh_preview()
        show_tab(1)
        notify("Project opened.")

    def delete_project(folder):
        def do_delete(e):
            shutil.rmtree(folder, ignore_errors=True)
            if state["folder"] == folder:
                state["folder"] = None
                state["code"] = ""
                editor.value = ""
                project_label.value = "No project open"
            close_dialog(dialog)
            refresh_projects()
            notify("Project deleted.")
        dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Delete project?"),
            content=ft.Text(f"Delete {folder.name} and all its files?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(dialog)),
                ft.Button("Delete", on_click=do_delete, bgcolor=ft.Colors.RED_700)
            ]
        )
        page.show_dialog(dialog)

    def create_project(e=None):
        name_field = ft.TextField(label="Project name", value="My Flet App", autofocus=True)
        def create(e):
            name = name_field.value.strip() or "My Flet App"
            folder = PROJECTS_DIR / safe_name(name)
            if folder.exists():
                notify("That project already exists.")
                return
            write_project(folder, name)
            close_dialog(dialog)
            open_project(folder)
            refresh_projects()
            notify("Project created.")
        dialog = ft.AlertDialog(
            modal=True, title=ft.Text("New project"),
            content=name_field,
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog(dialog)),
                ft.Button("Create", on_click=create)
            ]
        )
        page.show_dialog(dialog)

    def refresh_preview():
        preview_area.controls.clear()
        if not state["folder"]:
            preview_area.controls.append(empty_state("No preview", "Open a project first."))
        else:
            preview_area.controls.append(ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(width=7, height=7, bgcolor=ft.Colors.GREEN_400, border_radius=8),
                        ft.Text("APP PREVIEW", size=10, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_400),
                        ft.Container(expand=True),
                        ft.Text("390 × 844", size=10, color=ft.Colors.GREY_500)
                    ]),
                    ft.Divider(),
                    ft.Text(state["name"], size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Built with Flet Studio", color=ft.Colors.GREY_400),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Welcome 👋", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text("Your app preview appears here.", color=ft.Colors.GREY_400),
                            ft.Button("Get started")
                        ], spacing=12),
                        padding=18, border_radius=15,
                        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.TEAL)
                    ),
                    ft.Text("Mock preview. Run main.py to execute your actual app.",
                            size=10, color=ft.Colors.GREY_500)
                ], spacing=12),
                padding=18, border_radius=22,
                bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE)
            ))

    def add_component(kind):
        state["items"].append(kind)
        render_canvas()
        notify(f"{kind} added.")

    def remove_component(index):
        if index < len(state["items"]):
            state["items"].pop(index)
        render_canvas()

    def render_canvas():
        designer_canvas.controls.clear()
        if not state["items"]:
            designer_canvas.controls.append(empty_state("Empty canvas", "Choose a component to add."))
        icons = {
            "Text": ft.Icons.TEXT_FIELDS, "Button": ft.Icons.SMART_BUTTON,
            "Container": ft.Icons.CROP_SQUARE, "Image": ft.Icons.IMAGE_OUTLINED,
            "Row": ft.Icons.TABLE_ROWS, "Column": ft.Icons.VIEW_COLUMN
        }
        for index, kind in enumerate(state["items"]):
            designer_canvas.controls.append(ft.Container(
                content=ft.Row([
                    ft.Icon(icons[kind], color=ft.Colors.TEAL_200),
                    ft.Text(kind, expand=True),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE,
                                  on_click=lambda e, i=index: remove_component(i))
                ]),
                padding=10, border_radius=12,
                bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE)
            ))
        page.update()

    def generate_code(e=None):
        if not state["folder"]:
            notify("Create or open a project first.")
            return
        generated = []
        for kind in state["items"]:
            if kind == "Text":
                generated.append('                    ft.Text("New text", size=20),')
            elif kind == "Button":
                generated.append('                    ft.Button("Click me"),')
            elif kind == "Container":
                generated.append('                    ft.Container(content=ft.Text("Container"), padding=12),')
            elif kind == "Image":
                generated.append('                    ft.Text("[Image placeholder]"),')
            elif kind == "Row":
                generated.append('                    ft.Row(controls=[ft.Text("Left"), ft.Text("Right")]),')
            elif kind == "Column":
                generated.append('                    ft.Column(controls=[ft.Text("Item 1"), ft.Text("Item 2")]),')
        if not generated:
            generated = ['                    ft.Text("Hello from my app!"),']
        state["code"] = f'''import flet as ft


def main(page: ft.Page):
    page.title = "{state["name"]}"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
{chr(10).join(generated)}
                ],
                spacing=12,
            )
        )
    )


ft.run(main)
'''
        editor.value = state["code"]
        save(False)
        show_tab(3)
        notify("Code generated from visual design.")

    def save_code(e=None):
        save(True)

    def run_preview(e=None):
        save(False)
        refresh_preview()
        show_tab(4)
        notify("Preview refreshed. Run main.py for a real app preview.")

    def export_project(e=None):
        if not state["folder"]:
            notify("Create or open a project first.")
            return
        save(False)
        export_output.value = f'''Project: {state["name"]}
Folder: {state["folder"]}

Included files:
  main.py
  pyproject.toml
  requirements.txt
  README.md
  studio.json

Run:
  python -m pip install -r requirements.txt
  python main.py

Build Android APK (on a computer with Flutter + Android SDK):
  flet build apk

Build checklist:
  1. Install Python 3.10+.
  2. Install Flutter and Android SDK.
  3. Accept Android SDK licenses.
  4. Open the project folder in a terminal.
  5. Run: flet build apk
  6. Find the APK in the build output directory.

Flet Studio exports source files and instructions.
APK compilation requires a configured build environment.
'''
        show_tab(5)
        page.update()

    def copy_export(e=None):
        if export_output.value:
            page.set_clipboard(export_output.value)
            notify("Instructions copied.")

    def use_template(name):
        templates = {
            "Counter app": '''import flet as ft

def main(page: ft.Page):
    page.title = "Counter App"
    count = ft.Text("0", size=36, weight=ft.FontWeight.BOLD)
    def increment(e):
        count.value = str(int(count.value) + 1)
        page.update()
    page.add(ft.Column([ft.Text("Counter", size=26), count,
                        ft.Button("Add", on_click=increment)]))
ft.run(main)
''',
            "Profile UI": '''import flet as ft

def main(page: ft.Page):
    page.title = "Profile"
    page.add(ft.Card(content=ft.Container(
        content=ft.Column([
            ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON), radius=34),
            ft.Text("Your Name", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Flet developer"),
            ft.Button("Edit profile"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=24)))
ft.run(main)
''',
            "Dashboard": '''import flet as ft

def main(page: ft.Page):
    page.title = "Dashboard"
    page.add(ft.Column([
        ft.Text("Dashboard", size=28, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.Card(content=ft.Container(content=ft.Text("Projects: 12"), padding=18)),
            ft.Card(content=ft.Container(content=ft.Text("Users: 240"), padding=18)),
        ]),
        ft.Text("Recent activity"),
        ft.ListTile(title=ft.Text("Welcome to your dashboard"),
                    leading=ft.Icon(ft.Icons.NOTIFICATIONS)),
    ]))
ft.run(main)
'''
        }
        if name == "Blank app":
            new_code = starter_code("Blank app")
        else:
            new_code = templates[name]
        if not state["folder"]:
            create_project()
            notify("Create a project first, then choose the template again.")
            return
        state["code"] = new_code
        editor.value = new_code
        save(False)
        show_tab(3)
        notify(f"{name} template loaded.")

    def make_page(title, controls):
        return ft.Column([ft.Text(title, size=23, weight=ft.FontWeight.BOLD), *controls],
                         expand=True, spacing=12)

    def stat_card(title, value, icon):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.TEAL_200, size=22),
                ft.Column([ft.Text(value, size=19, weight=ft.FontWeight.BOLD),
                           ft.Text(title, size=11, color=ft.Colors.GREY_400)], spacing=1)
            ], spacing=10),
            padding=12, border_radius=14, expand=True,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE)
        )

    def quick_action(title, icon, tab):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=ft.Colors.TEAL_200, size=22),
                ft.Text(title, size=10, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=7),
            padding=12, border_radius=14, expand=True,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            on_click=lambda e: show_tab(tab)
        )

    home_page = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("Flet Studio", size=27, weight=ft.FontWeight.BOLD),
                        ft.Text("Build apps from your phone", size=12, color=ft.Colors.GREY_300)
                    ], expand=True),
                    ft.Icon(ft.Icons.TERMINAL, size=28, color=ft.Colors.TEAL_200)
                ]),
                ft.Button("＋  Create new project", on_click=create_project, expand=True)
            ], spacing=14),
            padding=18, border_radius=20,
            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.TEAL)
        ),
        ft.Text("Workspace", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([stat_card("Projects", str(len(list(PROJECTS_DIR.iterdir()))), ft.Icons.FOLDER_CODE),
                stat_card("Flet version", "1.1.2", ft.Icons.PYTHON)], spacing=10),
        ft.Text("Quick actions", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([
            quick_action("Designer", ft.Icons.DASHBOARD_CUSTOMIZE, 2),
            quick_action("Code editor", ft.Icons.CODE, 3),
            quick_action("Templates", ft.Icons.WIDGETS, 6)
        ], spacing=8),
        ft.Row([ft.Text("Recent projects", size=18, weight=ft.FontWeight.BOLD, expand=True),
                ft.TextButton("See all", on_click=lambda e: show_tab(1))]),
        projects_list
    ], expand=True, spacing=14, scroll=ft.ScrollMode.AUTO)

    projects_page = make_page("Projects", [
        ft.Text("Your Flet applications", size=12, color=ft.Colors.GREY_500),
        ft.Row([ft.Container(expand=True), ft.Button("New project", icon=ft.Icons.ADD,
                                                       on_click=create_project)]),
        projects_list
    ])

    palette = ft.Row([
        ft.OutlinedButton(kind, on_click=lambda e, k=kind: add_component(k))
        for kind in ["Text", "Button", "Container", "Image", "Row", "Column"]
    ], wrap=True, spacing=6, run_spacing=6)

    designer_page = make_page("UI Designer", [
        ft.Text("Add components to your layout", size=12, color=ft.Colors.GREY_500),
        ft.Text("Components", weight=ft.FontWeight.BOLD),
        palette,
        ft.Divider(),
        ft.Row([ft.Text("Design canvas", weight=ft.FontWeight.BOLD, expand=True),
                ft.TextButton("Clear", on_click=lambda e: (state["items"].clear(), render_canvas()))]),
        designer_canvas,
        ft.Button("Generate Python code", icon=ft.Icons.CODE, on_click=generate_code)
    ])

    code_page = make_page("Python Editor", [
        project_label,
        editor,
        ft.Row([
            ft.OutlinedButton("Save", icon=ft.Icons.SAVE, on_click=save_code, expand=True),
            ft.Button("Preview", icon=ft.Icons.PLAY_ARROW, on_click=run_preview, expand=True)
        ])
    ])

    preview_page = make_page("Live Preview", [
        ft.Text("Phone-sized mock preview", size=12, color=ft.Colors.GREY_500),
        preview_area,
        ft.OutlinedButton("Refresh", icon=ft.Icons.REFRESH,
                          on_click=lambda e: (refresh_preview(), page.update()))
    ])

    export_page = make_page("Export & Build", [
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ANDROID, size=34, color=ft.Colors.GREEN_300),
                ft.Text("Android APK", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Prepare source files and build instructions.", size=11,
                        color=ft.Colors.GREY_400),
                ft.Button("Prepare export", icon=ft.Icons.PACKAGE, on_click=export_project)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=18, border_radius=16,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE)
        ),
        ft.Text("Build output", weight=ft.FontWeight.BOLD),
        export_output,
        ft.OutlinedButton("Copy instructions", icon=ft.Icons.COPY, on_click=copy_export)
    ])

    templates = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.TEAL_200, size=24),
                ft.Column([ft.Text(name, weight=ft.FontWeight.BOLD),
                           ft.Text(desc, size=11, color=ft.Colors.GREY_500)], expand=True, spacing=3),
                ft.Button("Use", on_click=lambda e, n=name: use_template(n))
            ]),
            padding=12, border_radius=14,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
        )
        for name, desc, icon in [
            ("Blank app", "Clean Flet starter", ft.Icons.APP_SHORTCUT),
            ("Counter app", "Interactive counter", ft.Icons.EXPOSURE_PLUS_1),
            ("Profile UI", "Profile card layout", ft.Icons.PERSON),
            ("Dashboard", "Cards and statistics", ft.Icons.DASHBOARD)
        ]
    ], spacing=8)
    templates_page = make_page("Templates", [
        ft.Text("Start with a ready-made example.", size=12, color=ft.Colors.GREY_500),
        templates
    ])

    settings_page = make_page("Settings", [
        ft.Container(
            content=ft.Column([
                ft.ListTile(leading=ft.Icon(ft.Icons.INFO_OUTLINE), title=ft.Text("Flet Studio"),
                            subtitle=ft.Text("Version 1.0.0")),
                ft.ListTile(leading=ft.Icon(ft.Icons.PYTHON), title=ft.Text("Target Flet version"),
                            subtitle=ft.Text("1.1.2")),
                ft.ListTile(leading=ft.Icon(ft.Icons.PHONE_ANDROID), title=ft.Text("Designed for"),
                            subtitle=ft.Text("Android phones and tablets")),
                ft.ListTile(leading=ft.Icon(ft.Icons.FOLDER), title=ft.Text("Workspace"),
                            subtitle=ft.Text(str(PROJECTS_DIR)))
            ]),
            border_radius=16, bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
        ),
        ft.Text("The visual preview is a mockup. Run the generated main.py to execute the app.",
                size=11, color=ft.Colors.GREY_500)
    ])

    pages = [home_page, projects_page, designer_page, code_page, preview_page,
             export_page, templates_page, settings_page]

    def nav_item(icon, label, index):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=19, color=ft.Colors.GREY_400),
                ft.Text(label, size=9, color=ft.Colors.GREY_400)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
            padding=7, border_radius=12, expand=True,
            on_click=lambda e: show_tab(index)
        )

    nav = ft.Row([
        nav_item(ft.Icons.HOME_ROUNDED, "Home", 0),
        nav_item(ft.Icons.FOLDER_COPY, "Projects", 1),
        nav_item(ft.Icons.DASHBOARD_CUSTOMIZE, "Design", 2),
        nav_item(ft.Icons.CODE, "Code", 3),
        nav_item(ft.Icons.MORE_HORIZ, "More", 7)
    ], spacing=2)

    def show_tab(index):
        state["tab"] = index
        for i, item in enumerate(nav.controls):
            active = i == index or (i == 4 and index in [5, 6, 7])
            item.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.TEAL) if active else None
            item.content.controls[0].color = ft.Colors.TEAL_200 if active else ft.Colors.GREY_400
            item.content.controls[1].color = ft.Colors.TEAL_200 if active else ft.Colors.GREY_400
        body.content = pages[index]
        page.update()

    header = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Container(content=ft.Icon(ft.Icons.TERMINAL, color=ft.Colors.TEAL_200),
                             padding=8, border_radius=10,
                             bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.TEAL)),
                ft.Text("Flet Studio", size=17, weight=ft.FontWeight.BOLD)
            ], spacing=8, expand=True),
            ft.IconButton(ft.Icons.WIDGETS_OUTLINED, tooltip="Templates",
                          on_click=lambda e: show_tab(6)),
            ft.IconButton(ft.Icons.SETTINGS_OUTLINED, tooltip="Settings",
                          on_click=lambda e: show_tab(7))
        ]),
        padding=ft.Padding(left=14, right=8, top=6, bottom=6)
    )
    footer = ft.Container(
        content=nav, padding=ft.Padding(left=7, right=7, top=5, bottom=7),
        bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
        border=ft.Border(top=ft.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)))
    )

    page.add(ft.Column([
        header,
        ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
        body,
        footer
    ], spacing=0, expand=True))

    refresh_projects()
    refresh_preview()
    render_canvas()
    show_tab(0)


ft.run(main)

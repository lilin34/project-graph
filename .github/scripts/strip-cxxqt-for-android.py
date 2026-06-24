#!/usr/bin/env python3
"""Strip platform-specific deps for Android cross-compile."""
import os, re

def strip_cargo_toml():
    path = "app/src-tauri/Cargo.toml"
    with open(path) as f:
        src = f.read()
    src = re.sub(
        r'[target.\'cfg\(not\(target_os = "android"\)\)\'.build-dependencies].*?(?=
\[|\Z)',
        "", src, flags=re.DOTALL
    )
    src = re.sub(
        r'[target.\'cfg\(target_os = "linux"\)\'.dependencies].*?(?=
\[|\Z)',
        "", src, flags=re.DOTALL
    )
    src = re.sub(r"^tauri-plugin-system-info.*\n?", "", src, flags=re.MULTILINE)
    with open(path, "w") as f:
        f.write(src)
    if os.path.exists("app/src-tauri/Cargo.lock"):
        os.remove("app/src-tauri/Cargo.lock")
    print("Cargo.toml ready")

def strip_build_rs():
    path = "app/src-tauri/build.rs"
    with open(path) as f:
        src = f.read()
    src = re.sub(
        r"#\\[cfg\\(not\\(target_os = \"android\"\\)\\)\\]\\s*\\{.*?\\n\\s*\\}",
        "/* cxx-qt stripped for Android */",
        src, flags=re.DOTALL
    )
    with open(path, "w") as f:
        f.write(src)
    print("build.rs ready")

def strip_lib_rs():
    path = "app/src-tauri/src/lib.rs"
    with open(path) as f:
        src = f.read()
    src = re.sub(r"^\\s*tauri_plugin_system_info.*\\n?", "", src, flags=re.MULTILINE)
    with open(path, "w") as f:
        f.write(src)
    print("lib.rs ready")

def strip_capabilities():
    path = "app/src-tauri/capabilities/default.json"
    if os.path.exists(path):
        with open(path) as f:
            src = f.read()
        src = re.sub(r'\\s*"system-info:allow-all",?\\n?', "", src)
        with open(path, "w") as f:
            f.write(src)
        print("capabilities ready")

def cleanup():
    for fn in ["app/src-tauri/src/qt_app.cpp",
               "app/src-tauri/src/qt_app.h",
               "app/src-tauri/src/ipc_bridge.rs"]:
        if os.path.exists(fn):
            os.remove(fn)
    print("qt/ipc files removed")

if __name__ == "__main__":
    strip_cargo_toml()
    strip_build_rs()
    strip_lib_rs()
    strip_capabilities()
    cleanup()

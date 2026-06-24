#!/usr/bin/env python3
"""Strip platform deps for Android cross-compile. v11 - fix lib.rs regex"""
import os, re

def strip_cargo_toml():
    p = "app/src-tauri/Cargo.toml"
    with open(p) as f: src = f.read()
    src = re.sub(r"""\[target\.'cfg\(target_os = "linux"\)'\.build-dependencies\].*?(?=\n\[|\Z)""",
                 "", src, flags=re.DOTALL)
    src = re.sub(r"""\[target\.'cfg\(target_os = "linux"\)'\.dependencies\].*?(?=\n\[|\Z)""",
                 "", src, flags=re.DOTALL)
    src = re.sub(r'^.*tauri-plugin-system-info.*\n?', "", src, flags=re.MULTILINE)
    with open(p, "w") as f: f.write(src)
    for lk in ["app/src-tauri/Cargo.lock"]:
        if os.path.exists(lk): os.remove(lk)
    print("Cargo.toml ready")

def strip_build_rs():
    with open("app/src-tauri/build.rs", "w") as f:
        f.write("fn main() { tauri_build::build(); }\n")
    print("build.rs ready")

def strip_lib_rs():
    p = "app/src-tauri/src/lib.rs"
    with open(p) as f: src = f.read()
    # Remove ANY line containing tauri_plugin_system_info (not just lines starting with it)
    src = re.sub(r'^.*tauri_plugin_system_info.*\n?', "", src, flags=re.MULTILINE)
    with open(p, "w") as f: f.write(src)
    print("lib.rs ready")

def strip_capabilities():
    p = "app/src-tauri/capabilities/default.json"
    if not os.path.exists(p): return
    with open(p) as f: src = f.read()
    src = re.sub(r'\s*"system-info:allow-all",?\n?', "", src)
    with open(p, "w") as f: f.write(src)
    print("capabilities ready")

def cleanup():
    for f in ["app/src-tauri/src/qt_app.cpp","app/src-tauri/src/qt_app.h","app/src-tauri/src/ipc_bridge.rs"]:
        if os.path.exists(f): os.remove(f)
    print("qt/ipc files removed")

if __name__ == "__main__":
    strip_cargo_toml()
    strip_build_rs()
    strip_lib_rs()
    strip_capabilities()
    cleanup()

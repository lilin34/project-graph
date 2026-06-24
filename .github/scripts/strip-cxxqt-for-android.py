#!/usr/bin/env python3
"""v12: Strip ALL target-specific deps + cfg-gate paddle module for Android build.

Changes:
  Cargo.toml:
    - Remove ALL [target.'cfg(...)'.dependencies] sections
    - Remove ALL [target.'cfg(...)'.build-dependencies] sections
    - Strip tauri-plugin-system-info from regular deps
  lib.rs:
    - Strip tauri_plugin_system_info references
    - Strip cmd::paddle::* entries from invoke_handler
  cmd/mod.rs:
    - Add #[cfg(not(target_os = "android"))] to pub mod paddle;
  build.rs: replace with minimal version
  capabilities: strip system-info permissions
  cleanup: remove qt/cxx-qt source files + Cargo.lock
"""
import os, re

def strip_cargo_toml():
    p = "app/src-tauri/Cargo.toml"
    with open(p) as f: src = f.read()
    # Remove ALL target-specific build-dependencies sections
    src = re.sub(r"""\[target\.'cfg\([^)]+\)'\.build-dependencies\].*?(?=\n\[|\Z)""",
                 "", src, flags=re.DOTALL)
    # Remove ALL target-specific dependencies sections
    src = re.sub(r"""\[target\.'cfg\([^)]+\)'\.dependencies\].*?(?=\n\[|\Z)""",
                 "", src, flags=re.DOTALL)
    # Strip tauri-plugin-system-info from regular deps
    src = re.sub(r'^.*tauri-plugin-system-info.*\n?', "", src, flags=re.MULTILINE)
    # Clean up blank lines (max 1 consecutive)
    src = re.sub(r'\n{3,}', '\n\n', src)
    with open(p, "w") as f: f.write(src.strip() + '\n')
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
    # Strip tauri_plugin_system_info line (any position in line)
    src = re.sub(r'^.*tauri_plugin_system_info.*\n?', "", src, flags=re.MULTILINE)
    # Strip cmd::paddle::* entries from invoke_handler
    src = re.sub(r'^.*cmd::paddle::.*\n?', "", src, flags=re.MULTILINE)
    with open(p, "w") as f: f.write(src)
    print("lib.rs ready")

def strip_mod_rs():
    p = "app/src-tauri/src/cmd/mod.rs"
    with open(p) as f: src = f.read()
    # Add cfg gate before pub mod paddle
    src = re.sub(
        r'^(pub mod paddle;)',
        r'#[cfg(not(target_os = "android"))]\n\1',
        src, count=1, flags=re.MULTILINE
    )
    with open(p, "w") as f: f.write(src)
    print("cmd/mod.rs ready")

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
    strip_mod_rs()
    strip_capabilities()
    cleanup()

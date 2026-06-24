#!/usr/bin/env python3
import os
def strip_cargo_toml():
    p = "app/src-tauri/Cargo.toml"
    with open(p) as f: lines = f.readlines()
    out, skip_bd, skip_ld = [], False, False
    for line in lines:
        if 'build-dependencies' in line and 'not(target_os = "android")' in line: skip_bd = True; continue
        if 'dependencies' in line and 'target_os = "linux"' in line: skip_ld = True; continue
        if line.strip().startswith('['): skip_bd, skip_ld = False, False
        elif 'tauri-plugin-system-info' in line: continue
        if not skip_bd and not skip_ld: out.append(line)
    with open(p, 'w') as f: f.writelines(out)
    if os.path.exists('app/src-tauri/Cargo.lock'): os.remove('app/src-tauri/Cargo.lock')
    print('Cargo.toml ready')
def strip_build_rs():
    with open('app/src-tauri/build.rs', 'w') as f: f.write('fn main() { tauri_build::build(); }
')
    print('build.rs ready')
def strip_lib_rs():
    import re
    with open('app/src-tauri/src/lib.rs') as f: src = f.read()
    src = re.sub(r'^\s*tauri_plugin_system_info.*\n?', '', src, flags=re.MULTILINE)
    with open('app/src-tauri/src/lib.rs', 'w') as f: f.write(src)
    print('lib.rs ready')
def strip_capabilities():
    import re
    p = 'app/src-tauri/capabilities/default.json'
    if not os.path.exists(p): return
    with open(p) as f: src = f.read()
    src = re.sub(r'\s*"system-info:allow-all",?\n?', '', src)
    with open(p, 'w') as f: f.write(src)
    print('capabilities ready')
def cleanup():
    for f in ['app/src-tauri/src/qt_app.cpp','app/src-tauri/src/qt_app.h','app/src-tauri/src/ipc_bridge.rs']:
        if os.path.exists(f): os.remove(f)
    print('qt/ipc files removed')
if __name__ == '__main__':
    strip_cargo_toml(); strip_build_rs(); strip_lib_rs(); strip_capabilities(); cleanup()

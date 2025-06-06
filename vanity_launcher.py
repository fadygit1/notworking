MSBuild.exe VanitySearch.sln /p:Configuration=Release /p:Platform=x64"""
VanitySearch Command Builder
============================
Interactive TK-based GUI (falls back to CLI) to let a user choose *all* relevant
VanitySearch parameters then generate a ready-to-copy PowerShell command.

Run:
    python vanity_launcher.py        # GUI
    python vanity_launcher.py --cli  # text prompts

Dependencies: only stdlib (tkinter, argparse, textwrap, shutil). Clipboard copy
uses tkinter itself, no extra packages required.
"""

from __future__ import annotations
import argparse, sys, textwrap, shutil, os, subprocess, re
from tkinter import Tk, Label, Entry, Button, Checkbutton, Radiobutton, IntVar, StringVar, filedialog, END, W, E

# ---------- const helpers ----------

def is_hex(s: str) -> bool:
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def hex64(s: str) -> str:
    """Return s as 64-char hex (pad left) or raise ValueError."""
    s = s.lower().lstrip("0x").rjust(64, "0")
    if len(s) != 64 or not is_hex(s):
        raise ValueError("Hex value must be <= 64 chars")
    return s


def hex_validate(s: str):
    if not all(c in '0123456789abcdefABCDEF' for c in s):
        raise ValueError('HEX غير صالح!')


# ---------- core builder ----------

def build_command(opts: dict[str, str | bool | list[str]]) -> str:
    parts = [r".\x64\Release\VanitySearch.exe"]

    # keyspace
    start_hex = hex64(opts["start"])
    end_hex = hex64(opts["end"])
    # diff = end-start as hex (positive)
    diff = int(end_hex, 16) - int(start_hex, 16)
    if diff <= 0:
        raise ValueError("End key must be greater than start key")
    diff_hex = f"{diff:X}"
    parts.append(f"--keyspace {start_hex.lstrip('0') or '0'}:+{diff_hex}")

    # search mode
    mode = opts["mode"]
    if mode == "u":
        parts.append("-u")
    elif mode == "b":
        parts.append("-b")
    # compressed default needs no flag

    # threads / gpu
    if opts["gpu"]:
        parts.append("-gpu")
        if opts.get("gpuId"):
            parts.extend(["-gpuId", ",".join(opts["gpuId"])])
    if opts.get("threads"):
        parts.extend(["-t", str(opts["threads"])])

    # grid size
    if opts.get("grid"):
        parts.extend(["-g", opts["grid"]])

    # repeat limits
    r_flags = []
    for idx, val in enumerate(opts.get("repeat", []), 1):
        if val is not None:
            r_flags.extend([f"-r{idx}", str(val)])
    parts.extend(r_flags)

    # input / output files
    if opts.get("infile"):
        parts.extend(["-i", opts["infile"]])
    if opts.get("outfile"):
        parts.extend(["-o", opts["outfile"]])

    # resume
    if opts.get("resume"):
        parts.extend(["--resume", opts["resume"]])

    if opts.get("stop"):
        parts.append("-stop")
    if opts.get("stop_all"):
        parts.append("-stopAll")

    cmd = "`\n    ".join(parts)  # PowerShell multiline with backtick
    return cmd


# ---------- CLI fallback ----------

def run_cli():
    print("VanitySearch command builder (CLI)\n——————————————")
    start = input("Start key (hex 64chars, 0x.. optional): ").strip()
    end = input("End   key (hex 64chars): ").strip()
    mode = input("Search mode [c]ompressed/[u]ncompressed/[b]oth (default c): ").strip().lower() or "c"
    gpu = input("Enable GPU? (Y/n): ").strip().lower() != "n"
    gpu_ids = []
    if gpu:
        ids = input("GPU id(s) comma-sep (blank=0): ").strip()
        if ids:
            gpu_ids = [x.strip() for x in ids.split(",")]
    threads = input("CPU threads (blank=all): ").strip()
    grid = input("Grid size -g (e.g 2048x256, blank skip): ").strip()
    repeat = input("Repeat limits r1..r5 comma (blank skip): ").strip()
    infile = input("Addresses file path (blank addresses.txt): ").strip() or "addresses.txt"
    outfile = input("Output   file path (blank results.txt): ").strip() or "results.txt"
    resume = input("Resume from file (blank skip): ").strip()
    stop = input("Add -stop flag? (y/N): ").strip().lower() == "y"
    stop_all = input("Add -stopAll flag? (y/N): ").strip().lower() == "y"

    opts = {
        "start": start,
        "end": end,
        "mode": mode,
        "gpu": gpu,
        "gpuId": gpu_ids,
        "threads": int(threads) if threads else None,
        "grid": grid or None,
        "repeat": [int(x) if x else None for x in (repeat.split(",")+["","","","",""])[:5]] if repeat else [],
        "infile": infile,
        "outfile": outfile,
        "resume": resume or None,
        "stop": stop,
        "stop_all": stop_all,
    }
    try:
        hex_validate(opts["start"])
        hex_validate(opts["end"])
        cmd = build_command(opts)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
    with open("cmd_generated.txt", "w", encoding="utf-8") as f:
        f.write(cmd)
    print("\nGenerated command (also saved to cmd_generated.txt):\n")
    print(cmd)


# ---------- simple GUI ----------

def run_gui():
    root = Tk()
    root.title("VanitySearch Command Builder")

    var_start = StringVar()
    var_end = StringVar()
    var_mode = StringVar(value="c")
    var_gpu = IntVar(value=1)
    var_gpu_ids = StringVar(value="0")
    var_threads = StringVar()
    var_grid = StringVar()
    var_repeat = StringVar()
    var_in = StringVar(value="addresses.txt")
    var_out = StringVar(value="results.txt")
    var_resume = StringVar()
    var_stop = IntVar()
    var_stop_all = IntVar()

    def row(lbl, widget, r):
        Label(root, text=lbl).grid(row=r, column=0, sticky=W, padx=4, pady=2)
        widget.grid(row=r, column=1, sticky=E+W, padx=4, pady=2)

    row("Start key (hex)", Entry(root, textvariable=var_start, width=70), 0)
    row("End key (hex)", Entry(root, textvariable=var_end, width=70), 1)

    Label(root, text="Search mode").grid(row=2, column=0, sticky=W, padx=4)
    Radiobutton(root, text="Compressed", variable=var_mode, value="c").grid(row=2, column=1, sticky=W)
    Radiobutton(root, text="Uncompressed", variable=var_mode, value="u").grid(row=2, column=1)
    Radiobutton(root, text="Both", variable=var_mode, value="b").grid(row=2, column=1, sticky=E)

    row("Enable GPU", Checkbutton(root, variable=var_gpu), 3)
    row("GPU id(s)", Entry(root, textvariable=var_gpu_ids), 4)
    Button(root, text="Detect GPUs", command=lambda: detect_gpu(var_gpu_ids)).grid(row=3, column=2)
    row("CPU threads", Entry(root, textvariable=var_threads), 5)
    row("Grid size -g", Entry(root, textvariable=var_grid), 6)
    row("Repeat limits r1..r5", Entry(root, textvariable=var_repeat), 7)
    row("Addresses file", Entry(root, textvariable=var_in), 8)
    Button(root, text="…", command=lambda: var_in.set(filedialog.askopenfilename())).grid(row=8, column=2)
    row("Output file", Entry(root, textvariable=var_out), 9)
    Button(root, text="…", command=lambda: var_out.set(filedialog.askopenfilename())).grid(row=9, column=2)
    row("Resume file", Entry(root, textvariable=var_resume, width=60), 10)
    Button(root, text="…", command=lambda: var_resume.set(filedialog.askopenfilename())).grid(row=10, column=2)
    row("Add -stop", Checkbutton(root, variable=var_stop), 11)
    row("Add -stopAll", Checkbutton(root, variable=var_stop_all), 12)

    txt_result = Entry(root, width=100)
    txt_result.grid(row=14, column=0, columnspan=3, padx=4, pady=8, sticky=E+W)

    def detect_gpu(var_field):
        try:
            out = subprocess.check_output([r".\x64\Release\VanitySearch.exe", "-l"], stderr=subprocess.STDOUT, text=True, timeout=10)
            ids = re.findall(r"Device\s+(\d+):", out)
            if ids:
                var_field.set(",".join(ids))
        except Exception as e:
            print("GPU detect error", e)

    def generate():
        opts = {
            "start": var_start.get(),
            "end": var_end.get(),
            "mode": var_mode.get(),
            "gpu": bool(var_gpu.get()),
            "gpuId": [x.strip() for x in var_gpu_ids.get().split(",") if x.strip()],
            "threads": int(var_threads.get()) if var_threads.get() else None,
            "grid": var_grid.get() or None,
            "repeat": [int(x) if x else None for x in (var_repeat.get().split(",")+["","","","",""])[:5]] if var_repeat.get() else [],
            "infile": var_in.get(),
            "outfile": var_out.get(),
            "resume": var_resume.get() or None,
            "stop": bool(var_stop.get()),
            "stop_all": bool(var_stop_all.get()),
        }
        try:
            hex_validate(opts["start"])
            hex_validate(opts["end"])
            cmd = build_command(opts)
        except Exception as e:
            txt_result.delete(0, END)
            txt_result.insert(0, f"Error: {e}")
            return
        txt_result.delete(0, END)
        txt_result.insert(0, cmd)
        # copy to clipboard
        root.clipboard_clear(); root.clipboard_append(cmd)

    Button(root, text="Generate", command=generate).grid(row=13, column=0, columnspan=3, pady=4)

    root.mainloop()


# ---------- entry ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VanitySearch command builder GUI/CLI")
    parser.add_argument("--cli", action="store_true", help="use text mode prompts")
    args = parser.parse_args()

    if args.cli or (shutil.which("pythonw.exe") and os.environ.get("DISPLAY") is None):
        run_cli()
    else:
        run_gui()

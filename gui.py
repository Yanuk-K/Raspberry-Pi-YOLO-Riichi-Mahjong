import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Optional, Tuple

try:
    from ultralytics import YOLO  # type: ignore
except Exception:  # pragma: no cover - ultralytics might be missing at runtime
    YOLO = None

try:
    from yolo_grab import YoloGrab
except Exception:  # pragma: no cover
    YoloGrab = None

from Mahjong_rules.Yaku.utils import HandContext, Meld, Tile, parse_tiles
from Mahjong_rules.score_calc import calculate_final_score


class MahjongApp:
    PLAYER_NAMES = ["Player", "Right Player", "Top Player", "Left Player"]
    ROUND_NAMES = ["East", "South", "West", "North"]
    ROUND_LETTERS = ["E", "S", "W", "N"]
    YOLO_DEFAULT_PATHS = [
        os.path.join("Tools", "best.pt"),
        os.path.join("best_ncnn_model", "best_ncnn_model", "model.ncnn.bin"),
        os.path.join("best_ncnn_model", "best_ncnn_model", "model.ncnn.param"),
    ]

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.geometry("780x560")
        self.master.minsize(720, 520)
        self.master.title("Mahjong Score Calculator")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.player_count = 4
        self.initial_score = 25000
        self.scores: List[int] = [self.initial_score] * self.player_count
        self.oya = 0
        self.bakaze_index = 0
        self.honba = 0
        self.kyoutaku = 0
        self.hand_counter = 1
        self.game_log: List[Tuple[str, List[int]]] = []

        self.yolo_model = None
        self.yolo_available = False
        self.yolo_status_var = tk.StringVar()
        self.yolo_live_process: Optional[subprocess.Popen] = None

        self.load_yolo_model()
        self.start()

    # ---------- YOLO helpers ----------
    def load_yolo_model(self) -> None:
        if YOLO is None:
            self.yolo_available = False
            self.yolo_model = None
            self.yolo_status_var.set("YOLO unavailable (ultralytics not installed)")
            return

        for path in self.YOLO_DEFAULT_PATHS:
            if not os.path.exists(path):
                continue
            try:
                self.yolo_model = YOLO(path)
                self.yolo_available = True
                self.yolo_status_var.set(f"YOLO ready ({os.path.basename(path)})")
                return
            except Exception:
                continue

        self.yolo_available = False
        self.yolo_model = None
        self.yolo_status_var.set("YOLO model not found")

    def reload_yolo(self) -> None:
        self.load_yolo_model()
        messagebox.showinfo("YOLO", self.yolo_status_var.get())

    def launch_live_camera(self) -> None:
        if self.yolo_live_process and self.yolo_live_process.poll() is None:
            messagebox.showinfo("YOLO", "Live camera already running.")
            return
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolo_text.py")
        if not os.path.exists(script_path):
            messagebox.showerror("YOLO", "yolo_text.py not found.")
            return
        try:
            self.yolo_live_process = subprocess.Popen([sys.executable, script_path])
            messagebox.showinfo("YOLO", "Live detection started.\nPress 'q' in the camera window to stop.")
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("YOLO", f"Failed to start live detection: {exc}")

    def stop_live_camera(self) -> None:
        if self.yolo_live_process and self.yolo_live_process.poll() is None:
            try:
                self.yolo_live_process.terminate()
                self.yolo_live_process.wait(timeout=2)
            except Exception:
                self.yolo_live_process.kill()
        self.yolo_live_process = None

    def capture_tiles_via_camera(self) -> List[str]:
        if not self.yolo_available or self.yolo_model is None or YoloGrab is None:
            messagebox.showerror("YOLO", "Camera capture unavailable.")
            return []
        try:
            grabber = YoloGrab(tk, self.yolo_model)
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("YOLO", f"Unable to initialise camera: {exc}")
            return []

        tokens: List[str] = []
        try:
            time.sleep(0.2)  # give picamera a moment
            frame = grabber.picam2.capture_array()
            results = grabber.model(frame)
            tokens = self.extract_tiles_from_results(results)
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("YOLO", f"Capture failed: {exc}")
        finally:
            try:
                grabber.on_closing()
            except Exception:
                pass

        if not tokens:
            messagebox.showinfo("YOLO", "No tiles detected.")
        return tokens

    @staticmethod
    def extract_tiles_from_results(results) -> List[str]:
        tokens: List[str] = []
        if not results:
            return tokens
        result = results[0]
        boxes = getattr(result, "boxes", None)
        if boxes is None:
            return tokens

        names = getattr(result, "names", {}) or {}
        if isinstance(names, list):
            name_lookup = {idx: label for idx, label in enumerate(names)}
        else:
            name_lookup = names

        cls_values = boxes.cls.tolist() if hasattr(boxes.cls, "tolist") else list(boxes.cls)
        xyxy = boxes.xyxy.tolist() if hasattr(boxes, "xyxy") else []
        order = list(range(len(cls_values)))
        if xyxy:
            order.sort(key=lambda idx: xyxy[idx][0])

        for idx in order:
            cls_id = int(cls_values[idx])
            label = name_lookup.get(cls_id)
            if not label:
                continue
            tokens.append(str(label).strip())
        return tokens

    # ---------- UI setup ----------
    def start(self) -> None:
        self.clear_screen()
        start_frame = tk.Frame(self.master, padx=20, pady=20)
        start_frame.pack(expand=True)

        tk.Label(start_frame, text="Mahjong Score Calculator", font=("Arial", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        tk.Label(start_frame, text="Initial score:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.initial_score_var = tk.StringVar(value="25000")
        tk.Entry(start_frame, textvariable=self.initial_score_var, width=10).grid(
            row=1, column=1, sticky=tk.W
        )

        tk.Label(start_frame, text="Number of players:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.player_count_var = tk.IntVar(value=4)
        ttk.Combobox(
            start_frame, textvariable=self.player_count_var, values=[3, 4], width=3, state="readonly"
        ).grid(row=2, column=1, sticky=tk.W)

        tk.Label(start_frame, text="Select dealer (Oya):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.oya_var = tk.IntVar(value=0)
        oya_frame = tk.Frame(start_frame)
        oya_frame.grid(row=3, column=1, sticky=tk.W)
        for idx, name in enumerate(self.PLAYER_NAMES):
            tk.Radiobutton(oya_frame, text=name, variable=self.oya_var, value=idx).pack(anchor=tk.W)

        tk.Label(start_frame, text="Round wind (0=E, 1=S, 2=W, 3=N):").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.round_var = tk.IntVar(value=0)
        ttk.Combobox(
            start_frame, textvariable=self.round_var, values=list(range(4)), width=3, state="readonly"
        ).grid(row=4, column=1, sticky=tk.W)

        tk.Button(start_frame, text="Start Game", command=self.init_params, width=18).grid(
            row=5, column=0, columnspan=2, pady=15
        )

    def init_params(self) -> None:
        try:
            self.initial_score = int(self.initial_score_var.get())
            if self.initial_score <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid score", "Initial score must be a positive number.")
            return

        player_count = self.player_count_var.get()
        if player_count not in (3, 4):
            messagebox.showerror("Invalid selection", "Player count must be 3 or 4.")
            return
        if self.oya_var.get() >= player_count:
            messagebox.showerror("Invalid dealer", "Dealer must be one of the active players.")
            return

        self.player_count = player_count
        self.scores = [self.initial_score] * self.player_count
        self.oya = self.oya_var.get()
        self.bakaze_index = self.round_var.get()
        self.honba = 0
        self.kyoutaku = 0
        self.hand_counter = 1
        self.game_log.clear()

        self.build_main_screen()

    def clear_screen(self) -> None:
        for widget in self.master.winfo_children():
            widget.destroy()

    def build_main_screen(self) -> None:
        self.clear_screen()

        self.main_frame = tk.Frame(self.master, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(self.main_frame)
        header.pack(fill=tk.X)
        tk.Label(header, text="Mahjong Scoreboard", font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        status_frame = tk.Frame(header)
        status_frame.pack(side=tk.RIGHT)
        tk.Label(status_frame, textvariable=self.yolo_status_var, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Button(status_frame, text="Reload YOLO", command=self.reload_yolo, width=12).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(status_frame, text="Live Camera", command=self.launch_live_camera, width=12).pack(
            side=tk.LEFT
        )

        info_frame = tk.Frame(self.main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        self.round_label = tk.Label(info_frame, font=("Arial", 12))
        self.round_label.pack(side=tk.LEFT)
        self.honba_label = tk.Label(info_frame, font=("Arial", 12))
        self.honba_label.pack(side=tk.LEFT, padx=(20, 0))
        self.kyoutaku_label = tk.Label(info_frame, font=("Arial", 12))
        self.kyoutaku_label.pack(side=tk.LEFT, padx=(20, 0))

        board = tk.Frame(self.main_frame, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        board.pack(fill=tk.X, pady=10)
        self.score_labels: List[tk.Label] = []
        self.seat_labels: List[tk.Label] = []
        for idx in range(self.player_count):
            frame = tk.Frame(board, padx=10)
            frame.grid(row=0, column=idx, sticky=tk.N)
            tk.Label(frame, text=self.PLAYER_NAMES[idx], font=("Arial", 12, "bold")).pack()
            seat = tk.Label(frame, font=("Arial", 10))
            seat.pack()
            self.seat_labels.append(seat)
            score = tk.Label(frame, font=("Arial", 12))
            score.pack(pady=5)
            self.score_labels.append(score)

        actions = tk.Frame(self.main_frame)
        actions.pack(fill=tk.X, pady=10)
        tk.Button(actions, text="Record Winning Hand", command=self.open_hand_form, width=20).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(actions, text="Record Draw", command=self.open_draw_form, width=15).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(actions, text="Reset Game", command=self.start, width=12).pack(side=tk.RIGHT, padx=5)

        log_frame = tk.Frame(self.main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        tk.Label(log_frame, text="Hand Log:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        self.log_listbox = tk.Listbox(log_frame, height=12)
        self.log_listbox.pack(fill=tk.BOTH, expand=True)

        self.refresh_ui()

    # ---------- Utility methods ----------
    def refresh_ui(self) -> None:
        round_name = self.ROUND_NAMES[self.bakaze_index]
        oya_name = self.PLAYER_NAMES[self.oya]
        self.round_label.config(
            text=f"Round: {round_name} ({self.ROUND_LETTERS[self.bakaze_index]}) | Dealer: {oya_name}"
        )
        self.honba_label.config(text=f"Honba: {self.honba}")
        self.kyoutaku_label.config(text=f"Riichi sticks: {self.kyoutaku}")

        for idx in range(self.player_count):
            seat_wind = self.get_seat_wind(idx)
            self.seat_labels[idx].config(text=f"Seat Wind: {seat_wind}")
            self.score_labels[idx].config(text=f"{self.scores[idx]:,}")

    def get_seat_wind(self, player_index: int) -> str:
        if self.player_count == 4:
            winds = ["E", "S", "W", "N"]
            return winds[(player_index - self.oya) % 4]
        winds = ["E", "S", "W"]
        return winds[(player_index - self.oya) % 3]

    def advance_round(self) -> None:
        self.oya = (self.oya + 1) % self.player_count
        if self.oya == 0 and self.bakaze_index < len(self.ROUND_NAMES) - 1:
            self.bakaze_index += 1

    @staticmethod
    def parse_tile_entry(text: str) -> List[Tile]:
        tokens = text.replace(",", " ").split()
        return parse_tiles(tokens)

    def parse_melds(self, text: str) -> List[Meld]:
        melds: List[Meld] = []
        chunks = [chunk.strip() for chunk in text.split(";") if chunk.strip()]
        for chunk in chunks:
            parts = chunk.replace(",", " ").split()
            if not parts:
                continue
            kind = parts[0].lower()
            if kind not in {"chi", "pon", "kan", "ankan", "kakan"}:
                raise ValueError(f"Unknown meld type '{kind}'.")
            is_open = True
            tiles: List[str] = []
            for token in parts[1:]:
                low = token.lower()
                if low in {"open", "closed", "concealed"}:
                    is_open = low == "open"
                else:
                    tiles.append(token)
            meld_tiles = tuple(Tile.from_str(t) for t in tiles)
            melds.append(Meld(meld_tiles, kind, is_open=is_open))
        return melds

    def add_log_entry(self, message: str, deltas: List[int]) -> None:
        change_parts = [
            f"{self.PLAYER_NAMES[idx]} {delta:+}" for idx, delta in enumerate(deltas) if delta
        ]
        entry = message
        if change_parts:
            entry = f"{entry} | " + ", ".join(change_parts)
        self.log_listbox.insert(tk.END, entry)
        self.log_listbox.yview(tk.END)
        self.game_log.append((message, deltas))
        self.hand_counter += 1

    # ---------- Hand form ----------
    def open_hand_form(self) -> None:
        self.hand_window = tk.Toplevel(self.master)
        self.hand_window.title("Record Winning Hand")
        self.hand_window.grab_set()

        form = tk.Frame(self.hand_window, padx=10, pady=10)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Winner:").grid(row=0, column=0, sticky=tk.W)
        self.winner_var = tk.IntVar(value=0)
        ttk.Combobox(
            form, textvariable=self.winner_var, values=list(range(self.player_count)), width=5, state="readonly"
        ).grid(row=0, column=1, sticky=tk.W)

        tk.Label(form, text="Win Method:").grid(row=1, column=0, sticky=tk.W)
        self.win_method_var = tk.StringVar(value="ron")
        method_frame = tk.Frame(form)
        method_frame.grid(row=1, column=1, columnspan=2, sticky=tk.W)
        tk.Radiobutton(
            method_frame, text="Ron", variable=self.win_method_var, value="ron", command=self.toggle_loser_state
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            method_frame, text="Tsumo", variable=self.win_method_var, value="tsumo", command=self.toggle_loser_state
        ).pack(side=tk.LEFT)

        tk.Label(form, text="Loser (for Ron):").grid(row=2, column=0, sticky=tk.W)
        self.loser_var = tk.IntVar(value=1 if self.player_count > 1 else 0)
        self.loser_box = ttk.Combobox(
            form, textvariable=self.loser_var, values=list(range(self.player_count)), width=5, state="readonly"
        )
        self.loser_box.grid(row=2, column=1, sticky=tk.W)

        tk.Label(form, text="Concealed tiles:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.concealed_entry = tk.Entry(form, width=50)
        self.concealed_entry.grid(row=3, column=1, sticky=tk.W, pady=(10, 0))
        tk.Button(
            form,
            text="Capture (YOLO)",
            command=lambda: self.capture_tiles_into_entry(self.concealed_entry),
            width=15,
        ).grid(row=3, column=2, padx=5, pady=(10, 0))

        tk.Label(form, text="Melds (e.g. 'pon 1m 1m 1m; chi 2p 3p 4p'):").grid(row=4, column=0, sticky=tk.W)
        self.meld_entry = tk.Entry(form, width=50)
        self.meld_entry.grid(row=4, column=1, sticky=tk.W)
        tk.Button(
            form,
            text="Capture (YOLO)",
            command=lambda: self.capture_tiles_into_entry(self.meld_entry),
            width=15,
        ).grid(row=4, column=2, padx=5)

        tk.Label(form, text="Winning tile:").grid(row=5, column=0, sticky=tk.W)
        self.winning_tile_var = tk.StringVar()
        tk.Entry(form, textvariable=self.winning_tile_var, width=10).grid(row=5, column=1, sticky=tk.W)

        tk.Label(form, text="Wait type (optional):").grid(row=6, column=0, sticky=tk.W)
        self.wait_type_var = tk.StringVar(value="")
        ttk.Combobox(
            form,
            textvariable=self.wait_type_var,
            values=["", "tanki", "shanpon", "ryanmen", "kanchan", "penchan"],
            width=10,
            state="readonly",
        ).grid(row=6, column=1, sticky=tk.W)

        flags_frame = tk.LabelFrame(form, text="Flags", padx=5, pady=5)
        flags_frame.grid(row=7, column=0, columnspan=3, sticky=tk.W + tk.E, pady=10)
        self.flag_vars = {
            "riichi": tk.BooleanVar(value=False),
            "double_riichi": tk.BooleanVar(value=False),
            "ippatsu": tk.BooleanVar(value=False),
            "chankan": tk.BooleanVar(value=False),
            "rinshan": tk.BooleanVar(value=False),
            "haitei": tk.BooleanVar(value=False),
            "houtei": tk.BooleanVar(value=False),
            "nagashi_mangan": tk.BooleanVar(value=False),
        }
        row = col = 0
        for name, var in self.flag_vars.items():
            tk.Checkbutton(flags_frame, text=name.replace("_", " ").title(), variable=var).grid(
                row=row, column=col, sticky=tk.W, padx=5, pady=2
            )
            col += 1
            if col > 2:
                col = 0
                row += 1

        tk.Label(form, text="Blessing:").grid(row=8, column=0, sticky=tk.W)
        self.blessing_var = tk.StringVar(value="")
        ttk.Combobox(
            form, textvariable=self.blessing_var, values=["", "tenho", "chiho", "renho"], width=10, state="readonly"
        ).grid(row=8, column=1, sticky=tk.W)

        tk.Label(form, text="Dora indicators:").grid(row=9, column=0, sticky=tk.W)
        self.dora_entry = tk.Entry(form, width=40)
        self.dora_entry.grid(row=9, column=1, sticky=tk.W)
        tk.Button(
            form,
            text="Capture",
            command=lambda: self.capture_tiles_into_entry(self.dora_entry),
            width=10,
        ).grid(row=9, column=2, padx=5)

        tk.Label(form, text="Kan dora indicators:").grid(row=10, column=0, sticky=tk.W)
        self.kan_dora_entry = tk.Entry(form, width=40)
        self.kan_dora_entry.grid(row=10, column=1, sticky=tk.W)
        tk.Button(
            form,
            text="Capture",
            command=lambda: self.capture_tiles_into_entry(self.kan_dora_entry),
            width=10,
        ).grid(row=10, column=2, padx=5)

        tk.Label(form, text="Ura dora indicators:").grid(row=11, column=0, sticky=tk.W)
        self.ura_dora_entry = tk.Entry(form, width=40)
        self.ura_dora_entry.grid(row=11, column=1, sticky=tk.W)
        tk.Button(
            form,
            text="Capture",
            command=lambda: self.capture_tiles_into_entry(self.ura_dora_entry),
            width=10,
        ).grid(row=11, column=2, padx=5)

        tk.Label(form, text="Kan ura dora indicators:").grid(row=12, column=0, sticky=tk.W)
        self.kan_ura_entry = tk.Entry(form, width=40)
        self.kan_ura_entry.grid(row=12, column=1, sticky=tk.W)
        tk.Button(
            form,
            text="Capture",
            command=lambda: self.capture_tiles_into_entry(self.kan_ura_entry),
            width=10,
        ).grid(row=12, column=2, padx=5)

        tk.Label(form, text="Red tiles:").grid(row=13, column=0, sticky=tk.W)
        self.red_tiles_entry = tk.Entry(form, width=40)
        self.red_tiles_entry.grid(row=13, column=1, sticky=tk.W)
        tk.Button(
            form,
            text="Capture",
            command=lambda: self.capture_tiles_into_entry(self.red_tiles_entry),
            width=10,
        ).grid(row=13, column=2, padx=5)

        tk.Label(form, text="Pei-nuki count:").grid(row=14, column=0, sticky=tk.W)
        self.pei_nuki_var = tk.StringVar(value="0")
        tk.Entry(form, textvariable=self.pei_nuki_var, width=5).grid(row=14, column=1, sticky=tk.W)

        tk.Label(form, text="Extra dora:").grid(row=15, column=0, sticky=tk.W)
        self.extra_dora_var = tk.StringVar(value="0")
        tk.Entry(form, textvariable=self.extra_dora_var, width=5).grid(row=15, column=1, sticky=tk.W)

        self.three_player_var = tk.BooleanVar(value=self.player_count == 3)
        tk.Checkbutton(form, text="Three-player hand", variable=self.three_player_var).grid(
            row=16, column=0, sticky=tk.W, pady=5
        )

        tk.Label(form, text="Riichi declarations:").grid(row=17, column=0, sticky=tk.W, pady=(10, 0))
        self.riichi_flags = []
        riichi_frame = tk.Frame(form)
        riichi_frame.grid(row=17, column=1, columnspan=2, sticky=tk.W, pady=(10, 0))
        for idx in range(self.player_count):
            var = tk.BooleanVar(value=False)
            self.riichi_flags.append(var)
            tk.Checkbutton(riichi_frame, text=self.PLAYER_NAMES[idx], variable=var).pack(anchor=tk.W)

        submit = tk.Frame(form)
        submit.grid(row=18, column=0, columnspan=3, pady=15)
        tk.Button(submit, text="Cancel", command=self.hand_window.destroy, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(submit, text="Record Hand", command=self.submit_hand_form, width=18).pack(side=tk.LEFT, padx=5)

        self.toggle_loser_state()

    def capture_tiles_into_entry(self, entry: tk.Entry) -> None:
        tokens = self.capture_tiles_via_camera()
        if tokens:
            entry.delete(0, tk.END)
            entry.insert(0, " ".join(tokens))

    def toggle_loser_state(self) -> None:
        if self.win_method_var.get() == "ron":
            self.loser_box.configure(state="readonly")
        else:
            self.loser_box.configure(state="disabled")

    def submit_hand_form(self) -> None:
        try:
            winner = self.winner_var.get()
            if winner < 0 or winner >= self.player_count:
                raise ValueError("Winner index out of range.")

            win_method = self.win_method_var.get()
            loser: Optional[int] = None
            if win_method == "ron":
                loser = self.loser_var.get()
                if loser == winner:
                    raise ValueError("Loser cannot be the winner.")
                if loser < 0 or loser >= self.player_count:
                    raise ValueError("Loser index out of range.")

            concealed_tiles = self.parse_tile_entry(self.concealed_entry.get())
            melds = self.parse_melds(self.meld_entry.get())
            winning_tile_str = self.winning_tile_var.get().strip()
            if not winning_tile_str:
                raise ValueError("Winning tile is required.")
            winning_tile = Tile.from_str(winning_tile_str)
            wait_type = self.wait_type_var.get().strip() or None
            pei_nuki_count = int(self.pei_nuki_var.get() or 0)
            extra_dora = int(self.extra_dora_var.get() or 0)

            ctx = HandContext(
                concealed_tiles=concealed_tiles,
                melds=melds,
                winning_tile=winning_tile,
                win_method=win_method,
                seat_wind=self.get_seat_wind(winner),
                round_wind=self.ROUND_LETTERS[self.bakaze_index],
                riichi=self.flag_vars["riichi"].get(),
                double_riichi=self.flag_vars["double_riichi"].get(),
                ippatsu=self.flag_vars["ippatsu"].get(),
                is_chankan=self.flag_vars["chankan"].get(),
                is_rinshan=self.flag_vars["rinshan"].get(),
                is_haitei=self.flag_vars["haitei"].get(),
                is_houtei=self.flag_vars["houtei"].get(),
                nagashi_mangan=self.flag_vars["nagashi_mangan"].get(),
                blessing=self.blessing_var.get() or None,
                dora_indicators=self.parse_tile_entry(self.dora_entry.get()),
                ura_dora_indicators=self.parse_tile_entry(self.ura_dora_entry.get()),
                kan_dora_indicators=self.parse_tile_entry(self.kan_dora_entry.get()),
                kan_ura_dora_indicators=self.parse_tile_entry(self.kan_ura_entry.get()),
                red_five_tiles=self.parse_tile_entry(self.red_tiles_entry.get()),
                pei_nuki_count=pei_nuki_count,
                three_player=self.three_player_var.get(),
                additional_flags={"extra_dora": extra_dora} if extra_dora else {},
                wait_type=wait_type,
            )

            result = calculate_final_score(ctx)
            deltas = self.apply_hand_result(result, ctx, winner, loser)

            han = result["han"]
            fu = result["fu"]
            limit = result.get("limit") or ""
            yaku_names = ", ".join(y["name"] for y in result["yaku"])
            method_text = "tsumo" if win_method == "tsumo" else f"ron on {self.PLAYER_NAMES[loser] if loser is not None else ''}"
            current_round = self.ROUND_NAMES[self.bakaze_index]
            dealer_name = self.PLAYER_NAMES[self.oya]
            description = (
                f"{current_round} Hand {self.hand_counter} (Dealer: {dealer_name}) — "
                f"{self.PLAYER_NAMES[winner]} {method_text}; "
                f"{han} han, {fu} fu{f' ({limit})' if limit else ''}. Yaku: {yaku_names}"
            )
            self.add_log_entry(description, deltas)
            self.refresh_ui()
            self.hand_window.destroy()
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("Error", str(exc))

    def apply_hand_result(
        self,
        result: dict,
        ctx: HandContext,
        winner: int,
        loser: Optional[int],
    ) -> List[int]:
        deltas = [0] * self.player_count

        for idx in range(self.player_count):
            if self.riichi_flags[idx].get():
                deltas[idx] -= 1000
                self.kyoutaku += 1

        points = result["points"]
        kyoutaku_bonus = self.kyoutaku * 1000
        renchan = winner == self.oya

        if "ron" in points:
            if loser is None:
                raise ValueError("Loser must be specified for ron.")
            base = points["ron"]
            honba_bonus = self.honba * 300
            deltas[loser] -= base + honba_bonus
            deltas[winner] += base + honba_bonus + kyoutaku_bonus
            self.kyoutaku = 0
        elif "tsumo" in points:
            tsumo_detail = points["tsumo"]
            opponents = [idx for idx in range(self.player_count) if idx != winner]
            if winner == self.oya:
                base = tsumo_detail.get("non_dealer", 0)
                for opp in opponents:
                    payment = base + self.honba * 100
                    deltas[opp] -= payment
                    deltas[winner] += payment
            else:
                dealer_base = tsumo_detail.get("dealer", 0)
                non_dealer_base = tsumo_detail.get("non_dealer", 0)
                for opp in opponents:
                    if opp == self.oya:
                        payment = dealer_base + self.honba * 100
                    else:
                        payment = non_dealer_base + self.honba * 100
                    deltas[opp] -= payment
                    deltas[winner] += payment
            deltas[winner] += kyoutaku_bonus
            self.kyoutaku = 0
        else:  # pragma: no cover
            raise ValueError("Unable to locate scoring detail in result.")

        for idx in range(self.player_count):
            self.scores[idx] += deltas[idx]

        if renchan:
            self.honba += 1
        else:
            self.honba = 0
            self.advance_round()

        return deltas

    # ---------- Draw handling ----------
    def open_draw_form(self) -> None:
        self.draw_window = tk.Toplevel(self.master)
        self.draw_window.title("Record Draw (Ryuukyoku)")
        self.draw_window.grab_set()

        frame = tk.Frame(self.draw_window, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Tenpai Players:").grid(row=0, column=0, sticky=tk.W)
        self.tenpai_flags = []
        tenpai_frame = tk.Frame(frame)
        tenpai_frame.grid(row=0, column=1, sticky=tk.W)
        for idx in range(self.player_count):
            var = tk.BooleanVar(value=False)
            self.tenpai_flags.append(var)
            tk.Checkbutton(tenpai_frame, text=self.PLAYER_NAMES[idx], variable=var).pack(anchor=tk.W)

        tk.Label(frame, text="Riichi declarations:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.draw_riichi_flags = []
        riichi_frame = tk.Frame(frame)
        riichi_frame.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        for idx in range(self.player_count):
            var = tk.BooleanVar(value=False)
            self.draw_riichi_flags.append(var)
            tk.Checkbutton(riichi_frame, text=self.PLAYER_NAMES[idx], variable=var).pack(anchor=tk.W)

        tk.Button(frame, text="Cancel", command=self.draw_window.destroy, width=12).grid(row=2, column=0, pady=15)
        tk.Button(frame, text="Record Draw", command=self.submit_draw_form, width=18).grid(row=2, column=1, pady=15)

    def submit_draw_form(self) -> None:
        try:
            tenpai = [var.get() for var in self.tenpai_flags]
            tenpai_count = sum(tenpai)
            active = self.player_count
            deltas = [0] * active

            for idx in range(active):
                if self.draw_riichi_flags[idx].get():
                    deltas[idx] -= 1000
                    self.kyoutaku += 1

            if 0 < tenpai_count < active:
                payout_total = 3000
                losers = active - tenpai_count
                per_tenpai = payout_total // tenpai_count
                per_noten = payout_total // losers
                for idx in range(active):
                    if tenpai[idx]:
                        deltas[idx] += per_tenpai
                    else:
                        deltas[idx] -= per_noten

            for idx in range(active):
                self.scores[idx] += deltas[idx]

            current_round = self.ROUND_NAMES[self.bakaze_index]
            dealer_tenpai = tenpai[self.oya]
            if dealer_tenpai:
                self.honba += 1
            else:
                self.honba += 1
                self.advance_round()

            self.add_log_entry(
                f"{current_round} Hand {self.hand_counter} — Draw "
                f"({'Tenpai' if tenpai_count else 'All Noten'})",
                deltas,
            )
            self.refresh_ui()
            self.draw_window.destroy()
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("Error", str(exc))

    # ---------- Shutdown ----------
    def on_close(self) -> None:
        self.stop_live_camera()
        self.master.destroy()


def main() -> None:
    root = tk.Tk()
    app = MahjongApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

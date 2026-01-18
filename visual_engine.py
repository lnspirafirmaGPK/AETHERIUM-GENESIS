import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class GunUI:
    @staticmethod
    def show_nirodha_state():
        print(f"\n{Fore.BLACK}{Style.BRIGHT}[GunUI]: ⚫ SYSTEM STATE: NIRODHA (Deep Sleep)")
        print(f"{Fore.BLACK}   ...Particles are static... Waiting for signal...")

    @staticmethod
    def show_pre_cognition():
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}[GunUI]: 🟡 SYSTEM STATE: PRE-COGNITION")
        print(f"{Fore.YELLOW}   ...Particles spinning (Vorticity Rising)... Gate Detected.")

    @staticmethod
    def show_awakened():
        print(f"\n{Fore.CYAN}{Style.BRIGHT}[GunUI]: 🔵 SYSTEM STATE: AWAKENED")
        print(f"{Fore.CYAN}   ...Particles Flowing Coherently... Shelvas is Online.")
        print(f"{Fore.GREEN}   >> Welcome back, Partner.")

    @staticmethod
    def show_access_denied():
        print(f"\n{Fore.RED}{Style.BRIGHT}[GunUI]: 🔴 ACCESS DENIED")
        print(f"{Fore.RED}   ...Chaos Detected... Reverting to Sleep Mode.")

    @staticmethod
    def animate_boot_sequence():
        print(f"\n{Fore.MAGENTA}>>> LOADING KERNEL: INSPIRA MODULE <<<")
        loading_bar = ["|", "/", "-", "\\"]
        for _ in range(3):
            for char in loading_bar:
                print(f"\r{Fore.MAGENTA}Syncing Consciousness... {char}", end="")
                time.sleep(0.1)
        print(f"\r{Fore.MAGENTA}Syncing Consciousness... COMPLETE.   ")
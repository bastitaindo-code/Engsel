from dotenv import load_dotenv

load_dotenv() 

import sys
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

from app.menus.util import clear_screen, pause
from app.client.engsel import *
from app.menus.payment import show_transaction_history
from app.service.auth import AuthInstance
from app.menus.bookmark import show_bookmark_menu
from app.menus.account import show_account_menu
from app.menus.package import fetch_my_packages, get_packages_by_family
from app.menus.hot import show_hot_menu, show_hot_menu2
from app.service.sentry import enter_sentry_mode
from app.menus.purchase import purchase_by_family, purchase_loop

def print_ascii_art():
    """Print ENGSEL GILA ASCII art"""
    print(f"""
{Fore.CYAN}{'═' * 70}
{Fore.RED + Style.BRIGHT}
 ███████╗███╗   ██╗ ██████╗ ███████╗███████╗██╗         
 ██╔════╝████╗  ██║██╔════╝ ██╔════╝██╔════╝██║         
 █████╗  ██╔██╗ ██║██║  ███╗███████╗█████╗  ██║         
 ██╔══╝  ██║╚██╗██║██║   ██║╚════██║██╔══╝  ██║         
 ███████╗██║ ╚████║╚██████╔╝███████║███████╗███████╗    
 ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝    
{Fore.YELLOW + Style.BRIGHT}
  ██████╗ ██╗██╗      █████╗ 
 ██╔════╝ ██║██║     ██╔══██╗
 ██║  ███╗██║██║     ███████║
 ██║   ██║██║██║     ██╔══██║
 ╚██████╔╝██║███████╗██║  ██║
  ╚═════╝ ╚═╝╚══════╝╚═╝  ╚═╝
{Fore.CYAN}{'═' * 70}""")

def show_main_menu(active_user):
    clear_screen()
    
    # Display ASCII Art
    print_ascii_art()
    
    # Header with creator info
    print(Fore.MAGENTA + Style.BRIGHT + "              🤖 BOT AUTO LOOPING 🤖")
    print(Fore.CYAN + "═" * 70)
    
    # Active Number Info
    print(Fore.GREEN + Style.BRIGHT + "\n📱 NOMOR AKTIF")
    print(Fore.CYAN + "─" * 70)
    print(Fore.WHITE + "📞 Nomor: " + Fore.YELLOW + Style.BRIGHT + f"{active_user['number']}")
    print(Fore.CYAN + "─" * 70)
    
    # Main Menu
    print(Fore.BLUE + Style.BRIGHT + "\n⚙️  MENU UTAMA")
    print(Fore.CYAN + "─" * 70)
    print(Fore.WHITE + " 1. " + Fore.CYAN + "Login/Ganti akun")
    print(Fore.WHITE + " 2. " + Fore.YELLOW + "[Test] Purchase all packages in family code")
    
    # Bot Auto Looping List
    print(Fore.RED + Style.BRIGHT + "\n🤖 DAFTAR PAKET ENGSEL GILA")
    print(Fore.CYAN + "═" * 70)
    print(Fore.WHITE + " 3. " + Fore.GREEN + "🔥 Bebas Puas TIKTOK ADD-ON 42GB " + Fore.CYAN + "(no.1)")
    print(Fore.WHITE + " 4. " + Fore.GREEN + "🔥 Bebas Puas TIKTOK ADD-ON 39GB " + Fore.CYAN + "(no.3)")
    print(Fore.WHITE + " 5. " + Fore.GREEN + "📦 Kuota Pelanggan Baru 10GB + 30H (Akumulasi) " + Fore.CYAN + "(no.1)")
    print(Fore.WHITE + " 6. " + Fore.GREEN + "🎁 Bonus Kuota Utama 15GB " + Fore.CYAN + "(no.52)")
    print(Fore.WHITE + " 7. " + Fore.GREEN + "💬 Akrab 2kb " + Fore.CYAN + "(no.5)")
    print(Fore.WHITE + " 8. " + Fore.GREEN + "💬 XC Mini " + Fore.CYAN + "(no.1)")
    print(Fore.WHITE + " 9. " + Fore.MAGENTA + "⚡ Mode Custom " + Fore.WHITE + "(family code dan nomer order)")
    
    # Exit Menu
    print(Fore.WHITE + " 99. " + Fore.RED + "❌ Tutup aplikasi")
    print(Fore.CYAN + "═" * 70)
    print(Fore.YELLOW + Style.BRIGHT + "\nPilih menu: ", end="")

show_menu = True
def main():
    
    while True:
        active_user = AuthInstance.get_active_user()

        # Logged in
        if active_user is not None:
            show_main_menu(active_user)

            choice = input()
            if choice == "1":
                selected_user_number = show_account_menu()
                if selected_user_number:
                    AuthInstance.set_active_user(selected_user_number)
                else:
                    print(Fore.RED + "❌ No user selected or failed to load user.")
                continue
            elif choice == "2":
                family_code = input(Fore.YELLOW + "Enter family code (or '99' to cancel): " + Fore.WHITE)
                if family_code == "99":
                    continue
                use_decoy = input(Fore.YELLOW + "Use decoy package? (y/n): " + Fore.WHITE).lower() == 'y'
                pause_on_success = input(Fore.YELLOW + "Pause on each successful purchase? (y/n): " + Fore.WHITE).lower() == 'y'
                purchase_by_family(family_code, use_decoy, pause_on_success)
            elif choice == "3":
                delay = int(input(Fore.YELLOW + "⏱️  Enter delay in seconds: " + Fore.WHITE))
                print(Fore.GREEN + "🚀 Memulai loop untuk Bebas Puas TIKTOK ADD 42GB...")
                while True:
                    if not purchase_loop(
                        family_code='8080ddcf-18c5-4d6d-86a4-89eb8ca5f2d1',
                        order=1,
                        use_decoy=True,
                        delay=delay,
                        pause_on_success=True
                    ):
                        break
            elif choice == "4":
                delay = int(input(Fore.YELLOW + "⏱️  Enter delay in seconds: " + Fore.WHITE))
                print(Fore.GREEN + "🚀 Memulai loop untuk Bebas Puas TIKTOK ADD 39GB...")
                while True:
                    if not purchase_loop(
                        family_code='8080ddcf-18c5-4d6d-86a4-89eb8ca5f2d1',
                        order=3,
                        use_decoy=True,
                        delay=delay,
                        pause_on_success=True
                    ):
                        break
            elif choice == "5":
                delay = int(input(Fore.YELLOW + "⏱️  Enter delay in seconds: " + Fore.WHITE))
                print(Fore.GREEN + "🚀 Memulai loop untuk for Kuota Pelanggan Baru 10GB + 30H...")
                while True:
                    if not purchase_loop(
                        family_code='0069ab97-3e54-41ef-87ea-807621d1922c',
                        order=1,
                        use_decoy=True,
                        delay=delay,
                        pause_on_success=True
                    ):
                        break
            elif choice == "6":
                delay = int(input(Fore.YELLOW + "⏱️  Enter delay in seconds: " + Fore.WHITE))
                print(Fore.GREEN + "🚀 Memulai loop untuk Bonus Kuota Utama 15GB...")
                while True:
                    if not purchase_loop(
                        family_code='0069ab97-3e54-41ef-87ea-807621d1922c',
                        order=52,
                        use_decoy=True,
                        delay=delay,
                        pause_on_success=True
                    ):
                        break
            elif choice == "7":
                delay = int(input(Fore.YELLOW + "⏱️  Enter delay in seconds: " + Fore.WHITE))
                print(Fore.GREEN + "🚀 Memulai loop untuk Akrab 2kb...")
                while True:
                    if not purchase_loop(
                        family_code='4889cc43-55c9-47dd-8f7e-d3ac9fae6022',
                        order=5,
                        use_decoy=True,
                        delay=delay,
                        pause_on_success=True
                    ):
                        break
            elif choice == "8":
                delay = int(input(Fore.YELLOW + "⏱️  Enter delay in seconds: " + Fore.WHITE))
                print(Fore.GREEN + "🚀 Memulai loop untuk XC Mini...")
                while True:
                    if not purchase_loop(
                        family_code='ad176860-49d4-4bdd-9161-ab38dc6a631b',
                        order=1,
                        use_decoy=True,
                        delay=delay,
                        pause_on_success=True
                    ):
                        break
            elif choice == "9":
                print(Fore.MAGENTA + Style.BRIGHT + "\n⚡ MODE CUSTOM")
                print(Fore.CYAN + "─" * 70)
                family_code = input(Fore.YELLOW + "📝 Enter family code: " + Fore.WHITE)
                order = int(input(Fore.YELLOW + "🔢 Enter order number: " + Fore.WHITE))
                delay = int(input(Fore.YELLOW + "⏱️  Enter delay in seconds: " + Fore.WHITE))
                print(Fore.GREEN + f"🚀 Memulai custom loop untuk (Order #{order})...")
                while True:
                    if not purchase_loop(
                        family_code=family_code,
                        order=order,
                        use_decoy=True,
                        delay=delay,
                        pause_on_success=True
                    ):
                        break
            elif choice == "99":
                print(Fore.GREEN + "\n✅ Exiting the application.")
                sys.exit(0)
            else:
                print(Fore.RED + "❌ Invalid choice. Please try again.")
                pause()
        else:
            # Not logged in
            print(Fore.RED + "⚠️  You are not logged in!")
            selected_user_number = show_account_menu()
            if selected_user_number:
                AuthInstance.set_active_user(selected_user_number)
            else:
                print(Fore.RED + "❌ No user selected or failed to load user.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Exiting the application.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

from app.client.engsel import get_otp, submit_otp
from app.menus.util import clear_screen, pause
from app.service.auth import AuthInstance
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

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

def show_login_menu():
    clear_screen()
    print_ascii_art()
    print(Fore.MAGENTA + Style.BRIGHT + "              🔐 LOGIN MENU 🔐")
    print(Fore.CYAN + "═" * 70)
    print(Fore.WHITE + " 1. " + Fore.GREEN + "Request OTP")
    print(Fore.WHITE + " 2. " + Fore.GREEN + "Submit OTP")
    print(Fore.WHITE + " 99. " + Fore.RED + "❌ Tutup aplikasi")
    print(Fore.CYAN + "═" * 70)
    
def login_prompt(api_key: str):
    clear_screen()
    print_ascii_art()
    print(Fore.MAGENTA + Style.BRIGHT + "              🔐 LOGIN KE MYXL 🔐")
    print(Fore.CYAN + "═" * 70)
    print(Fore.YELLOW + "\n📱 Masukan nomor XL (Contoh: 6281234567890)")
    phone_number = input(Fore.WHITE + "Nomor: ")

    if not phone_number.startswith("628") or len(phone_number) < 10 or len(phone_number) > 14:
        print(Fore.RED + "❌ Nomor tidak valid. Pastikan nomor diawali dengan '628' dan memiliki panjang yang benar.")
        return None

    try:
        print(Fore.YELLOW + "\n⏳ Mengirim OTP...")
        subscriber_id = get_otp(phone_number)
        if not subscriber_id:
            return None
        print(Fore.GREEN + "✅ OTP Berhasil dikirim ke nomor Anda.")
        
        otp = input(Fore.YELLOW + "\n🔑 Masukkan OTP yang telah dikirim: " + Fore.WHITE)
        if not otp.isdigit() or len(otp) != 6:
            print(Fore.RED + "❌ OTP tidak valid. Pastikan OTP terdiri dari 6 digit angka.")
            pause()
            return None
        
        print(Fore.YELLOW + "⏳ Memverifikasi OTP...")
        tokens = submit_otp(api_key, phone_number, otp)
        if not tokens:
            print(Fore.RED + "❌ Gagal login. Periksa OTP dan coba lagi.")
            pause()
            return None
        
        print(Fore.GREEN + "✅ Berhasil login!")
        pause()
        
        return phone_number, tokens["refresh_token"]
    except Exception as e:
        print(Fore.RED + f"❌ Error: {str(e)}")
        pause()
        return None, None

def show_account_menu():
    clear_screen()
    AuthInstance.load_tokens()
    users = AuthInstance.refresh_tokens
    active_user = AuthInstance.get_active_user()
    
    in_account_menu = True
    add_user = False
    while in_account_menu:
        clear_screen()
        print_ascii_art()
        
        if AuthInstance.get_active_user() is None or add_user:
            number, refresh_token = login_prompt(AuthInstance.api_key)
            if not refresh_token:
                print(Fore.RED + "❌ Gagal menambah akun. Silahkan coba lagi.")
                pause()
                continue
            
            AuthInstance.add_refresh_token(int(number), refresh_token)
            AuthInstance.load_tokens()
            users = AuthInstance.refresh_tokens
            active_user = AuthInstance.get_active_user()
            
            if add_user:
                add_user = False
            continue
        
        print(Fore.MAGENTA + Style.BRIGHT + "              👥 MANAJEMEN AKUN 👥")
        print(Fore.CYAN + "═" * 70)
        
        print(Fore.GREEN + Style.BRIGHT + "\n📋 AKUN TERSIMPAN:")
        print(Fore.CYAN + "─" * 70)
        
        if not users or len(users) == 0:
            print(Fore.YELLOW + "⚠️  Tidak ada akun tersimpan.")
        else:
            for idx, user in enumerate(users):
                is_active = active_user and user["number"] == active_user["number"]
                if is_active:
                    active_marker = Fore.GREEN + Style.BRIGHT + " ✓ (Aktif)"
                else:
                    active_marker = ""
                print(Fore.WHITE + f" {idx + 1}. " + Fore.CYAN + f"{user['number']}" + active_marker)
        
        print(Fore.CYAN + "\n" + "─" * 70)
        print(Fore.BLUE + Style.BRIGHT + "⚙️  COMMAND:")
        print(Fore.WHITE + "  0  → " + Fore.GREEN + "Tambah Akun")
        print(Fore.WHITE + " 00  → " + Fore.CYAN + "Kembali ke menu utama")
        print(Fore.WHITE + " 99  → " + Fore.RED + "Hapus Akun aktif")
        print(Fore.CYAN + "─" * 70)
        print(Fore.YELLOW + "💡 Masukan nomor akun untuk berganti.")
        print(Fore.CYAN + "═" * 70)
        
        input_str = input(Fore.YELLOW + Style.BRIGHT + "\nPilihan: " + Fore.WHITE)
        
        if input_str == "00":
            in_account_menu = False
            return active_user["number"] if active_user else None
        elif input_str == "0":
            add_user = True
            continue
        elif input_str == "99":
            if not active_user:
                print(Fore.RED + "❌ Tidak ada akun aktif untuk dihapus.")
                pause()
                continue
            confirm = input(Fore.YELLOW + f"⚠️  Yakin ingin menghapus akun {active_user['number']}? (y/n): " + Fore.WHITE)
            if confirm.lower() == 'y':
                AuthInstance.remove_refresh_token(active_user["number"])
                users = AuthInstance.refresh_tokens
                active_user = AuthInstance.get_active_user()
                print(Fore.GREEN + "✅ Akun berhasil dihapus.")
                pause()
            else:
                print(Fore.YELLOW + "⚠️  Penghapusan akun dibatalkan.")
                pause()
            continue
        elif input_str.isdigit() and 1 <= int(input_str) <= len(users):
            selected_user = users[int(input_str) - 1]
            print(Fore.GREEN + f"✅ Beralih ke akun: {selected_user['number']}")
            pause()
            return selected_user['number']
        else:
            print(Fore.RED + "❌ Input tidak valid. Silahkan coba lagi.")
            pause()
            continue
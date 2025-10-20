import json
import sys

import requests
from app.service.auth import AuthInstance
from app.client.engsel import get_family, get_package, get_addons, get_package_details, send_api_request
from app.service.bookmark import BookmarkInstance
from app.client.purchase import settlement_bounty, settlement_loyalty
from app.menus.util import clear_screen, pause, display_html
from app.client.qris import show_qris_payment
from app.client.ewallet import show_multipayment
from app.client.balance import settlement_balance
from app.type_dict import PaymentItem
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


def show_package_details(api_key, tokens, package_option_code, is_enterprise, option_order = -1):
    clear_screen()
    print_ascii_art()
    print(Fore.MAGENTA + Style.BRIGHT + "              📦 DETAIL PAKET 📦")
    print(Fore.CYAN + "═" * 70)
    
    print(Fore.YELLOW + "⏳ Loading package details...")
    package = get_package(api_key, tokens, package_option_code)
    
    if not package:
        print(Fore.RED + "❌ Failed to load package details.")
        pause()
        return False

    price = package["package_option"]["price"]
    detail = display_html(package["package_option"]["tnc"])
    validity = package["package_option"]["validity"]

    option_name = package.get("package_option", {}).get("name","")
    family_name = package.get("package_family", {}).get("name","")
    variant_name = package.get("package_detail_variant", "").get("name","")
    
    title = f"{family_name} - {variant_name} - {option_name}".strip()
    
    token_confirmation = package["token_confirmation"]
    ts_to_sign = package["timestamp"]
    payment_for = package["package_family"]["payment_for"]
    
    payment_items = [
        PaymentItem(
            item_code=package_option_code,
            product_type="",
            item_price=price,
            item_name=f"{variant_name} {option_name}".strip(),
            tax=0,
            token_confirmation=token_confirmation,
        )
    ]
    
    print(Fore.GREEN + Style.BRIGHT + "\n📋 INFORMASI PAKET")
    print(Fore.CYAN + "─" * 70)
    print(Fore.WHITE + "📌 Nama         : " + Fore.YELLOW + f"{title}")
    print(Fore.WHITE + "💰 Harga        : " + Fore.GREEN + f"Rp {price}")
    print(Fore.WHITE + "💳 Payment For  : " + Fore.CYAN + f"{payment_for}")
    print(Fore.WHITE + "⏰ Masa Aktif   : " + Fore.MAGENTA + f"{validity}")
    print(Fore.WHITE + "⭐ Point        : " + Fore.YELLOW + f"{package['package_option']['point']}")
    print(Fore.WHITE + "📊 Plan Type    : " + Fore.BLUE + f"{package['package_family']['plan_type']}")
    print(Fore.CYAN + "─" * 70)
    
    benefits = package["package_option"]["benefits"]
    if benefits and isinstance(benefits, list):
        print(Fore.GREEN + Style.BRIGHT + "\n🎁 BENEFITS:")
        print(Fore.CYAN + "─" * 70)
        for benefit in benefits:
            print(Fore.YELLOW + f"  📦 {benefit['name']}")
            print(Fore.WHITE + f"     ID: " + Fore.CYAN + f"{benefit['item_id']}")
            data_type = benefit['data_type']
            if data_type == "VOICE" and benefit['total'] > 0:
                print(Fore.WHITE + f"     Total: " + Fore.GREEN + f"{benefit['total']/60} menit")
            elif data_type == "TEXT" and benefit['total'] > 0:
                print(Fore.WHITE + f"     Total: " + Fore.GREEN + f"{benefit['total']} SMS")
            elif data_type == "DATA" and benefit['total'] > 0:
                if benefit['total'] > 0:
                    quota = int(benefit['total'])
                    if quota >= 1_000_000_000:
                        quota_gb = quota / (1024 ** 3)
                        print(Fore.WHITE + f"     Quota: " + Fore.GREEN + f"{quota_gb:.2f} GB")
                    elif quota >= 1_000_000:
                        quota_mb = quota / (1024 ** 2)
                        print(Fore.WHITE + f"     Quota: " + Fore.GREEN + f"{quota_mb:.2f} MB")
                    elif quota >= 1_000:
                        quota_kb = quota / 1024
                        print(Fore.WHITE + f"     Quota: " + Fore.GREEN + f"{quota_kb:.2f} KB")
                    else:
                        print(Fore.WHITE + f"     Total: " + Fore.GREEN + f"{quota}")
            elif data_type not in ["DATA", "VOICE", "TEXT"]:
                print(Fore.WHITE + f"     Total: " + Fore.GREEN + f"{benefit['total']} ({data_type})")
            
            if benefit["is_unlimited"]:
                print(Fore.MAGENTA + "     ♾️  Unlimited: Yes")
            print(Fore.CYAN + "     " + "─" * 66)
    
    addons = get_addons(api_key, tokens, package_option_code)
    bonuses = addons.get("bonuses", [])
    
    print(Fore.BLUE + Style.BRIGHT + "\n🔧 ADDONS:")
    print(Fore.CYAN + "─" * 70)
    print(json.dumps(addons, indent=2))
    print(Fore.CYAN + "─" * 70)
    
    print(Fore.YELLOW + Style.BRIGHT + "\n📜 SYARAT & KETENTUAN:")
    print(Fore.CYAN + "─" * 70)
    print(detail)
    print(Fore.CYAN + "─" * 70)
    
    in_package_detail_menu = True
    while in_package_detail_menu:
        print(Fore.BLUE + Style.BRIGHT + "\n💳 METODE PEMBAYARAN:")
        print(Fore.CYAN + "─" * 70)
        print(Fore.WHITE + " 1. " + Fore.GREEN + "💰 Beli dengan Pulsa")
        print(Fore.WHITE + " 2. " + Fore.CYAN + "📱 Beli dengan E-Wallet")
        print(Fore.WHITE + " 3. " + Fore.MAGENTA + "📲 Bayar dengan QRIS")
        print(Fore.WHITE + " 4. " + Fore.YELLOW + "🎯 Pulsa + Decoy XCP")
        
        if payment_for == "":
            payment_for = "BUY_PACKAGE"
        
        if payment_for == "REDEEM_VOUCHER":
            print(Fore.WHITE + " 5. " + Fore.GREEN + "🎁 Ambil sebagai bonus (jika tersedia)")
            print(Fore.WHITE + " 6. " + Fore.YELLOW + "⭐ Beli dengan Poin (jika tersedia)")
        
        if option_order != -1:
            print(Fore.WHITE + " 0. " + Fore.BLUE + "🔖 Tambah ke Bookmark")
        print(Fore.WHITE + " 00. " + Fore.RED + "◀️  Kembali ke daftar paket")
        print(Fore.CYAN + "─" * 70)

        choice = input(Fore.YELLOW + Style.BRIGHT + "Pilihan: " + Fore.WHITE)
        
        if choice == "00":
            return False
        if choice == "0" and option_order != -1:
            success = BookmarkInstance.add_bookmark(
                family_code=package.get("package_family", {}).get("package_family_code",""),
                family_name=package.get("package_family", {}).get("name",""),
                is_enterprise=is_enterprise,
                variant_name=variant_name,
                option_name=option_name,
                order=option_order,
            )
            if success:
                print(Fore.GREEN + "✅ Paket berhasil ditambahkan ke bookmark.")
            else:
                print(Fore.YELLOW + "⚠️  Paket sudah ada di bookmark.")
            pause()
            continue
        
        if choice == '1':
            settlement_balance(api_key, tokens, payment_items, payment_for, True)
            input(Fore.YELLOW + "💡 Silahkan cek hasil pembelian di aplikasi MyXL. Tekan Enter untuk kembali.")
            return True
        elif choice == '2':
            show_multipayment(api_key, tokens, payment_items, payment_for, True)
            input(Fore.YELLOW + "💡 Silahkan lakukan pembayaran & cek hasil pembelian di aplikasi MyXL. Tekan Enter untuk kembali.")
            return True
        elif choice == '3':
            show_qris_payment(api_key, tokens, payment_items, payment_for, True)
            input(Fore.YELLOW + "💡 Silahkan lakukan pembayaran & cek hasil pembelian di aplikasi MyXL. Tekan Enter untuk kembali.")
            return True
        elif choice == '4':
            print(Fore.YELLOW + "⏳ Loading decoy package...")
            url = "https://me.mashu.lol/pg-decoy-xcp.json"
            
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                print(Fore.RED + "❌ Gagal mengambil data decoy package.")
                pause()
                return None
            
            decoy_data = response.json()
            decoy_package_detail = get_package_details(
                api_key, tokens,
                decoy_data["family_code"],
                decoy_data["variant_code"],
                decoy_data["order"],
                decoy_data["is_enterprise"],
                decoy_data["migration_type"],
            )

            payment_items.append(
                PaymentItem(
                    item_code=decoy_package_detail["package_option"]["package_option_code"],
                    product_type="",
                    item_price=decoy_package_detail["package_option"]["price"],
                    item_name=decoy_package_detail["package_option"]["name"],
                    tax=0,
                    token_confirmation=decoy_package_detail["token_confirmation"],
                )
            )

            overwrite_amount = price + decoy_package_detail["package_option"]["price"]
            res = settlement_balance(api_key, tokens, payment_items, "BUY_PACKAGE", False, overwrite_amount)
            
            if res and res.get("status", "") != "SUCCESS":
                error_msg = res.get("message", "Unknown error")
                if "Bizz-err.Amount.Total" in error_msg:
                    error_msg_arr = error_msg.split("=")
                    valid_amount = int(error_msg_arr[1].strip())
                    
                    print(Fore.YELLOW + f"⚙️  Adjusted total amount to: {valid_amount}")
                    res = settlement_balance(api_key, tokens, payment_items, "BUY_PACKAGE", False, valid_amount)
                    if res and res.get("status", "") == "SUCCESS":
                        print(Fore.GREEN + "✅ Purchase successful!")
            else:
                print(Fore.GREEN + "✅ Purchase successful!")
            pause()
            return True
        elif choice == '5':
            settlement_bounty(api_key, tokens, token_confirmation, ts_to_sign, package_option_code, price, variant_name)
            input(Fore.YELLOW + "💡 Silahkan lakukan pembayaran & cek hasil pembelian di aplikasi MyXL. Tekan Enter untuk kembali.")
            return True
        elif choice == '6':
            settlement_loyalty(api_key, tokens, token_confirmation, ts_to_sign, package_option_code, price)
            input(Fore.YELLOW + "💡 Silahkan lakukan pembayaran & cek hasil pembelian di aplikasi MyXL. Tekan Enter untuk kembali.")
            return True
        else:
            print(Fore.RED + "❌ Purchase cancelled.")
            return False
    pause()
    sys.exit(0)

def get_packages_by_family(family_code: str, is_enterprise: bool | None = None, migration_type: str | None = None):
    api_key = AuthInstance.api_key
    tokens = AuthInstance.get_active_tokens()
    if not tokens:
        print(Fore.RED + "❌ No active user tokens found.")
        pause()
        return None
    
    packages = []
    
    print(Fore.YELLOW + "⏳ Loading family data...")
    data = get_family(api_key, tokens, family_code, is_enterprise, migration_type)
    
    if not data:
        print(Fore.RED + "❌ Failed to load family data.")
        pause()
        return None
        
    price_currency = "Rp"
    rc_bonus_type = data["package_family"].get("rc_bonus_type", "")
    if rc_bonus_type == "MYREWARDS":
        price_currency = "Poin"
    
    in_package_menu = True
    while in_package_menu:
        clear_screen()
        print_ascii_art()
        print(Fore.MAGENTA + Style.BRIGHT + "              📦 DAFTAR PAKET 📦")
        print(Fore.CYAN + "═" * 70)
        
        print(Fore.GREEN + Style.BRIGHT + "\n📋 INFORMASI FAMILY")
        print(Fore.CYAN + "─" * 70)
        print(Fore.WHITE + "📌 Family Name  : " + Fore.YELLOW + f"{data['package_family']['name']}")
        print(Fore.WHITE + "🔑 Family Code  : " + Fore.CYAN + f"{family_code}")
        print(Fore.WHITE + "📊 Family Type  : " + Fore.MAGENTA + f"{data['package_family']['package_family_type']}")
        print(Fore.WHITE + "📦 Variant Count: " + Fore.GREEN + f"{len(data['package_variants'])}")
        print(Fore.CYAN + "─" * 70)
        
        print(Fore.GREEN + Style.BRIGHT + "\n🛒 PAKET TERSEDIA")
        print(Fore.CYAN + "═" * 70)
        
        package_variants = data["package_variants"]
        
        option_number = 1
        variant_number = 1
        
        for variant in package_variants:
            variant_name = variant["name"]
            variant_code = variant["package_variant_code"]
            print(Fore.YELLOW + Style.BRIGHT + f"\n 📂 Variant {variant_number}: {variant_name}")
            print(Fore.CYAN + f"    Code: {variant_code}")
            
            for option in variant["package_options"]:
                option_name = option["name"]
                
                packages.append({
                    "number": option_number,
                    "variant_name": variant_name,
                    "option_name": option_name,
                    "price": option["price"],
                    "code": option["package_option_code"],
                    "option_order": option["order"]
                })
                                
                print(Fore.WHITE + f"    {option_number}. " + Fore.GREEN + f"{option_name} " + Fore.CYAN + f"- {price_currency} {option['price']}")
                
                option_number += 1
            
            if variant_number < len(package_variants):
                print(Fore.CYAN + "    " + "─" * 66)
            variant_number += 1
        
        print(Fore.CYAN + "\n═" * 70)
        print(Fore.WHITE + " 00. " + Fore.RED + "◀️  Kembali ke menu utama")
        print(Fore.CYAN + "═" * 70)
        
        pkg_choice = input(Fore.YELLOW + Style.BRIGHT + "\nPilih paket (nomor): " + Fore.WHITE)
        
        if pkg_choice == "00":
            in_package_menu = False
            return None
            
        selected_pkg = next((p for p in packages if p["number"] == int(pkg_choice)), None)
        
        if not selected_pkg:
            print(Fore.RED + "❌ Paket tidak ditemukan. Silakan masukan nomor yang benar.")
            pause()
            continue
        
        is_done = show_package_details(api_key, tokens, selected_pkg["code"], is_enterprise, option_order=selected_pkg["option_order"])
        if is_done:
            in_package_menu = False
            return None
        else:
            continue
        
    return packages

def fetch_my_packages():
    api_key = AuthInstance.api_key
    tokens = AuthInstance.get_active_tokens()
    if not tokens:
        print(Fore.RED + "❌ No active user tokens found.")
        pause()
        return None
    
    id_token = tokens.get("id_token")
    
    path = "api/v8/packages/quota-details"
    
    payload = {
        "is_enterprise": False,
        "lang": "en",
        "family_member_id": ""
    }
    
    print(Fore.YELLOW + "⏳ Fetching my packages...")
    res = send_api_request(api_key, path, payload, id_token, "POST")
    if res.get("status") != "SUCCESS":
        print(Fore.RED + "❌ Failed to fetch packages")
        print(Fore.RED + "Response:", res)
        pause()
        return None
    
    quotas = res["data"]["quotas"]
    
    clear_screen()
    print_ascii_art()
    print(Fore.MAGENTA + Style.BRIGHT + "              📦 PAKET SAYA 📦")
    print(Fore.CYAN + "═" * 70)
    
    my_packages =[]
    num = 1
    for quota in quotas:
        quota_code = quota["quota_code"]
        group_code = quota["group_code"]
        group_name = quota["group_name"]
        quota_name = quota["name"]
        family_code = "N/A"
        
        benefit_infos = []
        benefits = quota.get("benefits", [])
        if len(benefits) > 0:
            for benefit in benefits:
                benefit_id = benefit.get("id", "")
                name = benefit.get("name", "")
                data_type = benefit.get("data_type", "N/A")
                benefit_info = Fore.CYAN + "  ─────────────────────────────────────────────────────────────────\n"
                benefit_info += Fore.WHITE + "  ID    : " + Fore.CYAN + f"{benefit_id}\n"
                benefit_info += Fore.WHITE + "  Name  : " + Fore.YELLOW + f"{name}\n"
                benefit_info += Fore.WHITE + "  Type  : " + Fore.MAGENTA + f"{data_type}\n"
                

                remaining = benefit.get("remaining", 0)
                total = benefit.get("total", 0)

                if data_type == "DATA":
                    if remaining >= 1_000_000_000:
                        remaining_gb = remaining / (1024 ** 3)
                        remaining_str = f"{remaining_gb:.2f} GB"
                    elif remaining >= 1_000_000:
                        remaining_mb = remaining / (1024 ** 2)
                        remaining_str = f"{remaining_mb:.2f} MB"
                    elif remaining >= 1_000:
                        remaining_kb = remaining / 1024
                        remaining_str = f"{remaining_kb:.2f} KB"
                    else:
                        remaining_str = str(remaining)
                    
                    if total >= 1_000_000_000:
                        total_gb = total / (1024 ** 3)
                        total_str = f"{total_gb:.2f} GB"
                    elif total >= 1_000_000:
                        total_mb = total / (1024 ** 2)
                        total_str = f"{total_mb:.2f} MB"
                    elif total >= 1_000:
                        total_kb = total / 1024
                        total_str = f"{total_kb:.2f} KB"
                    else:
                        total_str = str(total)
                    
                    benefit_info += Fore.WHITE + "  Kuota : " + Fore.GREEN + f"{remaining_str}" + Fore.WHITE + " / " + Fore.CYAN + f"{total_str}"
                elif data_type == "VOICE":
                    benefit_info += Fore.WHITE + "  Kuota : " + Fore.GREEN + f"{remaining/60:.2f}" + Fore.WHITE + " / " + Fore.CYAN + f"{total/60:.2f} menit"
                elif data_type == "TEXT":
                    benefit_info += Fore.WHITE + "  Kuota : " + Fore.GREEN + f"{remaining}" + Fore.WHITE + " / " + Fore.CYAN + f"{total} SMS"
                else:
                    benefit_info += Fore.WHITE + "  Kuota : " + Fore.GREEN + f"{remaining}" + Fore.WHITE + " / " + Fore.CYAN + f"{total}"

                benefit_infos.append(benefit_info)
            
        
        print(Fore.YELLOW + f"⏳ Fetching package no. {num} details...")
        package_details = get_package(api_key, tokens, quota_code)
        if package_details:
            family_code = package_details["package_family"]["package_family_code"]
        
        print(Fore.CYAN + "\n═" * 70)
        print(Fore.GREEN + Style.BRIGHT + f"📦 Package {num}")
        print(Fore.CYAN + "─" * 70)
        print(Fore.WHITE + "📌 Name        : " + Fore.YELLOW + f"{quota_name}")
        
        if len(benefit_infos) > 0:
            print(Fore.WHITE + "\n🎁 Benefits:")
            for bi in benefit_infos:
                print(bi)
            print(Fore.CYAN + "  ─────────────────────────────────────────────────────────────────")
        
        print(Fore.WHITE + "\n📊 Group Name  : " + Fore.CYAN + f"{group_name}")
        print(Fore.WHITE + "🔑 Quota Code  : " + Fore.MAGENTA + f"{quota_code}")
        print(Fore.WHITE + "🏷️  Family Code : " + Fore.BLUE + f"{family_code}")
        print(Fore.WHITE + "🆔 Group Code  : " + Fore.YELLOW + f"{group_code}")
        print(Fore.CYAN + "═" * 70)
        
        my_packages.append({
            "number": num,
            "quota_code": quota_code,
        })
        
        num += 1
    
    print(Fore.YELLOW + "\n💡 Rebuy package? Input package number to rebuy, or '00' to back.")
    choice = input(Fore.YELLOW + Style.BRIGHT + "Choice: " + Fore.WHITE)
    
    if choice == "00":
        return None
        
    selected_pkg = next((pkg for pkg in my_packages if str(pkg["number"]) == choice), None)
    
    if not selected_pkg:
        print(Fore.RED + "❌ Paket tidak ditemukan. Silakan masukan nomor yang benar.")
        pause()
        return None
    
    is_done = show_package_details(api_key, tokens, selected_pkg["quota_code"], False)
    if is_done:
        return None
        
    pause()
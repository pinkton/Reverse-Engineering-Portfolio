import logging, lief, os, sys, subprocess, stat, time
from operator import contains
from subprocess import Popen

#Set cmd line logging information
logging.basicConfig(level=logging.INFO) #Prints all info and above
#logging.basicConfig(level=logging.WARNING) ##Displays all warnings and above

#File in question
myapp = lief.parse("C:\\Users\\Keiran\\projects\\helloworld\\x64\\Release\\Helloworld.exe")
logging.info("[+] EXE found")

#Custom hook code
code = [
                0x48, 0x83, 0xc4, 0x48,                                     # add rsp, 0x48         ; Stack unwind
                0x48, 0x31, 0xc9,                                           # xor rcx, rcx          ; hWnd
                0x48, 0x89, 0xd2,                                           # mov rdx, rdx          ; Message
                0x49, 0xB8, 0x00, 0xF0, 0x00, 0x40, 0x01, 0x00, 0x00, 0x00, # mov r8, 0x14000f000   ; Title
                0x4d, 0x31, 0xc9,                                           # xor r9, r9            ; MessageBox push button: OK
                0x48, 0xB8, 0x44, 0x04, 0x01, 0x40, 0x01, 0x00, 0x00, 0x00, # mov rax,0x140010444   ; MessageBoxA address
                0xff, 0x10,                                                 # call [rax]            ; MessageBoxA(hWnd, Message, Title, MB_OK)
                0x48, 0x31, 0xc9,                                           # xor rcx, rcx          ; exit value
                0x48, 0xB8, 0x34, 0x04, 0x01, 0x40, 0x01, 0x00, 0x00, 0x00, # mov rax, 0x140010434  ; ExitProcess address
                0xff, 0x10,                                                 # call [rax]            ; ExitProcess(0)
                0xc3                                                        # ret                   ; Never reached
                ]

#Data for the exe
title = "LIEF is awesome\0"
data  =  list(map(ord, title))

logging.info("[+] Custom ASM hex read")

# Create a '.text' section which will contain the hooking code and add it
section_text                 = lief.PE.Section(".htext")
section_text.content         = code
section_text.virtual_address = 0xe000
section_text.characteristics = lief.PE.SECTION_CHARACTERISTICS.CNT_CODE | lief.PE.SECTION_CHARACTERISTICS.MEM_READ | lief.PE.SECTION_CHARACTERISTICS.MEM_EXECUTE
section_text = myapp.add_section(section_text)
htext = 0

# Create '.data' section for the string(s) and add it
section_data                 = lief.PE.Section(".hdata")
section_data.content         = data
section_data.virtual_address = 0xf000
section_data.characteristics = lief.PE.SECTION_CHARACTERISTICS.CNT_INITIALIZED_DATA | lief.PE.SECTION_CHARACTERISTICS.MEM_READ
section_data = myapp.add_section(section_data)
hdata = 0

#Check for created sections created above
for sections in myapp.sections:
    if ".htext" in (sections.name):
        htext = 1
    if ".hdata" in (sections.name):
        hdata = 1

if htext != 1:
    logging.error("[-!-] .htext not found!")
else:
    logging.info("[+] .htext found")

if hdata != 1:
    logging.error("[-!-] .hdata not found!")
else:
    logging.info("[+] .hdata found")

#Print all sections in the application
""" for sections in myapp.sections:
    print("Name -- V.Size -- V.Addr -- Raw Size -- Raw Addr  -- ?? -- Entropy")
    print(sections) """ 

# Disable ASLR
myapp.optional_header.dll_characteristics &= ~lief.PE.DLL_CHARACTERISTICS.DYNAMIC_BASE

logging.info("[+] Disabled ASLR - DYNAMIC_BASE -- " + hex(myapp.optional_header.dll_characteristics))

# Disable NX protection
myapp.optional_header.dll_characteristics &= ~lief.PE.DLL_CHARACTERISTICS.NX_COMPAT
if (myapp.has_nx) == False:
    logging.info("[+] Disabled NX Protection")
else:
    logging.warning("[-!-] NX Protection was not disabled!")

# Add the 'ExitProcess' function to kernel32
kernel32 = myapp.get_import("KERNEL32.dll")
kernel32.add_entry("ExitProcess")

# Add the 'user32.dll' library
user32 = myapp.add_library("user32.dll")
user32.add_entry("MessageBoxA")

logging.info("[+] ExitProcess and MessageBoxA loaded")

ExitProcess_addr = myapp.predict_function_rva("KERNEL32.dll", "ExitProcess")
ExitProcess_addr += myapp.optional_header.imagebase
MessageBoxA_addr = myapp.predict_function_rva("user32.dll", "MessageBoxA")
MessageBoxA_addr += myapp.optional_header.imagebase
print("Address of 'MessageBoxA': 0x{:06x} ".format(MessageBoxA_addr))
print("Address of 'ExitProcess': 0x{:06x} ".format(ExitProcess_addr))

# Hook the '__acrt_iob_func' function with our code
myapp.hook_function("__acrt_iob_func", section_text.virtual_address + myapp.optional_header.imagebase)
logging.info("[+] __acrt_iob_func is hooked, not going to run")

# Invoke the builder
builder = lief.PE.Builder(myapp)

# Configure it to rebuild and patch the imports
builder.build_imports(True)
builder.patch_imports(True)

# Build !
builder.build()

# Save the result
builder.write("lief_pe64_hooking.exe")
logging.info("[+] File saved")

output = ("C:\\Users\\Keiran\\projects\\helloworld\\lief_pe64_hooking.exe")

st = os.stat(output)
os.chmod(output, st.st_mode | stat.S_IEXEC)

if sys.platform.startswith("win"):
    subprocess_flags = 0x8000000 # win32con.CREATE_NO_WINDOW?
    p = Popen(["START", output, "foo"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=subprocess_flags)
    time.sleep(3)
    q = Popen(["taskkill", "/im", "lief_pe64_hooking.exe"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
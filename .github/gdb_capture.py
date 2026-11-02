import gdb


def u32(expr):
    try:
        return int(gdb.parse_and_eval(expr)) & 0xffffffff
    except Exception:
        return 0


def mem32(address):
    if not 0x50000000 <= address < 0x68000000:
        return 0
    try:
        data = gdb.selected_inferior().read_memory(address, 4)
        return int.from_bytes(bytes(data), "little")
    except Exception:
        return 0


def emit(text):
    gdb.write(text)
    try:
        gdb.flush()
    except Exception:
        pass


class E68EF0Probe(gdb.Breakpoint):
    def __init__(self, offset, label):
        super().__init__("*sub_00E68EF0+%d" % offset)
        self.label = label

    def stop(self):
        rbx = u32("$rbx")
        r11 = u32("$r11")
        ebx = u32("g_ebx")
        esi = u32("g_esi")
        edi = u32("g_edi")
        ebp = u32("g_ebp")
        esp = u32("g_esp")
        emit(
            "[gdb] E68EF0+%s rbx=%#x ebx=%#x r11=%#x "
            "esi=%#x edi=%#x ebp=%#x esp=%#x\n"
            % (self.label, rbx, ebx, r11, esi, edi, ebp, esp)
        )
        if self.label == "6699-chain":
            emit(
                "[gdb] source=%#x candidate=%#x local=%#x source+4c=%#x\n"
                % (rbx, r11, ebp, mem32(rbx + 0x4c))
            )
        else:
            emit(
                "[gdb] ebp+8=%#x ebp+c=%#x ebp+24=%#x\n"
                % (mem32(ebp + 0x8), mem32(ebp + 0xc),
                   mem32(ebp + 0x24))
            )
            emit(
                "[gdb] esp[0..3]=%#x/%#x/%#x/%#x\n"
                % (mem32(esp), mem32(esp + 4), mem32(esp + 8),
                   mem32(esp + 0xc))
            )
        self.enabled = False
        return False


probes = [
    E68EF0Probe(6699, "6699-chain"),
    E68EF0Probe(7359, "7359-null"),
]

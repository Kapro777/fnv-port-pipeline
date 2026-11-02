import gdb


def u32(expr):
    try:
        return int(gdb.parse_and_eval(expr)) & 0xffffffff
    except Exception:
        return 0


class E68EF0Predecessor(gdb.Breakpoint):
    def __init__(self):
        super().__init__("*sub_00E68EF0+6699")

    def stop(self):
        rbx = u32("$rbx")
        r11 = u32("$r11")
        ebx = u32("g_ebx")
        esi = u32("g_esi")
        edi = u32("g_edi")
        ebp = u32("g_ebp")
        gdb.write(
            "[gdb] E68EF0+6699 predecessor "
            "rbx=%#x ebx=%#x r11=%#x esi=%#x edi=%#x ebp=%#x\n"
            % (rbx, ebx, r11, esi, edi, ebp)
        )
        for label, address in (("source", rbx), ("predecessor", r11),
                               ("local", ebp)):
            if 0x50000000 <= address < 0x68000000:
                gdb.write("[gdb] %s=%#x\n" % (label, address))
                gdb.execute("x/8wx %#x" % address)
        if 0x50000000 <= r11 < 0x68000000:
            gdb.write(
                "[gdb] predecessor +4c=%#x\n"
                % u32("*(unsigned int *)(%#x + 0x4c)" % r11)
            )
        self.delete()
        return False


E68EF0Predecessor()

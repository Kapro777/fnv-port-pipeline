import gdb


def u32(expr):
    try:
        return int(gdb.parse_and_eval(expr)) & 0xffffffff
    except Exception:
        return 0


class E68EF0Current(gdb.Breakpoint):
    def __init__(self):
        super().__init__("*sub_00E68EF0+7359")

    def stop(self):
        rbx = u32("$rbx")
        r11 = u32("$r11")
        ebx = u32("g_ebx")
        esi = u32("g_esi")
        edi = u32("g_edi")
        ebp = u32("g_ebp")
        gdb.write(
            "[gdb] E68EF0+7359 before ebp+8 "
            "rbx=%#x ebx=%#x r11=%#x esi=%#x edi=%#x ebp=%#x\n"
            % (rbx, ebx, r11, esi, edi, ebp)
        )
        gdb.write("[gdb] ebp+8=%#x ebp+c=%#x ebp+24=%#x\n" % (
            u32("*(unsigned int *)(%#x + 0x8)" % ebp),
            u32("*(unsigned int *)(%#x + 0xc)" % ebp),
            u32("*(unsigned int *)(%#x + 0x24)" % ebp)))
        for label, address in (("source", rbx), ("r11", r11),
                               ("local", ebp)):
            if 0x50000000 <= address < 0x68000000:
                gdb.write("[gdb] %s=%#x\n" % (label, address))
                gdb.execute("x/40wx %#x" % address)
        if 0x50000000 <= u32("g_esp") < 0x68000000:
            gdb.write("[gdb] esp=%#x\n" % u32("g_esp"))
            gdb.execute("x/32wx %#x" % u32("g_esp"))
        self.delete()
        return False


E68EF0Current()

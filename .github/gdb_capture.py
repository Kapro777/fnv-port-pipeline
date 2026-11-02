import gdb


def u32(expr):
    try:
        return int(gdb.parse_and_eval(expr)) & 0xffffffff
    except Exception:
        return 0


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
        gdb.write(
            "[gdb] E68EF0+%s rbx=%#x ebx=%#x r11=%#x "
            "esi=%#x edi=%#x ebp=%#x esp=%#x\n"
            % (self.label, rbx, ebx, r11, esi, edi, ebp, esp)
        )
        if self.label == "6699-chain":
            for label, address in (("source", rbx), ("candidate", r11),
                                   ("local", ebp)):
                if 0x50000000 <= address < 0x68000000:
                    gdb.write("[gdb] %s=%#x\n" % (label, address))
                    gdb.execute("x/40wx %#x" % address)
            if 0x50000000 <= rbx < 0x68000000:
                gdb.write(
                    "[gdb] source+4c=%#x\n"
                    % u32("*(unsigned int *)(%#x + 0x4c)" % rbx)
                )
        else:
            gdb.write("[gdb] ebp+8=%#x ebp+c=%#x ebp+24=%#x\n" % (
                u32("*(unsigned int *)(%#x + 0x8)" % ebp),
                u32("*(unsigned int *)(%#x + 0xc)" % ebp),
                u32("*(unsigned int *)(%#x + 0x24)" % ebp)))
            if 0x50000000 <= ebp < 0x68000000:
                gdb.execute("x/40wx %#x" % ebp)
            if 0x50000000 <= esp < 0x68000000:
                gdb.write("[gdb] esp=%#x\n" % esp)
                gdb.execute("x/32wx %#x" % esp)
        self.delete()
        return False


E68EF0Probe(6699, "6699-chain")
E68EF0Probe(7359, "7359-null")

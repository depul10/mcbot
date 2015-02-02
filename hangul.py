# This file is part of KoreanCodecs.
#
# Copyright(C) 2002-2003 Hye-Shik Chang <perky@FreeBSD.org>.
#
# KoreanCodecs is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# KoreanCodecs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with KoreanCodecs; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: hangul.py,v 1.2 2003/10/15 19:24:53 perky Exp $
#

class UnicodeHangulError(Exception):
    
    def __init__ (self, msg):
        self.msg = msg
        Exception.__init__(self, msg)
    
    def __repr__ (self):
        return self.msg
    
    __str__ = __repr__

Null = ''

class Jaeum(object):

    Codes = ('\u3131', '\u3132', '\u3133', '\u3134', '\u3135', '\u3136',
            #   G        GG         GS        N         NJ        NH
             '\u3137', '\u3138', '\u3139', '\u313a', '\u313b', '\u313c',
            #   D        DD         L         LG        LM        LB
             '\u313d', '\u313e', '\u313f', '\u3140', '\u3141', '\u3142',
            #   LS       LT         LP        LH        M         B
             '\u3143', '\u3144', '\u3145', '\u3146', '\u3147', '\u3148',
            #   BB       BS         S         SS        NG        J
             '\u3149', '\u314a', '\u314b', '\u314c', '\u314d', '\u314e')
            #   JJ       C          K         T         P         H
    Width = len(Codes)
    G, GG, GS, N, NJ, NH, D, DD, L, LG, LM, LB, LS, LT, LP, LH, M, B, \
    BB, BS, S, SS, NG, J, JJ, C, K, T, P, H = Codes
    Choseong = [G, GG, N, D, DD, L, M, B, BB, S, SS, NG, J, JJ, C, K, T, P, H]
    Jongseong = [Null, G, GG, GS, N, NJ, NH, D, L, LG, LM, LB, LS, LT, \
                LP, LH, M, B, BS, S, SS, NG, J, C, K, T, P, H]
    MultiElement = {
        GG: (G, G),  GS: (G, S),  NJ: (N, J),  NH: (N, H),  DD: (D, D),
        LG: (L, G),  LM: (L, M),  LB: (L, B),  LS: (L, S),  LT: (L, T),
        LP: (L, P),  LH: (L, H),  BB: (B, B),  BS: (B, S),  SS: (S, S),
        JJ: (J, J)
    }


class Moeum(object):

    Codes = ('\u314f', '\u3150', '\u3151', '\u3152', '\u3153', '\u3154',
            #   A         AE       YA        YAE        EO        E
             '\u3155', '\u3156', '\u3157', '\u3158', '\u3159', '\u315a',
            #   YEO       YE       O         WA         WAE       OE
             '\u315b', '\u315c', '\u315d', '\u315e', '\u315f', '\u3160',
            #   YO        U        WEO       WE         WI        YU
             '\u3161', '\u3162', '\u3163')
            #   EU        YI       I
    Width = len(Codes)
    A, AE, YA, YAE, EO, E, YEO, YE, O, WA, WAE, OE, YO, \
    U, WEO, WE, WI, YU, EU, YI, I = Codes
    Jungseong = list(Codes)
    MultiElement = {
        AE: (A, I),  YAE: (YA, I),  YE: (YEO, I), WA: (O, A),  WAE: (O, A, I),
        OE: (O, I),  WEO: (U, EO),  WE: (U, E),   WI: (U, I),  YI: (EU, I)
    }

# Aliases for your convinience
Choseong = Jaeum.Choseong
Jungseong = Moeum.Jungseong
Jongseong = Jaeum.Jongseong

for name, code in list(Jaeum.__dict__.items()) + list(Moeum.__dict__.items()):
    if name.isupper() and len(name) <= 3:
        exec("%s = %s" % (name, repr(code)))
del name, code

# Unicode Hangul Syllables Characteristics
ZONE = ('\uAC00', '\uD7A3')
NCHOSEONG  = len(Choseong)
NJUNGSEONG = len(Jungseong)
NJONGSEONG = len(Jongseong)
JBASE_CHOSEONG  = '\u1100'
JBASE_JUNGSEONG = '\u1161'
JBASE_JONGSEONG = '\u11A8'
CHOSEONG_FILLER = '\u115F'
JUNGSEONG_FILLER = '\u1160'

_ishangul = (
    lambda code:
        ZONE[0] <= code <= ZONE[1] or
        code in Jaeum.Codes or
        code in Moeum.Codes
)

# Alternative Suffixes : do not use outside
ALT_SUFFIXES = {
    '\uc744': ('\ub97c', '\uc744'), # reul, eul
    '\ub97c': ('\ub97c', '\uc744'), # reul, eul
    '\uc740': ('\ub294', '\uc740'), # neun, eun
    '\ub294': ('\ub294', '\uc740'), # neun, eun
    '\uc774': ('\uac00', '\uc774'), # yi, ga
    '\uac00': ('\uac00', '\uc774'), # yi, ga
    '\uc640': ('\uc640', '\uacfc'), # wa, gwa
    '\uacfc': ('\uc640', '\uacfc'), # wa, gwa
}

# Ida-Varitaion Suffixes : do not use outside
IDA_SUFFIXES = {
    '(\uc774)': ('', '\uc774'),     # (yi)da
    '(\uc785)': (17, '\uc785'),      # (ip)nida
    '(\uc778)': (4, '\uc778'),       # (in)-
}

def isJaeum(u):
    if u:
        for c in u:
            if c not in Jaeum.Codes:
                break
        else:
            return True
    return False

def isMoeum(u):
    if u:
        for c in u:
            if c not in Moeum.Codes:
                break
        else:
            return True
    return False

def ishangul(u):
    if u:
        for c in u:
            if not _ishangul(c):
                break
        else:
            return True
    return False

def join(codes):
    """ Join function which makes hangul syllable from jamos """
    if len(codes) is not 3:
        raise UnicodeHangulError("needs 3-element tuple")
    if not codes[0] or not codes[1]: # single jamo
        return codes[0] or codes[1]

    return chr(
        0xac00 + (
            Choseong.index(codes[0])*NJUNGSEONG +
            Jungseong.index(codes[1])
        )*NJONGSEONG + Jongseong.index(codes[2])
    )

def split(code):
    """ Split function which splits hangul syllable into jamos """
    if len(code) != 1 or not _ishangul(code):
        raise UnicodeHangulError("needs 1 hangul letter")
    if code in Jaeum.Codes:
        return (code, Null, Null)
    if code in Moeum.Codes:
        return (Null, code, Null)

    code = ord(code) - 0xac00
    return (
        Choseong[int(code / (NJUNGSEONG*NJONGSEONG))], # Python3000 safe
        Jungseong[int(code / NJONGSEONG) % NJUNGSEONG],
        Jongseong[code % NJONGSEONG]
    )

def conjoin(s):
    obuff = []
    ncur = 0

    while ncur < len(s):
        c = s[ncur]
        if JBASE_CHOSEONG <= c <= '\u1112' or c == CHOSEONG_FILLER: # starts with choseong
            if len(s) > ncur+1 and JUNGSEONG_FILLER <= s[ncur+1] <= '\u1175':
                cho = Choseong[ord(c) - ord(JBASE_CHOSEONG)]
                jung = Jungseong[ord(s[ncur+1]) - ord(JBASE_JUNGSEONG)]
                if len(s) > ncur+2 and JBASE_JONGSEONG <= s[ncur+2] <= '\u11C2':
                    jong = Jongseong[ord(s[ncur+2]) - ord(JBASE_JONGSEONG) + 1]
                    ncur += 2
                else:
                    jong = Null
                    ncur += 1
                obuff.append(join([cho, jung, jong]))
            else:
                obuff.append(join([Choseong[ord(c) - ord(JBASE_CHOSEONG)], Null, Null]))
        elif JBASE_JUNGSEONG <= c <= '\u1175':
            obuff.append(join([Null, Jungseong[ord(c) - ord(JBASE_JUNGSEONG)], Null]))
        else:
            obuff.append(c)
        ncur += 1
    
    return ''.join(obuff)

def disjoint(s):
    obuff = []
    for c in s:
        if _ishangul(c):
            cho, jung, jong = split(c)
            if cho:
                obuff.append( chr(ord(JBASE_CHOSEONG) + Choseong.index(cho)) )
            else:
                obuff.append( CHOSEONG_FILLER )

            if jung:
                obuff.append( chr(ord(JBASE_JUNGSEONG) + Jungseong.index(jung)) )
            else:
                obuff.append( JUNGSEONG_FILLER )

            if jong:
                obuff.append( chr(ord(JBASE_JONGSEONG) + Jongseong.index(jong) - 1) )
        else:
            obuff.append(c)
    return ''.join(obuff)

def _has_final(c):
    # for internal use only
    if '\uac00' <= c <= '\ud7a3': # hangul
        return 1, (ord(c) - 0xac00) % 28 > 0
    else:
        return 0, c in '013678.bklmnptLMNRZ'

def format(fmtstr, *args, **kwargs):
    if kwargs:
        argget = lambda:kwargs
    else:
        argget = iter(args).next

    obuff = []
    ncur = escape = fmtinpth = 0
    ofmt = fmt = ''

    while ncur < len(fmtstr):
        c = fmtstr[ncur]

        if escape:
            obuff.append(c)
            escape = 0
            ofmt   = ''
        elif c == '\\':
            escape = 1
        elif fmt:
            fmt += c
            if not fmtinpth and c.isalpha():
                ofmt = fmt % argget()
                obuff.append(ofmt)
                fmt = ''
            elif fmtinpth and c == ')':
                fmtinpth = 0
            elif c == '(':
                fmtinpth = 1
            elif c == '%':
                obuff.append('%')
        elif c == '%':
            fmt  += c
            ofmt = ''
        else:
            if ofmt and c in ALT_SUFFIXES:
                obuff.append(ALT_SUFFIXES[c][
                    _has_final(ofmt[-1])[1] and 1 or 0
                ])
            elif ofmt and fmtstr[ncur:ncur+3] in IDA_SUFFIXES:
                sel = IDA_SUFFIXES[fmtstr[ncur:ncur+3]]
                ishan, hasfinal = _has_final(ofmt[-1])

                if hasfinal:
                    obuff.append(sel[1])
                elif ishan:
                    if sel[0]:
                        obuff[-1] = obuff[-1][:-1] + chr(ord(ofmt[-1]) + sel[0])
                else:
                    obuff.append(sel[0] and sel[1])
                ncur += 2
            else:
                obuff.append(c)
    
            ofmt = ''

        ncur += 1
    
    return ''.join(obuff)


#
# This file is part of KoreanCodecs.
#
# Copyright(C) 2002-2003 Hye-Shik Chang <perky@FreeBSD.org>.
#
# KoreanCodecs is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# KoreanCodecs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with KoreanCodecs; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: qwerty2bul.py,v 1.4 2003/10/16 03:58:14 perky Exp $
#

import codecs

_2bul_codekeymap = {
    Jaeum.G: 'r',   Jaeum.GG:'R',   Jaeum.GS: 'rt',
    Jaeum.N: 's',   Jaeum.NJ:'sw',  Jaeum.NH: 'sg', Jaeum.D:  'e',
    Jaeum.DD:'E',   Jaeum.L: 'f',   Jaeum.LG: 'fr', Jaeum.LM: 'fa',
    Jaeum.LB:'fq',  Jaeum.LS:'ft',  Jaeum.LT: 'fx', Jaeum.LP: 'fv',
    Jaeum.LH:'fg',  Jaeum.M: 'a',   Jaeum.B:  'q',  Jaeum.BB: 'Q',
    Jaeum.BS:'qt',  Jaeum.S: 't',   Jaeum.SS: 'T',  Jaeum.NG:  'd',
    Jaeum.J: 'w',   Jaeum.JJ:'W',   Jaeum.C:  'c',  Jaeum.K:  'z',
    Jaeum.T: 'x',   Jaeum.P: 'v',   Jaeum.H:  'g',

    Moeum.A: 'k',   Moeum.AE:'o',   Moeum.YA: 'i',  Moeum.YAE:'O',
    Moeum.EO:'j',   Moeum.E: 'p',   Moeum.YEO:'u',  Moeum.YE: 'P',
    Moeum.O: 'h',   Moeum.WA:'hk',  Moeum.WAE:'ho', Moeum.OE: 'hl',
    Moeum.YO:'y',   Moeum.U: 'n',   Moeum.WEO:'nj', Moeum.WE: 'np',
    Moeum.WI:'nl',  Moeum.YU:'b',   Moeum.EU: 'm',  Moeum.YI: 'ml',
    Moeum.I: 'l',

    '': '',
}

_2bul_keycodemap = {}
for k, v in _2bul_codekeymap.items():
    _2bul_keycodemap[v] = k
    _2bul_keycodemap.setdefault(v.upper(), k)
_2bul_keycodes = ''.join(_2bul_keycodemap.keys())
del k, v


class Automata_Hangul2(object):
    
    # must Unicode in / Unicode out

    def __init__(self):
        self.clear()

    def pushcomp(self):
        if not (self.chosung and self.jungsung):
            self.word_valid = 0
        self.word_comp.append(join([
            self.chosung, self.jungsung, self.jongsung
        ]))
        self.clearcomp()

    def clearcomp(self):
        self.chosung = ''
        self.jungsung = ''
        self.jongsung = ''

    def clear(self):
        self.buff = ['']
        self.word_raw = []
        self.word_comp = []
        self.word_valid = 1
        self.clearcomp()

    def convert(self, s):
        self.clear()

        for c in s: self.feed(c)
        self.finalize()

        return ''.join(self.buff)
    
    def finalize(self):
        if self.chosung or self.jungsung or self.jongsung:
            self.pushcomp()
        if self.word_raw or self.word_comp:
            if self.word_valid:
                rjoi = ''.join(self.word_comp)
                r = 0
            else:
                self.word_valid = 1
                rjoi = ''.join(self.word_raw)
                r = 1

            self.word_raw, self.word_comp = [], []
            if rjoi:
                self.buff.append(rjoi)
                return r
        return 0

    def feed(self, c):
        self.word_raw.append(c)
        if c in _2bul_keycodes:
            code = _2bul_keycodemap[c]
            if isJaeum(code):
                if not self.chosung: # chosung O
                    if self.jungsung or self.jongsung:
                        self.word_valid = 0
                    else:
                        self.chosung = code
                elif not self.jungsung: # chosung O  jungsung X
                    if self.jongsung:
                        self.word_valid = 0
                    else:
                        self.pushcomp()
                        self.chosung = code
                elif not self.jongsung: # chosung O  jungsung O  jongsung X
                    if code not in Jongseong:
                        self.pushcomp()
                        self.chosung = code
                    else:
                        self.jongsung = code
                else: # full
                    trymul = _2bul_codekeymap[self.jongsung] + c
                    if trymul in _2bul_keycodemap: # can be multi jongsung
                        self.jongsung = _2bul_keycodemap[trymul]
                    else:
                        self.pushcomp()
                        self.chosung = code
            else: # MOEUM...
                if not self.jongsung:
                    if not self.jungsung: # jungsung X  jongsung X
                        self.jungsung = code
                    else: # jungsung O  jongsung X
                        trymul = _2bul_codekeymap[self.jungsung] + c
                        if trymul in _2bul_keycodemap: # can be multi jungsung
                            self.jungsung = _2bul_keycodemap[trymul]
                        else:
                            self.pushcomp()
                            self.jungsung = code
                else: # jongsung O
                    if len(_2bul_codekeymap[self.jongsung]) > 1:
                        ojong = _2bul_keycodemap[_2bul_codekeymap[self.jongsung][:-1]]
                        ncho  = _2bul_keycodemap[_2bul_codekeymap[self.jongsung][-1]]
                        self.jongsung = ojong
                        self.pushcomp()
                        self.chosung = ncho
                        self.jungsung = code
                    else:
                        njong = self.jongsung
                        self.jongsung = ''
                        self.pushcomp()
                        self.chosung = njong
                        self.jungsung = code
        else: # non key code
            if not self.finalize():
                self.buff.append(c)


class Codec_Hangul2(codecs.Codec):

    BASECODEC = 'utf-8' # fallback codec of decoder

    # Unicode to key stroke
    def encode(self, data, errors='strict'):
        if errors not in ('strict', 'ignore', 'replace'):
            raise ValueError("unknown error handling")

        r = []
        for c in data:
            if c <= '\u0080':
                r.append(c.encode('ascii'))
            elif not ishangul(c):
                r.append(c.encode(self.BASECODEC, errors=errors))
            else:
                for k in split(c):
                    r.append(_2bul_codekeymap[k])

        r = ''.join(r)
        return (r, len(r))

    # key stroke to Unicode
    def decode(self, data, errors='strict'):
        if errors not in ('strict', 'ignore', 'replace'):
            raise ValueError("unknown error handling")

        if isinstance(data, str):
            s = data
        else:
            s = str(data, self.BASECODEC, errors)
        am = Automata_Hangul2()
        r = am.convert(s)
        return (r, len(r))

class StreamWriter_Hangul2(Codec_Hangul2, codecs.StreamWriter):
    pass

class StreamReader_Hangul2(Codec_Hangul2, codecs.StreamReader):
    pass


#
# This file is part of KoreanCodecs.
#
# Copyright(C) 2002-2003 Hye-Shik Chang <perky@FreeBSD.org>.
#
# KoreanCodecs is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# KoreanCodecs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with KoreanCodecs; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: qwerty3bul.py,v 1.2 2003/10/16 03:58:14 perky Exp $
#

import codecs

# This mapping table is kindly contributed by Mithrandir.
_3bul_codekeymap = [{
    Jaeum.G: 'k',   Jaeum.GG:'kk',   
    Jaeum.N: 'h',   
    Jaeum.D: 'u',
    Jaeum.DD:'uu',  
    Jaeum.L: 'y',   
    Jaeum.M: 'i',   Jaeum.B:  ';',  Jaeum.BB: ';;',
    Jaeum.S: 'n',   Jaeum.SS: 'nn', 
    Jaeum.NG:'j', 
    Jaeum.J: 'l',   Jaeum.JJ:'ll',   Jaeum.C:  'o',  Jaeum.K:  '0',
    Jaeum.T: '\'',  Jaeum.P: 'p',    Jaeum.H:  'm',
    '': '',
}, {
    Moeum.A: 'f',   Moeum.AE:'r',   Moeum.YA: '6',  Moeum.YAE:'G',
    Moeum.EO:'t',   Moeum.E: 'c',   Moeum.YEO:'e',  Moeum.YE: '7',
    Moeum.O: 'v',   Moeum.WA:'/f',  Moeum.WAE:'/r', Moeum.OE: '/d',
    Moeum.YO:'4',   Moeum.U: 'b',   Moeum.WEO:'9t', Moeum.WE: '9c',
    Moeum.WI:'9d',  Moeum.YU:'5',   Moeum.EU: 'g',  Moeum.YI: '8',
    Moeum.I: 'd',
    '': '',
}, {
    Jaeum.G: 'x',   Jaeum.GG: '!',  Jaeum.GS: 'V',
    Jaeum.N: 's',   Jaeum.NJ: 'E',  Jaeum.NH: 'S',
    Jaeum.D: 'A',
    Jaeum.L: 'w', Jaeum.LG: '@', Jaeum.LM: 'F',
    Jaeum.LB: 'D', Jaeum.LS: 'T', Jaeum.LT: '%',
    Jaeum.LP:'$', Jaeum.LH: 'R',
    Jaeum.M: 'z', 
    Jaeum.B: '3', Jaeum.BS: 'X',
    Jaeum.S: 'q', Jaeum.SS: '2',
    Jaeum.NG:'a', Jaeum.J: '#',
    Jaeum.C: 'Z', Jaeum.K: 'C',
    Jaeum.T: 'W', Jaeum.P: 'Q', Jaeum.H: '1',
    '': '',
}]

_3bul_keycodemap = []
for cmap in _3bul_codekeymap:
    m = {}
    for k, v in cmap.items():
        m[v] = k
        m.setdefault(v.upper(), k)
    _3bul_keycodemap.append(m)
_3bul_keycodemap[1].update({
'/': Moeum.O, '9': Moeum.U,
}) # double allocated jungseongs

class Automata_Hangul3(object):
    
    # must Unicode in / Unicode out

    def __init__(self):
        self.clear()

    def pushcomp(self):
        if not (self.choseong and self.jungseong):
            self.word_valid = 0
        self.word_comp.append(join([
            self.choseong, self.jungseong, self.jongseong
        ]))
        self.clearcomp()

    def clearcomp(self):
        self.choseong = ''
        self.jungseong = ''
        self.jongseong = ''

    def clear(self):
        self.buff = ['']
        self.word_raw = []
        self.word_comp = []
        self.word_valid = 1
        self.clearcomp()

    def convert(self, s):
        self.clear()

        for c in s: self.feed(c)
        self.finalize()

        return ''.join(self.buff)
    
    def finalize(self):
        if self.choseong or self.jungseong or self.jongseong:
            self.pushcomp()
        if self.word_raw or self.word_comp:
            if self.word_valid:
                rjoi = ''.join(self.word_comp)
                r = 0
            else:
                self.word_valid = 1
                rjoi = ''.join(self.word_raw)
                r = 1

            self.word_raw, self.word_comp = [], []
            if rjoi:
                self.buff.append(rjoi)
                return r
        return 0

    def feed(self, c):
        self.word_raw.append(c)
        if c in _3bul_keycodemap[0]: # choseong key
            if self.choseong:
                if (self.choseong in (Jaeum.G, Jaeum.D, Jaeum.B, Jaeum.S,
                        Jaeum.J) and self.choseong == _3bul_keycodemap[0][c]):
                    c = c+c
                else:
                    self.pushcomp()
            self.choseong = _3bul_keycodemap[0][c]
        elif c in _3bul_keycodemap[1]: # jungseong key
            if self.jungseong:
                if self.jungseong == Moeum.O and '/'+c in _3bul_keycodemap[1]:
                    c = '/'+c
                elif self.jungseong == Moeum.U and '9'+c in _3bul_keycodemap[1]:
                    c = '9'+c
                else:
                    self.pushcomp()
            self.jungseong = _3bul_keycodemap[1][c]
        elif c in _3bul_keycodemap[2]: # jongseong key
            if self.jongseong:
                self.pushcomp()
            self.jongseong = _3bul_keycodemap[2][c]
        else: # non key code
            if not self.finalize():
                self.buff.append(c)


class Codec_Hangul3(codecs.Codec):

    BASECODEC = 'utf-8' # fallback codec of decoder

    # Unicode to key stroke
    def encode(self, data, errors='strict'):
        if errors not in ('strict', 'ignore', 'replace'):
            raise ValueError("unknown error handling")

        r = []
        for c in data:
            if c <= '\u0080':
                r.append(c.encode('ascii'))
            elif not ishangul(c):
                r.append(c.encode(self.BASECODEC, errors=errors))
            else:
                for k, m in zip(split(c), _3bul_codekeymap):
                    r.append(m[k])

        r = ''.join(r)
        return (r, len(r))

    # key stroke to Unicode
    def decode(self, data, errors='strict'):
        if errors not in ('strict', 'ignore', 'replace'):
            raise ValueError("unknown error handling")

        if isinstance(data, str):
            s = data
        else:
            s = str(data, self.BASECODEC, errors)
        am = Automata_Hangul3()
        r = am.convert(s)
        return (r, len(r))

class StreamWriter_Hangul3(Codec_Hangul3, codecs.StreamWriter):
    pass

class StreamReader_Hangul3(Codec_Hangul3, codecs.StreamReader):
    pass


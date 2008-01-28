#!/usr/bin/python

# Update kernel.conf based on kernel .config file
# arekm@pld-linux.org
# glen@pld-linux.org

import sys
import re

if len(sys.argv) != 4:
    print "Usage: %s target_arch kernel.conf .config" % sys.argv[0]
    sys.exit(1)

arch = sys.argv[1]
kernelconfig = sys.argv[2]
inconfig = sys.argv[3]

from UserDict import UserDict

# odict (Ordered Dict) from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/107747
class odict(UserDict):
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)

dict = odict()

rc = 0
f = open(kernelconfig, 'r')
for l in f:
    if l[:6] == 'CONFIG_':
        print "Omit CONFIG_ when specifing symbol name: %s" % l
        rc = 1
        continue

    if re.match('^#', l) or re.match('^\s*$', l):
        continue

    if not re.match('^[0-9A-Z]+', l):
        print "Unknown line: %s" % l
        rc = 1
        continue

    c = l.strip().split()
    symbol = c[0]
    if dict.has_key(symbol):
        print "Duplicate symbol: %s" % symbol
        rc = 1
        continue

    conf = dict[symbol] = odict()
    for item in c[1:]:
        (key, value) = item.split('=')
        dict[symbol][key] = value

#    print "Add symbol: %s = %s" % (symbol, dict[symbol])

f.close()
#rc =1

if not rc == 0:
    sys.exit(1)

f = open(inconfig, 'r')
for l in f:
    # yes, module and string, numeric values
    m = re.match("^CONFIG_(.*)=(.*)$", l)
    if not m == None:
        symbol = m.group(1)
        value = m.group(2)
    else:
        # no values
        m = re.match("^# CONFIG_(.*) is not set$", l)
        if not m == None:
            symbol = m.group(1)
            value = "n"

    # other data. perhaps comments
    if m == None:
        print l.strip()
        continue

    if dict.has_key(symbol):
        c = dict[symbol]
        if c.has_key('all') and c.has_key(arch):
            c[arch] = value
        if c.has_key('all'):
            c['all'] = value
        else:
            c[arch] = value

        s = ''
        for k in c.keys():
            s += ' %s=%s' % (k, c[k])

        l = "%s %s" % (symbol, s.strip())
        del dict[symbol]
    else:
        l = "%s %s=%s" % (symbol, arch, value)

    # blacklist
    # TODO: use some list here instead
    if symbol != "LOCALVERSION" and symbol != "DEFCONFIG_LIST":
        print l

f.close()

# print out remaining items from old dictionary
for symbol in dict.keys():
    s = ''
    c = dict[symbol]
    for k in c.keys():
        s += ' %s=%s' % (k, c[k])
    print "%s %s" % (symbol, s.strip())

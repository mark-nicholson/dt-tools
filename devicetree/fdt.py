#
#  Flattened Device Tree Parser
#     Interpret a compiled flattened-device-tree file (.dtb)
#
#  Copyright 2014 - Mark Nicholson <nicholson.mark@gmail.com>
#

import sys


class FDTTags(object):
    BEGIN_NODE = 1
    END_NODE = 2
    PROP = 3
    NOP = 4
    END = 9

    # textual names for the states
    name = [ '', 'BEGIN_NODE', 'END_NODE', 'PROP', 'NOP', '', '', '', '', 'END' ]
    

class FDTBase(object):

    def __init__(self, fdt=None, offset=-1, origin=None):
        self._fields = [ 'offset' ]
        if origin is None:
            if fdt is None or offset == -1:
                raise ValueError("Must specify fdt,offset for new entry or origin=x for copy-constructor")
            self._fdt = fdt
            self.offset = offset
        else:
            self._fdt = origin._fdt
            self.offset = origin.offset

    @staticmethod
    def _fdt32_to_py(data, offset):
        s = offset
        e = s + 4
        return int.from_bytes(data[s:e], 'big')

    @staticmethod
    def _py_to_fdt32(value):
        return int.to_bytes(value, 'big')

    def serialize(self):
        bstr = b''
        for field,fmt in self._fields:
            bstr += self._py_to_fdt(getattr(self, field))
        return bstr

    def value_text(self):
        raise NotImplemented("You must override value_text()")
    
    def __str__(self):
        s = self.__class__.__name__ + '('
        for field in self._fields:
            fn = getattr(self, '_disp_'+field, str)
            s += field + " -> " + fn(getattr(self, field)) + ", "
        else:
            s += field + " -> " + fn(getattr(self, field)) + ')'
        return s

    @staticmethod
    def _disp_tag(tag):
        return FDTTags.name[tag]


class FDTHeader(FDTBase):
    """
    FDTHeader Class
    Emulate the C-Structure representation of the data at the start of an FDT.
    """
    
    def __init__(self, fdt):
        super().__init__(fdt, 0)

        self._fields = [ 'magic',
                         'totalsize',
                         'off_dt_struct',
                         'off_dt_strings',
                         'off_mem_rsvmap',
                         'version',
                         'last_comp_version']
        offset = 0

        for field in self._fields:
            setattr(self, field, self._fdt32_to_py(self._fdt.data, offset))
            offset += 4

        if self.version >= 2:
            self.boot_cpuid_phys = self._fdt32_to_py(self._fdt.data, offset)
            self._fields.append( 'boot_cpuid_phys' )
            offset += 4

        if self.version >= 3:
            self.size_dt_strings = self._fdt32_to_py(self._fdt.data, offset)
            self._fields.append( 'size_dt_strings' )
            offset += 4

        if self.version >= 17:
            self.size_dt_struct = self._fdt32_to_py(self._fdt.data, offset)
            self._fields.append( 'size_dt_struct' )
            offset += 4

        self._header = self._fdt.data[:offset]

    @staticmethod
    def _disp_magic(magic):
        return hex(magic)


class FDTNodeHeader(FDTBase):

    def __init__(self, fdt, offset):
        super().__init__(fdt, offset)
        
        self.offset = offset
        self._fields += [ 'tag', 'name' ]

        # tag is a direct value
        self.tag = self._fdt32_to_py(self._fdt.data, offset)
        offset += 4

        # subsection the bytes
        end = self._fdt.data.find(b'\x00', offset)
        self.name = self._fdt.data[offset:end]
        self.name = self.name.decode('UTF-8')
        

    def __len__(self):
        """The ALIGNED length of the whole structure."""

        # length is really a C-string, so account for the '\0'
        length = len(self.name) + 1

        # account for the tag
        length += 4

        # pad...
        length = ((length + 3) // 4) * 4

        # done
        return length

    def value_text(self):
        return ''

    @staticmethod
    def _disp_name(name):
        if name is None:
            return "<none>"
        return name


class FDTProperty(FDTBase):

    def __init__(self, fdt=None, offset=0, origin=None):
        super().__init__(fdt, offset, origin)

        # management
        self._fields += [ 'tag',
                          'length',
                          'name_offset',
                          'name',
                          'data' ]

        # adjust the pointer
        if origin is None:

            # extract the fields
            self.tag = self._fdt32_to_py(self._fdt.data, offset)
            offset += 4
            
            self.length = self._fdt32_to_py(self._fdt.data, offset)
            offset += 4
            
            self.name_offset = self._fdt32_to_py(self._fdt.data, offset)
            offset += 4            

            # grab the data
            s = offset
            e = s + ((self.length + 3) // 4) * 4
            self.data = self._fdt.data[s:e]

            # dig out the name
            s = fdt.header.off_dt_strings + self.name_offset
            e = self._fdt.data.find(b'\x00', s)
            if e > 0:
                self.name = self._fdt.data[s:e]
            else:
                self.name = "<invalid>"
                print("FDTProperty: error: failed to locate end of name string")

        else:
            self.tag = origin.tag
            self.length = origin.length
            self.name_offset = origin.name_offset
            self.name = origin.name
            self.data = origin.data


    def __len__(self):
        # pad out the data length
        length = ((self.length + 3) // 4) * 4

        # account for the tag, length, name_offset
        length += 3 * 4

        # done
        return length

    def value_text(self):
        return "<debug me>"


class FDTStringProperty(FDTProperty):

    def __init__(self, fdt=None, offset=0, origin=None):
        super().__init__(fdt, offset, origin)

        self._fields += [ 'text' ]

        # should convert it to a string
        self.text = self.data.decode('UTF-8')

    def Match(prop):
        Tags = [
            'compatible', 'chosen', 'model', 'console'
            ]

        if prop.name in Tags:
            return True
        if (prop.length % 4) != 0:
            return True
        else:
            # check for only printable chars, followed only by up to 4 '\0' bytes
            pass
        return False

    def value_text(self):
        return self.text


class FDTIntegerProperty(FDTProperty):

    def __init__(self, fdt=None, offset=0, origin=None):
        super().__init__(fdt, offset, origin)

        self._fields += [ 'value' ]

        # generate the integer value
        self.value = self._fdt32_to_py(self.data, 0)

    
    def Match(prop):
        Tags = [
            'interrupt-parent'
            ]
        if prop.name in Tags:
            return True
        if prop.name.startswith(b'#'):
            return True
        if prop.length == 4:
            return True
        return False

    @staticmethod
    def _disp_value(value):
        return hex(value)

    def value_text(self):
        return self._disp_value( self.value )


class FDTArrayProperty(FDTProperty):

    def __init__(self, fdt=None, offset=0, origin=None):
        super().__init__(fdt, offset, origin)

        self._fields += [ 'items' ]
        self.items = []

        # copy over and convert
        for i in range(0, self.length, 4):
            self.items.append( self._fdt32_to_py( self.data, i ) )

    def Match(prop):
        Tags  = [
            'cpufreq_tbl', 'reg', 'ranges', 'dmas', 'interrupts', 'data_width'
            ]
    
        if prop.name in Tags:
            return True
        if prop.length % 4 == 0 and prop.length > 4:
            return True
        return False

    @staticmethod
    def _disp_items(items):
        s = '< '
        for i in items:
            s += hex(i) + ', '
        else:
            s += hex(i) + ' >'
        return s

    def value_text(self):
        return self._disp_items( self.items )


class FDTAction(object):

    def __init__(self):
        super().__init__()

    def manage(self, fdt, offset, item):
        raise NotImplementedError("Action must customise 'manage()")

    def enter(self, fdt, offset, item):
        raise NotImplementedError("Action must customise 'enter()")

    def exit(self, fdt, offset, item):
        raise NotImplementedError("Action must customise 'exit()")


class FDT(object):

    def __init__(self, filename):
        self.filename = filename

        fd = open(filename, 'rb')
        self.data = fd.read()
        fd.close()

        # pull the header
        self.header = FDTHeader(self)

    def CreateProperty(self, offset):
        # Generate a generic property
        prop = FDTProperty(self, offset)

        # update the type
        if FDTStringProperty.Match(prop):
            prop = FDTStringProperty(origin=prop)
        elif FDTIntegerProperty.Match(prop):
            prop = FDTIntegerProperty(origin=prop)
        elif FDTArrayProperty.Match(prop):
            prop = FDTArrayProperty(origin=prop)

        return prop


    def walk(self, action, offset=None):

        depth = 0

        # adjust the default
        if offset is None:
            offset = self.header.off_dt_struct

        # iterate at this level
        while True:
            
            # grab a header
            item = FDTNodeHeader(self, offset)

            if item.tag == FDTTags.END_NODE:
                offset += 4
                break

            if item.tag == FDTTags.BEGIN_NODE:
                noff = offset + len(item)
                action.enter(self, offset, item)
                offset = self.walk(action, noff) 
                action.exit(self, offset, item)
                continue

            if item.tag == FDTTags.PROP:
                # rebrand
                item = self.CreateProperty(offset)

                # manage this node
                action.manage(self, offset, item)
                offset = offset + len(item)
                continue
            
            if item.tag == FDTTags.NOP:
                offset += 4
                continue

            if item.tag == FDTTags.END:
                offset += 4
                break

        # close out this node
        return offset
    


class DebugAction(FDTAction):
    def __init__(self):
        super().__init__()
        self.depth = 0

    def manage(self, fdt, offset, item):
        self.msg('MANAGE: ', item, offset)

    def enter(self, fdt, offset, item):
        self.depth += 1
        self.msg('ENTER: ', item, offset)

    def exit(self, fdt, offset, item):
        self.msg('EXIT: ', item, offset)
        self.depth -= 1

    def msg(self, text, item, offset):
        pad = '    ' * self.depth
        #print(pad + text + item.__class__.__name__ + '@%d' % offset)
        print(pad + text + '%d: ' % offset + str(item))

                
if __name__ == "__main__":
    fdt = FDT('devicetree/test/spear1310-evb.dtb')

    print(fdt.header)

    action = DebugAction()
    fdt.walk(action)
    

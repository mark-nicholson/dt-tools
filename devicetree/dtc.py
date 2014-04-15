#
#  Flattened Device Tree Compiler Wrapper
#     Drive the 'dtc' utility in an automated way
#
#  Copyright 2014 - Mark Nicholson <nicholson.mark@gmail.com>
#

import os
import sys
from subprocess import Popen, PIPE

class DTC(object):

    # private options
    _format_choices = [ 'dts', 'dtb', 'asm' ]
    _phandle_choices = [ '', 'legacy', 'phandle', 'both' ]
        

    def __init__(self, compiler=None):

        # qualify a decent 'dtc' tool
        self.compiler = compiler
        if self.compiler is None:
            for path in os.environ['PATH'].split(':'):
                suspect = os.path.join(path, 'dtc')
                if not os.path.exists(suspect):
                    continue
                if not os.path.isfile(suspect):
                    continue
                self.compiler = suspect

            # catch...
            if self.compiler is None:
                raise ValueError("cannot locate 'dtc' compiler")

        else:
            # should check to see the user is not crazy
            if not os.path.exists(compiler) or not os.path.isfile(compiler):
                raise ValueError("path '%s' is not a valid compiler" % compiler)

        # grab the version
        proc = Popen( args=[self.compiler, '--version'], stdout=PIPE)
        version = proc.stdout.read()
        proc.stdout.close()
        version = version.decode('UTF-8')
        self.version = version.split()[2]

        # prep some common options
        self._in_file = None
        self.in_format = None
        self._out_file = None
        self.out_format = None
        self.out_version = None
        self.reserve = 128
        self.space = 1024
        self.pad = 1024
        self.boot_cpu = None
        self.includes = []
        self.sort_nodes = False
        self.phandle = None
        self.force = False
    
    # manage the in-file to tweak the other params
    @property
    def in_file(self):
        return self._in_file

    @in_file.setter
    def in_file(self, value):
        self._in_file = value

        # guess the output format based on the filename
        pos = self._in_file.rfind('.')
        if pos > 0:
            ext = self._in_file[pos+1:]
            if ext in self._format_choices:
                self.in_format = ext

        # otherwise, they need to manually set it

    # manage the out-file to tweak the other params
    @property
    def out_file(self):
        return self._out_file

    @out_file.setter
    def out_file(self, value):
        self._out_file = value

        # guess the output format based on the filename
        pos = self._out_file.rfind('.')
        if pos > 0:
            ext = self._out_file[pos+1:]
            if ext in self._format_choices:
                self.out_format = ext

        # otherwise, they need to manually set it

    def build(self, in_file=None, out_file=None):
        """build the output file base on the input file.
            Expects most values to be preconfigured.
            Will deduce input format and output format from filenames
            """
        # sanity check
        if self.in_file is None:
            if in_file is None:
                raise ValueError("must define in-file name")
            self.in_file = in_file
        if self.out_file is None:
            if out_file is None:
                raise ValueError("must define out-file name")
            self.out_file = out_file

        # setup the command line
        cmd = []
        cmd.append( self.compiler )

        # provide the sorting options
        if self.sort_nodes:
            cmd.append( '--sort' )

        # even provide non-sensible things
        if self.force:
            cmd.append( '--force' )

        # install the include paths
        for inc in self.includes:
            cmd += [ '-i', inc ]

        # advise on input format
        cmd += [ '-I', self.in_format ]

        # itemize output data
        cmd += [ '-O',  self.out_format ]
        cmd += [ '-o',  self.out_file ]
        if self.out_version is not None:
            cmd += [ '--out-version ', '%d' % self.out_version ]

        cmd += [ '--reserve',  '%d' % self.reserve ]

        # mutual exclusion on space & pad
        #cmd += [ '--space',  '%d' % self.space ]
        cmd += [ '--pad',  '%d' % self.pad ]

        # add the source file
        cmd.append( self.in_file )

        # run the tool
        #print("DEBUG: cmd: " + str(cmd))
        proc = Popen( cmd, stdout=PIPE)
        log = proc.stdout.read()
        proc.stdout.close()
        proc.wait()
        rc = proc.returncode

        # report
        return (rc, log)


if __name__ == "__main__":
    dtc = DTC()
    print("Version: " + str(dtc.version))
    

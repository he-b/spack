# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmDebugAgent(CMakePackage):
    """Radeon Open Compute (ROCm) debug agent"""

    homepage = "https://github.com/ROCm-Developer-Tools/rocr_debug_agent"
    url      = "https://github.com/ROCm-Developer-Tools/rocr_debug_agent/archive/roc-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.7.0', sha256='d0f442a2b224a734b0080c906f0fc3066a698e5cde9ff97ffeb485b36d2caba1')
    version('3.5.0', sha256='203ccb18d2ac508aae40bf364923f67375a08798b20057e574a0c5be8039f133')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on("elfutils", type='link')

    for ver in ['3.5.0', '3.7.0']:
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('hsakmt-roct@' + ver, type='link', when='@' + ver)

    depends_on('rocm-dbgapi@3.7.0', type='link', when='@3.7.0')
    depends_on('hip@3.7.0', when='@3.7.0')

    # https://github.com/ROCm-Developer-Tools/rocr_debug_agent/pull/4
    patch('0001-Drop-overly-strict-Werror-flag.patch', when='@3.7.0')

    @property
    def root_cmakelists_dir(self):
        if '@3.5.0' in self.spec:
            return 'src'
        else:
            return self.stage.source_path

    def cmake_args(self):
        spec = self.spec
        args = []

        if '@3.5.0' in spec:
            args.append(
                '-DCMAKE_PREFIX_PATH={0}/include/hsa;{1}/include,'.
                format(spec['hsa-rocr-dev'].prefix, spec['hsakmt-roct'].prefix)
            )

        if '@3.7.0' in spec:
            args.append(
                '-DCMAKE_MODULE_PATH={0}'.
                format(spec['hip'].prefix.cmake)
            )
        return args

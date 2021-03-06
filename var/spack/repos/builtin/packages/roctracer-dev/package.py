# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RoctracerDev(CMakePackage):
    """ROC-tracer library: Runtimes Generic Callback/Activity APIs.
       The goal of the implementation is to provide a generic independent from
       specific runtime profiler to trace API and asyncronous activity."""

    homepage = "https://github.com/ROCm-Developer-Tools/roctracer"
    url      = "https://github.com/ROCm-Developer-Tools/roctracer/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.7.0', sha256='6fa5b771e990f09c242237ab334b9f01039ec7d54ccde993e719c5d6577d1518')
    version('3.5.0', sha256='7af5326c9ca695642b4265232ec12864a61fd6b6056aa7c4ecd9e19c817f209e')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0']:
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)
        depends_on('rocminfo@' + ver, type='build', when='@' + ver)
        depends_on('hip@' + ver, type='build', when='@' + ver)

    def setup_build_environment(self, build_env):
        spec = self.spec
        build_env.set("HIP_PATH", spec['hip'].prefix)

    def patch(self):
        filter_file('${CMAKE_PREFIX_PATH}/hsa',
                    '${HSA_RUNTIME_INC_PATH}', 'src/CMakeLists.txt',
                    string=True)

    def cmake_args(self):
        args = ['-DHIP_VDI=1',
                '-DCMAKE_MODULE_PATH={0}/cmake_modules'.format(
                    self.stage.source_path),
                '-DHSA_RUNTIME_HSA_INC_PATH={0}/include'.format(
                    self.spec['hsa-rocr-dev'].prefix)
                ]
        return args

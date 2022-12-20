# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mom5-git
#
# You can edit this file again by typing:
#
#     spack edit mom5-git
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
from spack.util.executable import which

class Mom5Git(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://mom-ocean.github.io"
    git      = "https://github.com/ACCESS-NRI/MOM5.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    variant("netcdf", default=True, description="enable netcdf interface")

    # FIXME: Add dependencies if required.
    depends_on("mpi")
    depends_on("netcdf-c", type="link", when="+netcdf")
    depends_on("netcdf-fortran", type="link", when="+netcdf")

    root_cmakelists_dir = 'cmake'

    def patch(self):

        # Get the commit hash
        git_exe = which('git')
        commit = git_exe("rev-parse", "--short", "HEAD", output=str).strip()

        # Write commit into version file
        version_file = 'src/version/version.F90'

        copy(version_file+'.template', version_file)
        filter_file('{MOM_COMMIT_HASH}', commit, version_file, string=True)

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        spec = self.spec
        env["CC"] = spec["mpi"].mpicc
        env["FC"] = spec["mpi"].mpifc
        args = [
            define("CPPFLAGS", "-Duse_netCDF=1 -Duse_libMPI=1 -DLAND_BND_TRACERS=1 -DUSE_OCEAN_BGC=1 -DENABLE_ODA=1 -DSPMD=1")
        ]

        return args


# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file at the
# root of this repository, or online at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines all of our third party C dependencies."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")

def c_repositories():
    """
    We need to make sure the versions of libraries defined here stay in sync
    with the relevant Rust `*-sys` crates.

    TODO(parkmycar): Add automatic linting to detect mismatches.
    """

    BZIP2_VERSION = "1.0.8"
    BZIP2_INTEGRITY = "sha256-q1oDF27hBtPw+pDjgdpHjdrkBZGBU8yiSOaCzQxKImk="
    maybe(
        http_archive,
        name = "bzip2",
        build_file = Label("//misc/bazel/c_deps:BUILD.bzip2.bazel"),
        integrity = BZIP2_INTEGRITY,
        strip_prefix = "bzip2-{0}".format(BZIP2_VERSION),
        urls = [
            "https://sourceware.org/pub/bzip2/bzip2-{0}.tar.gz".format(BZIP2_VERSION),
        ],
    )

    LZ4_VERSION = "1.9.4"
    LZ4_INTEGRITY = "sha256-Cw46oHyMBj3fQLCCvffjehVivaQKD/UnKVfz6Yfg5Us="
    maybe(
        http_archive,
        name = "lz4",
        build_file = Label("//misc/bazel/c_deps:BUILD.lz4.bazel"),
        integrity = LZ4_INTEGRITY,
        strip_prefix = "lz4-{0}".format(LZ4_VERSION),
        urls = [
            "https://github.com/lz4/lz4/releases/download/v{0}/lz4-{0}.tar.gz".format(LZ4_VERSION),
        ],
    )

    JEMALLOC_VERSION = "5.3.0"
    JEMALLOC_INTEGRITY = "sha256-LbgtHnEZ3z5xt2QCGbbf6EeJvAU3mDw7esT3GJrs/qo="
    maybe(
        http_archive,
        name = "jemalloc",
        build_file = Label("//misc/bazel/c_deps:BUILD.jemalloc.bazel"),
        integrity = JEMALLOC_INTEGRITY,
        strip_prefix = "jemalloc-{0}".format(JEMALLOC_VERSION),
        urls = [
            "https://github.com/jemalloc/jemalloc/releases/download/{0}/jemalloc-{0}.tar.bz2".format(JEMALLOC_VERSION),
        ],
    )

    OPENSSL_VERSION = "1.1.1w"
    OPENSSL_INTEGRITY = "sha256-zzCYlQy02FOtlcCEHx+cbT3BAtzPys1SHZOSUgi3asg="
    maybe(
        http_archive,
        name = "openssl",
        build_file = Label("//misc/bazel/c_deps:BUILD.openssl.bazel"),
        integrity = OPENSSL_INTEGRITY,
        strip_prefix = "openssl-{0}".format(OPENSSL_VERSION),
        urls = [
            "https://www.openssl.org/source/openssl-{0}.tar.gz".format(OPENSSL_VERSION),
            "https://github.com/openssl/openssl/releases/download/openssl-{0}/openssl-{0}.tar.gz".format(OPENSSL_VERSION),
            "https://mirror.bazel.build/www.openssl.org/source/openssl-{0}.tar.gz".format(OPENSSL_VERSION),
        ],
    )

    PROTOC_VERSION = "3.25.2"
    PROTOC_SHA256 = "3c83e4301b968d0b4f29a0c29c0b3cde1da81d790ffd344b111c523ba1954392"
    maybe(
        http_archive,
        name = "protobuf",
        sha256 = PROTOC_SHA256,
        strip_prefix = "protobuf-{}".format(PROTOC_VERSION),
        urls = [
            "https://github.com/protocolbuffers/protobuf/archive/v{}.tar.gz".format(PROTOC_VERSION),
        ],
    )

    ZLIB_VERSION = "1.2.13"
    ZLIB_INTEGRITY = "sha256-s6JN6XqP28g1uYMxaVAQMLiXcDG8tUs7OsE3QPhGqzA="
    maybe(
        http_archive,
        name = "zlib",
        build_file = Label("//misc/bazel/c_deps:BUILD.zlib.bazel"),
        integrity = ZLIB_INTEGRITY,
        strip_prefix = "zlib-{0}".format(ZLIB_VERSION),
        urls = [
            "https://github.com/madler/zlib/releases/download/v{0}/zlib-{0}.tar.gz".format(ZLIB_VERSION),
        ],
    )

    ZSTD_VERSION = "1.5.6"
    ZSTD_INTEGRITY = "sha256-jCngbPQqrMHq/EB3ri7Gxvy5amJhV+BZPV6Co0/UA8E="
    maybe(
        http_archive,
        name = "zstd",
        build_file = Label("//misc/bazel/c_deps:BUILD.zstd.bazel"),
        integrity = ZSTD_INTEGRITY,
        strip_prefix = "zstd-{0}".format(ZSTD_VERSION),
        urls = [
            "https://github.com/facebook/zstd/releases/download/v{0}/zstd-{0}.tar.gz".format(ZSTD_VERSION),
        ],
    )

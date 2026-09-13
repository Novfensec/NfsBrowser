plugins {
    id("{{ plugin_id }}")
}

android {
    namespace = "{{ package_name }}"
    compileSdk = {{ compile_sdk }}
{{ ndk_line }}    ndkPath = "{{ ndk_path }}"

    defaultConfig {
{{ app_id_lines }}        minSdk = {{ min_sdk }}
        targetSdk = {{ target_sdk }}

{{ ndk_abi_block }}

        externalNativeBuild {
            cmake {
                arguments += listOf("-DANDROID_STL=c++_static")
            }
        }

        // ONESIGNAL_APP_ID setup for pyonesignal (reads from env and creates a string resource)
        val oneSignalId = System.getenv("ONESIGNAL_APP_ID") ?: ""
        resValue("string", "onesignal_app_id", oneSignalId)
    }

    packaging {
        jniLibs {
            useLegacyPackaging = true
            excludes += setOf(
                "**/libcrypto.so",
                "**/libssl.so",
                "**/libsqlite3.so"
            )
        }
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = "3.22.1"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

{{ flavor_block }}
{{ source_sets_block }}

    // CPython stdlib and packages contain underscore-prefixed directories
    // (e.g. zipfile/_path) that AGP's default aapt ignore pattern strips.
    // Override to keep them.
    androidResources {
        ignoreAssetsPatterns.clear()
        ignoreAssetsPatterns.addAll(listOf(
            "!.svn", "!.git", "!.ds_store", "!*.scc",
            "!CVS", "!thumbs.db", "!picasa.ini", "!*~",
            "python*", "lib-dynload", "site-packages"
        ))
    }
}

dependencies {
    implementation(fileTree("libs") { include("*.aar", "*.jar") })
{{ extra_deps }}
}

{{ site_packages_tasks }}
